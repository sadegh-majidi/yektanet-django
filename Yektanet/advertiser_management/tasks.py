from celery.task import task


@task(name='sum_clicks_last_hour')
def get_sum_of_clicks_per_add_last_hour():
    pass
