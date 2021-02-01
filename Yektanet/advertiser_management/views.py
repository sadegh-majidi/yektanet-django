import django.views.generic.base as generic
from django.shortcuts import get_object_or_404, reverse
from django.views.generic.list import ListView
from django.views.generic.base import RedirectView, TemplateView
from django.core.exceptions import ValidationError
from django.db.models import Count, Subquery, F, Avg, DurationField, OuterRef, ExpressionWrapper, FloatField
from django.db.models.functions import TruncHour, Cast
from django.http.response import JsonResponse
from django.utils import timezone

from .models import Advertiser, Ad, View, Click


class ShowAllAdsListView(ListView):
    template_name = 'advertisement/ads.html'
    context_object_name = 'advertisers'

    def get_queryset(self):
        advertisers = Advertiser.objects.all()
        for advertiser in advertisers:
            for ad in advertiser.ads.all():
                View.objects.create(user_ip=self.request.user_ip, ad=ad, time=timezone.now())
        return advertisers


class AdClickRedirectView(RedirectView):
    pattern_name = 'click'
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        ad = get_object_or_404(Ad, pk=kwargs['ad_id'])
        Click.objects.create(user_ip=self.request.user_ip, ad=ad, time=timezone.now())
        return ad.link


class CreateAdView(RedirectView):
    pattern_name = 'create'
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        try:
            title = self.request.POST['title']
            image = self.request.POST['image']
            link = self.request.POST['link']
            advertiser = Advertiser.objects.get(username=self.request.POST['advertiser_username'])
            assert link.startswith('http'), 'Links should start with http'
            Ad.objects.create(title=title, image=image, link=link, advertiser=advertiser)
        except(KeyError, Advertiser.DoesNotExist, AssertionError, ValidationError) as e:
            self.request.session['error_message'] = str(e)
            return reverse('advertiser_management:new_form')
        else:
            return reverse('advertiser_management:show_all')


class NewAdFormView(TemplateView):
    template_name = 'advertisement/create_add.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'error_message' in self.request.session:
            context['error_message'] = self.request.session.get('error_message')
            del self.request.session['error_message']
        return context


def get_sum_of_clicks_per_hour():
    result = Click.objects.all().annotate(hour=TruncHour('time')).values('ad', 'hour').annotate(click=Count('id'))
    return result


def get_sum_of_views_per_hour():
    result = View.objects.all().annotate(hour=TruncHour('time')).values('ad', 'hour').annotate(view=Count('id'))
    return result


def get_view_clicks_per_view_rate_summary():
    result = Ad.objects.all().annotate(view_count=Count('views')).annotate(click_count=Count('clicks')). \
        annotate(
        rate=ExpressionWrapper(
            (Cast('click_count', FloatField()) / F('view_count')),
            output_field=FloatField(),
        ),
    ).order_by('-rate').values('id', 'rate')
    '''
    views_set = View.objects.all().values('ad').annotate(view=Count('id'))
    clicks_set = Click.objects.all().values('ad').annotate(click=Count('id'))
    clicks_modified_set = {item['ad']: item for item in clicks_set}
    result = []
    for view in views_set:
        views = view['view']
        clicks = clicks_modified_set.get(view['ad'], {}).get('click', 0)
        result.append({
            'ad_id': view['ad'],
            'rate': clicks / views,
        })
    result = sorted(result, key=lambda item: item['rate'], reverse=True)
    '''
    return result


def get_clicks_per_view_rate_hour():
    views_set = get_sum_of_views_per_hour()
    clicks_set = get_sum_of_clicks_per_hour()
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
    return result


def get_average_time_difference_view_click():
    result = Click.objects.annotate(
        time_diff=Subquery(
            View.objects.filter(
                ad=OuterRef('ad'),
                user_ip=OuterRef('user_ip'),
                time__lte=OuterRef('time')
            ).annotate(diff=OuterRef('time') - F('time')).order_by('diff').values('diff')[:1]
        )
    ).aggregate(average_time=Avg('time_diff', output_field=DurationField())).get('average_time')
    return result


'''
    total = timezone.timedelta()
    count = 0
    for click in Click.objects.all():
        duration = View.objects.all().filter(
            ad_id=click.ad_id,
            user_ip=click.user_ip,
            time__lte=click.time
        ).annotate(diff=click.time - F('time')).order_by('diff')
        print(type(duration))
        total = total + duration[0].diff
        count += 1
        '''


class ClickReporterView(generic.View):
    def get(self, request):
        return JsonResponse(list(get_sum_of_clicks_per_hour()), safe=False)


class ViewReporterView(generic.View):
    def get(self, request):
        return JsonResponse(list(get_sum_of_views_per_hour()), safe=False)


class RateSummaryView(generic.View):
    def get(self, request):
        return JsonResponse(list(get_view_clicks_per_view_rate_summary()), safe=False)


class RatePerHourView(generic.View):
    def get(self, request):
        return JsonResponse(list(get_clicks_per_view_rate_hour()), safe=False)


class AverageTimeBetweenViewAndClickView(generic.View):
    def get(self, request):
        return JsonResponse({'average_time_between_view_and_click': str(get_average_time_difference_view_click())})
