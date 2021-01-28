from django.urls import path

from .views import AdClickRedirectView, ShowAllAdsListView, NewAdFormView, CreateAdView, ClickReporterView,\
    RateSummaryView, RatePerHourView, ViewReporterView, AverageTimeBetweenViewAndClickView

app_name = 'advertiser_management'
urlpatterns = [
    path('', ShowAllAdsListView.as_view(), name='show_all'),
    path('click/<int:ad_id>/', AdClickRedirectView.as_view(), name='click'),
    path('create/', CreateAdView.as_view(), name='create'),
    path('new/', NewAdFormView.as_view(), name='new_form'),
    path('details/click/summary', ClickReporterView.as_view(), name='click_summary'),
    path('details/view/summary', ViewReporterView.as_view(), name='view_summary'),
    path('details/rate/summary', RateSummaryView.as_view(), name='rate_summary'),
    path('details/rate/hour-based', RatePerHourView.as_view(), name='rate_summary_hour'),
    path('details/duartion/avarage-view-click', AverageTimeBetweenViewAndClickView.as_view(), name='time_difference')
]
