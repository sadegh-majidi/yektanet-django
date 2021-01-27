from django.urls import path

from .views import AdClickRedirectView, ShowAllAdsListView, NewAdFormView, CreateAdView

app_name = 'advertiser_management'
urlpatterns = [
    path('', ShowAllAdsListView.as_view(), name='show_all'),
    path('click/<int:ad_id>/', AdClickRedirectView.as_view(), name='click'),
    path('create/', CreateAdView.as_view(), name='create'),
    path('new/', NewAdFormView.as_view(), name='new_form')
]
