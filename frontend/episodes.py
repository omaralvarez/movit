import logging
from datetime import datetime

from django.core.exceptions import ValidationError

from .models import (Episode, TVShow)

from guessit import guessit

logger = logging.getLogger(__name__)

def validate_episode(item):
    """
    Validates that a result dictionary has all needed parameters
    It returns a tuple
        Environment, False  when no errors where found
        Errormessage, True  when there is an error
    """
    mandatory_data = [
        'dir_name',
        'dl_date',
        'path',
        'processed',
    ]

    error = True
    for key in mandatory_data:
        if key not in item:
            return 'Key "' + key + '" missing from request', error
        elif key in item and item[key] == "":
            return 'Value for key "' + key + '" empty in request', error

    info = guessit(item['dir_name'])

    tv_show_name = info['title']

    # Check that the TVShow exists or create it
    t, created = TVShow.objects.get_or_create(name=tv_show_name)

    if not created:
        t.episode_count += 1
        t.full_clean()
        t.save()

    error = False
    return t, error

def save_episode(data):
    res, error = validate_episode(data)
    if error:
        return res, True
    else:
        assert(isinstance(res, TVShow))
        show = res

    ep, created = Episode.objects.get_or_create(dir_name=data["dir_name"],
                                                dl_date=data["dl_date"],
                                                processed=data["processed"],
                                                path=data["path"],
                                                tv_show=show)

    if created:
        #ep.full_clean()
        #ep.save()
        pass
    else:
        logger.warning("Episode already exists!")

    return (show, ep), False
