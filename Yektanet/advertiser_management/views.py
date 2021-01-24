from django.shortcuts import render
from .models import Advertiser, Ad


def show_all_ads(request):
    for ad in Ad.objects.all():
        ad.inc_views()
    advertisers = Advertiser.objects.all()
    context = {
        'advertisers': advertisers,
    }
    return render(request, 'advertisement/ads.html', context)


def click_ad(request, ad_id):
    pass


def create_ad(request):
    pass
