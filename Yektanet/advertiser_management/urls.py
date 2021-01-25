from django.urls import path

from .views import show_all_ads, create_ad, AdClickRedirectView, new_ad_form

app_name = 'advertiser_management'
urlpatterns = [
    path('', show_all_ads, name='show_all'),
    path('click/<int:ad_id>/', AdClickRedirectView.as_view(), name='click'),
    path('create/', create_ad, name='create'),
    path('new/', new_ad_form, name='new_form')
]
