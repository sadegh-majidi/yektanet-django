from django.db import models


class BaseAdvertising(models.Model):
    clicks = models.IntegerField(verbose_name='Clicks', default=0)
    views = models.IntegerField(verbose_name='Views', default=0)

    class Meta:
        abstract = True


class Advertiser(BaseAdvertising):
    name = models.CharField(max_length=70, verbose_name='Advertiser Name')


class Ad(BaseAdvertising):
    title = models.CharField(max_length=50, verbose_name='Ad Title')
    img_URL = models.CharField(max_length=2000, verbose_name='Image Address')
    link = models.CharField(max_length=2000, verbose_name='Link')
    advertiser = models.ForeignKey(
        to=Advertiser,
        on_delete=models.CASCADE,
        verbose_name='Advertiser',
        related_name='ads',
    )
