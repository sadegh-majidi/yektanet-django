import django.views.generic.base as generic
from django.shortcuts import get_object_or_404, reverse
from django.views.generic.list import ListView
from django.views.generic.base import RedirectView, TemplateView
from django.core.exceptions import ValidationError
from django.db.models import Count, Subquery, F, Avg, DurationField, OuterRef, ExpressionWrapper
from django.db.models.functions import TruncHour

from .models import Advertiser, Ad, View, Click


class ShowAllAdsListView(ListView):
    template_name = 'advertisement/ads.html'
    context_object_name = 'advertisers'

    def get_queryset(self):
        advertisers = Advertiser.objects.all()
        for advertiser in advertisers:
            for ad in advertiser.ads.all():
                View.objects.create(user_ip=self.request.user_ip, ad=ad)
        return advertisers


class AdClickRedirectView(RedirectView):
    pattern_name = 'click'
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        ad = get_object_or_404(Ad, pk=kwargs['ad_id'])
        Click.objects.create(user_ip=self.request.user_ip, ad=ad)
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
            advertiser = Advertiser.objects.get(pk=int(self.request.POST['advertiser_id']))
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


class StatisticsReportView(generic.View):
    def get_sum_of_clicks_per_hour(self):
        result = Click.objects.annotate(hour=TruncHour('time')).values('ad', 'hour').annotate(view=Count('id')).all()
        return result

    def get_sum_of_views_per_hour(self):
        result = View.objects.annotate(hour=TruncHour('time')).values('ad', 'hour').annotate(view=Count('id')).all()
        return result

    def get_clicks_per_view_rate(self):
        pass

    def get_average_time_difference_view_click(self):
        pass
