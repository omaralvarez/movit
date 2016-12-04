from __future__ import unicode_literals

from django.db import models

# Create your models here.

class TVShow(models.Model):
    name = models.CharField(max_length=200)
    episode_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Episode(models.Model):
    name = models.CharField(max_length=200)
    dir_name = models.CharField(max_length=255)
    tv_show = models.ForeignKey(TVShow, on_delete=models.CASCADE)
    dl_date = models.DateTimeField('download date')
    # FIXME Enough for path?
    path = models.CharField(max_length=255)
    processed = models.BooleanField()

    def __str__(self):
        return self.dir_name
