from django.db import models
from django.contrib.auth.models import User


class Advertiser(User):
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
    approve = models.BooleanField(default=False, verbose_name='Approved')

    def __str__(self):
        return self.title


class BaseAdInfo(models.Model):
    time = models.DateTimeField(verbose_name='Time')
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


class BaseCount(models.Model):
    time = models.DateTimeField(verbose_name='Hour')
    count = models.PositiveIntegerField(verbose_name='Count')

    class Meta:
        abstract = True


class AdClickCount(BaseCount):
    ad = models.ForeignKey(
        to=Ad,
        on_delete=models.CASCADE,
        verbose_name='Ad',
        related_name='clicks_count'
    )


class AdViewCount(BaseCount):
    ad = models.ForeignKey(
        to=Ad,
        on_delete=models.CASCADE,
        verbose_name='Ad',
        related_name='views_count'
    )
