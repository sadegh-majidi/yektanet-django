from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
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
    try:
        title = request.POST['title']
        image = request.POST['image']
        link = request.POST['link']
        advertiser = Advertiser.objects.get(pk=int(request.POST['advertiser_id']))
        ad = Ad(title=title, image=image, link=link, advertiser=advertiser)
        ad.save()
    except(KeyError, Advertiser.DoesNotExist):
        return render(request, 'advertisement/create_add.html', {'error_message': 'Error happened.'})
    else:
        return redirect('/advertisements/')


def new_ad_form(request):
    return render(request, 'advertisement/create_add.html', {})
