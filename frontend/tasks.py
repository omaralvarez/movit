from datetime import timedelta

from celery.utils.log import get_task_logger
from celery.decorators import periodic_task

from trakt import Trakt
from trakt.objects import Episode

from django.db.models import Max
from .models import TVShow
from .models import Episode as DjangoEpisode

logger = get_task_logger(__name__)

@periodic_task(run_every=timedelta(days=1))
def get_last_episode():
    for show in TVShow.objects.all():
        last = Trakt['shows'].last_episode(show.trakt_id)
        
        if type(last) is Episode:
            sk, ek = last.pk
            show.last_season = sk
            show.last_episode = ek

            l_s = DjangoEpisode.objects.filter(tv_show__name=show.name) \
                    .aggregate(Max('season'))['season__max']
            l_eps = DjangoEpisode.objects \
                    .filter(tv_show__name=show.name, season=l_s)
            l_ep = l_eps.aggregate(Max('number'))['number__max']

            show.updated = True if sk == l_s and ek == l_ep else False

            show.save()
        else:
            logger.info("No last episode for %s" % show.trakt_id)
