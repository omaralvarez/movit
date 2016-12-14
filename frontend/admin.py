from django.contrib import admin

from .models import Episode
from .models import TVShow

from .episodes import extract_info
from .shows import guess_slug

import logging

logger = logging.getLogger(__name__)

def update_ep_counts(modeladmin, request, queryset):
    for obj in queryset:
        ep_count = Episode.objects.filter(tv_show__name=obj.name).count()
        obj.episode_count = ep_count
        obj.save()

update_ep_counts.short_description = "Update episode counts"

def update_slugs(modeladmin, request, queryset):
    for obj in queryset:
        obj.trakt_id = guess_slug(obj.name)
        obj.save()

update_slugs.short_description = "Update Trakt slugs"

class TVShowAdmin(admin.ModelAdmin):
    actions = [update_ep_counts, update_slugs]

def update_ep_data(modeladmin, request, queryset):
    for obj in queryset:
        info = guessit(obj.dir_name, {'implicit': True})

        s,e = extract_info(info)

        obj.season = s
        obj.number = e
        obj.save()


update_ep_data.short_description = "Update episode data"

class EpisodeAdmin(admin.ModelAdmin):
    actions = [update_ep_data]

admin.site.register(Episode, EpisodeAdmin)
admin.site.register(TVShow, TVShowAdmin)
