from django.contrib import admin
from .models import Advertiser, Ad, Click, View, AdClickCount, AdViewCount

admin.site.register(Advertiser)
admin.site.register(Click)
admin.site.register(View)
admin.site.register(AdClickCount)
admin.site.register(AdViewCount)


@admin.register(Ad)
class AdModel(admin.ModelAdmin):
    list_display = ['title', 'approve']
    list_filter = (('approve', admin.BooleanFieldListFilter),)
    search_fields = ['title']
    actions = ['mark_approved', 'mark_not_approved']

    def mark_approved(self, request, queryset):
        queryset.update(approve=True)

    def mark_not_approved(self, request, queryset):
        queryset.update(approve=False)

    mark_approved.short_description = 'Mark selected ads as approved'
    mark_not_approved.short_description = 'Mark selected ads as not approved'
