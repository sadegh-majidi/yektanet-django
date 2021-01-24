from django.urls import path

from .views import show_all_ads, create_ad, AdClickRedirectView

app_name = 'advertiser_management'
urlpatterns = [
    path('', show_all_ads, name='show_all'),
    path('<int:ad_id>/', AdClickRedirectView.as_view()),
    path('create/', create_ad, name='create'),
]
