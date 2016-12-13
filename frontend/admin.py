from django.contrib import admin

from .models import Episode
from .models import TVShow

import logging

from guessit import guessit

logger = logging.getLogger(__name__)

def update_ep_counts(modeladmin, request, queryset):
    for obj in queryset:
        ep_count = Episode.objects.filter(tv_show__name=obj.name).count()
        obj.episode_count = ep_count
        obj.save()

update_ep_counts.short_description = "Update episode counts"

class TVShowAdmin(admin.ModelAdmin):
    actions = [update_ep_counts]

def update_ep_data(modeladmin, request, queryset):
    for obj in queryset:
        info = guessit(obj.dir_name, {'implicit': True})

        s = info['season']
        try:
            e = info['episode'] if type(info['episode']) is not list else info['episode'][-1]
        except KeyError:
            e = 0
            logger.info("No episode number available, probably a season pack")

        obj.season = s
        obj.number = e
        obj.save()


update_ep_data.short_description = "Update episode data"

class EpisodeAdmin(admin.ModelAdmin):
    actions = [update_ep_data]

admin.site.register(Episode, EpisodeAdmin)
admin.site.register(TVShow, TVShowAdmin)
