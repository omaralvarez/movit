from django.contrib import admin

from .models import Episode
from .models import TVShow

def update_ep_counts(modeladmin, request, queryset):
    for obj in queryset:
        ep_count = Episode.objects.filter(tv_show__name=obj.name).count
        obj.episode_count = ep_count
        obj.save()


update_ep_counts.short_description = "Update episode counts"

class EpisodeAdmin(admin.ModelAdmin):
    actions = [update_ep_counts]

admin.site.register(Episode, EpisodeAdmin)
admin.site.register(TVShow)
