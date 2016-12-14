from trakt import Trakt
# from trakt.objects import Season, Episode

import logging

logger = logging.getLogger(__name__)

def guess_slug(name):
    items = Trakt['search'].query(name, 'show')
    for item in items:
        logger.debug("\t[%.2d%%] %s (%s)" % (item.score, item.title, item.year))
        slug = item.to_identifier()['ids']['slug']
        seasons = Trakt['shows'].seasons(slug)
        if seasons is not None:
            return slug
