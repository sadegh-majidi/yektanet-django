from django.db import models


class BaseAdvertising(models.Model):
    clicks = models.IntegerField(verbose_name='Clicks', default=0)
    views = models.IntegerField(verbose_name='Views', default=0)

    def inc_clicks(self):
        self.clicks += 1
        self.save()

    def inc_views(self):
        self.views += 1
        self.save()

    class Meta:
        abstract = True


class Advertiser(BaseAdvertising):
    name = models.CharField(max_length=70, verbose_name='Advertiser Name')

    def __str__(self):
        return self.name


class Ad(BaseAdvertising):
    title = models.CharField(max_length=50, verbose_name='Ad Title')
    img_URL = models.CharField(max_length=2000, verbose_name='Image Address')
    link = models.CharField(max_length=2000, verbose_name='Link')
    advertiser = models.ForeignKey(
        to=Advertiser,
        on_delete=models.CASCADE,
        verbose_name='Advertiser',
        related_name='ads'
    )

    def inc_clicks(self):
        super(Ad, self).inc_clicks()
        self.advertiser.inc_clicks()

    def inc_views(self):
        super(Ad, self).inc_views()
        self.advertiser.inc_views()

    def __str__(self):
        return self.title
