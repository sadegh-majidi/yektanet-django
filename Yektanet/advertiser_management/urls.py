from django.urls import path

from .views import show_all_ads, click_ad, create_ad

app_name = 'advertiser_management'
urlpatterns = [
    path('', show_all_ads, name='show_all'),
    path('<int:ad_id>/', click_ad, name='click'),
    path('create/', create_ad, name='create'),
]
