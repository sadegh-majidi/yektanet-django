from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import AdClickRedirectView, ShowAllAdsListView, NewAdFormView, CreateAdView, AdvertiserLoginApiView, \
    AdvertiserLogoutApiView, AdvertiserRegisterApiView, StatisticReportsViewSet

app_name = 'advertiser_management'

details_router = DefaultRouter()
details_router.register(prefix=r'details', viewset=StatisticReportsViewSet, basename='detail')

urlpatterns = [
    path('', ShowAllAdsListView.as_view(), name='show_all'),
    path('click/<int:ad_id>/', AdClickRedirectView.as_view(), name='click'),
    path('create/', CreateAdView.as_view(), name='create'),
    path('new/', NewAdFormView.as_view(), name='new_form'),
    path('', include(details_router.urls)),
    path('auth/register', AdvertiserRegisterApiView.as_view(), name='register'),
    path('auth/login', AdvertiserLoginApiView.as_view(), name='login'),
    path('auth/logout', AdvertiserLogoutApiView.as_view(), name='logout'),
]
