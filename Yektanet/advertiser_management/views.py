from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, reverse
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
    pattern_name = 'click'
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
        assert link.startswith('http'), 'Links should start with http'
        ad = Ad(title=title, image=image, link=link, advertiser=advertiser)
        ad.save()
    except(KeyError, Advertiser.DoesNotExist, AssertionError) as e:
        request.session['error_message'] = str(e)
        return redirect(reverse('advertiser_management:new_form'))
    else:
        return redirect('/advertiser_management/')


def new_ad_form(request, *args, **kwargs):
    context = {}
    if 'error_message' in request.session:
        context['error_message'] = request.session.get('error_message')
        del request.session['error_message']
    return render(request, 'advertisement/create_add.html', context)
