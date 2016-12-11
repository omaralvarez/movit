from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from django.template import loader

from .models import Episode, TVShow

from django.views.generic.base import TemplateView
from django.contrib import messages

from .episodes import save_episode

import logging

logger = logging.getLogger(__name__)

def index(request):
    latest_episode_list = Episode.objects.order_by('-dl_date')[:10]
    template = loader.get_template('frontend/index.html')
    context = {
        'latest_episode_list': latest_episode_list,
        'active': 'index',
    }
    return HttpResponse(template.render(context, request))

def shows(request):
    tv_show_list = TVShow.objects.order_by('-name')
    tv_show_stats = []
    for show in tv_show_list:
        processed = Episode.objects.filter(tv_show__name=show.name).exclude(processed=False)
        last_ep = Episode.objects.filter(tv_show__name=show.name).latest('dl_date')
        tv_show_stats.append((show, processed.count(), last_ep))
    template = loader.get_template('frontend/shows.html')
    context = {
        'tv_show_stats': tv_show_stats,
        'active': 'shows',
    }
    return HttpResponse(template.render(context, request))

def about(request):
    template = loader.get_template('frontend/about.html')
    context = {
        'active': 'about',
    }
    return HttpResponse(template.render(context, request))

def detail_ep(request, episode_id):
    return HttpResponse("You're looking at episode %s." % episode_id)

def detail_show(request, tv_show_id):
    response = "You're looking at the results of tv show %s."
    return HttpResponse(response % tv_show_id)

@csrf_exempt
@require_POST
def add_episode(request):
    response, error = save_episode(request.POST)
    if error:
        logger.error("Could not save episode: " + response)
        return HttpResponseBadRequest(response)
    else:
        logger.debug("add_episode: completed")
        return HttpResponse("Episode data saved successfully", status=202)
