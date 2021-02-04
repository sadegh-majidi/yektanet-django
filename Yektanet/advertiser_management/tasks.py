from celery import shared_task
from .models import Click, View, AdClickCount, AdViewCount
from django.db.models.functions import TruncHour
from django.db import connection
from django.db.models import Count, Sum
from django.utils import timezone
from django.http import JsonResponse


@shared_task
def count_sum_of_clicks_per_ad_last_hour():
    hour_from = timezone.now().replace(microsecond=0, second=0, minute=0) - timezone.timedelta(hours=1)
    result = Click.objects.annotate(hour=TruncHour('time')).values('ad', 'hour').annotate(click=Count('id')).filter(
        hour=hour_from
    )
    result_list = [AdClickCount(time=item['hour'], count=item['click'], ad_id=item['ad']) for item in result]
    AdClickCount.objects.bulk_create(result_list)
    return None


@shared_task
def count_sum_of_views_per_ad_last_hour():
    hour_from = timezone.now().replace(microsecond=0, second=0, minute=0) - timezone.timedelta(hours=1)
    result = View.objects.annotate(hour=TruncHour('time')).values('ad', 'hour').annotate(view=Count('id')).filter(
        hour=hour_from
    )
    result_list = [AdViewCount(time=item['hour'], count=item['view'], ad_id=item['ad']) for item in result]
    AdViewCount.objects.bulk_create(result_list)
    return None


@shared_task
def get_ad_clicks_last_day():
    query_set = AdClickCount.objects.values('ad').annotate(sum_clicks=Sum('count'))
    result = str(JsonResponse(list(query_set), safe=False).content)
    cursor = connection.cursor()
    cursor.execute(f'TRUNCATE TABLE `{AdClickCount._meta.db_table}`')
    return result


@shared_task
def get_ad_views_last_day():
    query_set = AdViewCount.objects.values('ad').annotate(sum_views=Sum('count'))
    result = str(JsonResponse(list(query_set), safe=False).content)
    cursor = connection.cursor()
    cursor.execute(f'TRUNCATE TABLE `{AdViewCount._meta.db_table}`')
    return result
