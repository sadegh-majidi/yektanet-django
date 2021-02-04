from django.shortcuts import get_object_or_404, reverse
from django.views.generic.base import RedirectView
from django.core.exceptions import ValidationError
from django.db.models import Count, Subquery, F, Avg, DurationField, OuterRef, ExpressionWrapper, FloatField
from django.db.models.functions import TruncHour, Cast
from django.http.response import JsonResponse, HttpResponseRedirect
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from .serializers.ad_serializer import AdSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_200_OK
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import update_last_login
from .serializers.advertiser_serializer import AdvertiserSerializer
from .serializers.login_credential_serializer import LoginCredentialSerializer
from .permissions import IsAdvertiser

from .models import Advertiser, Ad, View, Click


class ShowAllAdsListView(ListAPIView):
    template_name = 'advertisement/ads.html'
    renderer_classes = [TemplateHTMLRenderer]
    queryset = Advertiser.objects.all()
    serializer_class = AdvertiserSerializer
    process_ip = True

    def get(self, request, *args, **kwargs):
        advertisers = self.get_queryset()
        for advertiser in advertisers:
            for ad in advertiser.ads.all():
                View.objects.create(user_ip=request.user_ip, ad=ad, time=timezone.now())
        return Response({'advertisers': advertisers})


class AdClickRedirectView(RedirectView):
    pattern_name = 'click'
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        ad = get_object_or_404(Ad, pk=kwargs['ad_id'])
        Click.objects.create(user_ip=self.request.user_ip, ad=ad, time=timezone.now())
        return ad.link


class CreateAdView(CreateAPIView):
    serializer_class = AdSerializer
    queryset = Ad.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsAdvertiser]

    def create(self, request, *args, **kwargs):
        try:
            super().create(request, *args, **kwargs)
        except (ValidationError, Advertiser.DoesNotExist) as e:
            request.session['error_message'] = str(e)
            return HttpResponseRedirect(redirect_to=reverse('advertiser_management:new_form'))
        else:
            return HttpResponseRedirect(redirect_to=reverse('advertiser_management:show_all'))

    def perform_create(self, serializer):
        serializer.save(advertiser=self.request.user.advertiser)


class NewAdFormView(APIView):
    template_name = 'advertisement/create_add.html'
    renderer_classes = [TemplateHTMLRenderer]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        context = {}
        if 'error_message' in self.request.session:
            context['error_message'] = self.request.session.get('error_message')
            del self.request.session['error_message']
        return Response(context)


class StatisticReportsViewSet(ViewSet):
    @action(detail=False, url_path='click/summary', url_name='click_summary')
    def get_sum_of_clicks_per_hour(self, request):
        result = Click.objects.all().annotate(hour=TruncHour('time')).values('ad', 'hour').annotate(click=Count('id'))
        return JsonResponse(list(result), safe=False)

    @action(detail=False, url_path='view/summary', url_name='view_summary')
    def get_sum_of_views_per_hour(self, request):
        result = View.objects.all().annotate(hour=TruncHour('time')).values('ad', 'hour').annotate(view=Count('id'))
        return JsonResponse(list(result), safe=False)

    @action(detail=False, url_path='rate/summary', url_name='rate_summary')
    def get_view_clicks_per_view_rate_summary(self, request):
        result = Ad.objects.all().annotate(view_count=Count('views')).annotate(click_count=Count('clicks')). \
            annotate(
            rate=ExpressionWrapper(
                (Cast('click_count', FloatField()) / F('view_count')),
                output_field=FloatField(),
            ),
        ).order_by('-rate').values('id', 'rate')
        return JsonResponse(list(result), safe=False)

    @action(detail=False, url_path='rate/hour-based', url_name='rate_summary_hour')
    def get_clicks_per_view_rate_hour(self, request):
        views_set = self.get_sum_of_views_per_hour(request)
        clicks_set = self.get_sum_of_clicks_per_hour(request)
        clicks_modified_set = {(item['ad'], item['hour']): item for item in clicks_set}
        result = []
        for view in views_set:
            views = view['view']
            clicks = clicks_modified_set.get((view['ad'], view['hour']), {}).get('click', 0)
            result.append({
                'ad_id': view['ad'],
                'hour': view['hour'],
                'rate': clicks / views,
            })
        result = sorted(result, key=lambda item: (item['rate'], item['hour']), reverse=True)
        return JsonResponse(list(result), safe=False)

    @action(detail=False, url_path='duration/average-view-click', url_name='time_difference')
    def get_average_time_difference_view_click(self, request):
        result = Click.objects.annotate(
            time_diff=Subquery(
                View.objects.filter(
                    ad=OuterRef('ad'),
                    user_ip=OuterRef('user_ip'),
                    time__lte=OuterRef('time')
                ).annotate(diff=OuterRef('time') - F('time')).order_by('diff').values('diff')[:1]
            )
        ).aggregate(average_time=Avg('time_diff', output_field=DurationField())).get('average_time')
        return JsonResponse({'average_time_between_view_and_click': str(result)})


class AdvertiserRegisterApiView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = AdvertiserSerializer


class AdvertiserLoginApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginCredentialSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        valid_data = serializer.validated_data
        advertiser = get_object_or_404(Advertiser, username=valid_data.get('username', ''))
        password = valid_data.get('password', '')
        if advertiser.check_password(password):
            raise ValidationError(message='Wrong password.', code=HTTP_403_FORBIDDEN)
        token, created = Token.objects.get_or_create(user=advertiser)
        update_last_login(None, token.user)
        return Response(
            data={
                'auth_token': token.key
            },
            status=HTTP_200_OK
        )


class AdvertiserLogoutApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsAdvertiser]

    def get(self, request):
        request.user.auth_token.delete()
        return Response(status=HTTP_200_OK)
