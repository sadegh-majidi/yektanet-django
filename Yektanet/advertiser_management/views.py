from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView

from .models import Advertiser, Ad


def show_all_ads(request):
    for ad in Ad.objects.all():
        ad.inc_views()
    advertisers = Advertiser.objects.all()
    context = {
        'advertisers': advertisers,
    }
    return render(request, 'advertisement/ads.html', context)


class AdClickRedirectView(RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        ad = get_object_or_404(Ad, pk=kwargs['ad_id'])
        ad.inc_clicks()
        return ad.link


def create_ad(request):
    pass
