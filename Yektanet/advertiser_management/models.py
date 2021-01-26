from django.db import models


class Advertiser(models.Model):
    name = models.CharField(max_length=70, verbose_name='Advertiser Name')

    def __str__(self):
        return self.name


class Ad(models.Model):
    title = models.CharField(max_length=50, verbose_name='Ad Title')
    image = models.CharField(max_length=2000, verbose_name='Image Address')
    link = models.CharField(max_length=2000, verbose_name='Link')
    advertiser = models.ForeignKey(
        to=Advertiser,
        on_delete=models.CASCADE,
        verbose_name='Advertiser',
        related_name='ads'
    )

    def __str__(self):
        return self.title


class BaseAdInfo(models.Model):
    click_time = models.DateTimeField(auto_now_add=True, verbose_name='Time')
    user_ip = models.GenericIPAddressField(verbose_name='User IP')

    class Meta:
        abstract = True


class Click(BaseAdInfo):
    ad = models.ForeignKey(
        to=Ad,
        on_delete=models.CASCADE,
        verbose_name='Clicked Ad',
        related_name='clicks'
    )


class View(BaseAdInfo):
    ad = models.ForeignKey(
        to=Ad,
        on_delete=models.CASCADE,
        verbose_name='Viewed Ad',
        related_name='views'
    )
