from datetime import datetime
from datetime import timedelta
import pytz

from celery.utils.log import get_task_logger
from celery.decorators import periodic_task, task

from trakt import Trakt
from trakt.objects import Episode

from django.db.models import Max
from django.conf import settings
from .models import TVShow
from .models import Episode as DjangoEpisode
from .shows import guess_slug

logger = get_task_logger(__name__)

@periodic_task(run_every=timedelta(days=1))
def get_last_episode():
    for show in TVShow.objects.exclude(skip=True):
        # TODO Check if slug exists if not guess_slug first
        last = Trakt['shows'].last_episode(show.trakt_id, extended='full')

        if type(last) is Episode:
            sk, ek = last.pk
            show.last_season = sk
            show.last_episode = ek
            show.last_date = last.first_aired

            l_s = DjangoEpisode.objects.filter(tv_show__name=show.name) \
                    .aggregate(Max('season'))['season__max']
            l_eps = DjangoEpisode.objects \
                    .filter(tv_show__name=show.name, season=l_s)
            l_ep = l_eps.aggregate(Max('number'))['number__max']

            days = (datetime.now(pytz.utc) - last.first_aired).days

            show.updated = True if (sk == l_s and ek == l_ep) or days < settings.DOWNLOAD_DELAY else False

            show.save()
        else:
            logger.info("No last episode for %s" % show.trakt_id)

@task(ignore_result=True)
def scrape_trakt_slugs(pks):
    for primary_key in pks:
        obj = TVShow.objects.get(pk=primary_key)
        obj.trakt_id = guess_slug(obj.name)
        obj.save()
