from __future__ import unicode_literals

from django.db import models

# Create your models here.

class TVShow(models.Model):
    name = models.CharField(max_length=200)
    episode_count = models.IntegerField(default=1)
    trakt_id = models.SlugField(max_length=255, blank=True, null=True)
    last_date = models.DateTimeField('last aired episode date', blank=True, null=True)
    last_season = models.PositiveSmallIntegerField(default=0)
    last_episode = models.PositiveSmallIntegerField(default=0)
    updated = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Episode(models.Model):
    name = models.CharField(max_length=200)
    season = models.PositiveSmallIntegerField(default=0)
    number = models.PositiveSmallIntegerField(default=0)
    dir_name = models.CharField(max_length=255)
    dl_date = models.DateTimeField('download date')
    # FIXME Enough for path?
    path = models.CharField(max_length=255)
    processed = models.BooleanField()

    # Foreign keys
    tv_show = models.ForeignKey(TVShow, on_delete=models.CASCADE)

    def __str__(self):
        return self.dir_name
