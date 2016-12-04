from django.contrib import admin

from .models import Episode
from .models import TVShow

admin.site.register(Episode)
admin.site.register(TVShow)
