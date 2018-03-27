import feedparser
from urllib.parse import urlencode

from collections import namedtuple

ARXIV_BASE = 'http://export.arxiv.org/api/'

Publication = namedtuple('Publication', ['doi', 'ref'])


def arxiv_query(method, params, agent=None):
    """Get the feed data from the arXiv API"""
    query = urlencode(params)
    return feedparser.parse(
        ARXIV_BASE + method + '?' + query,
        agent=agent,
    )


def get_publication_data(ids, agent=None):
    """Get doi and reference from the arXiv API for a list of ids

    Returns a dict mapping each of the ids to a `Publication` namedtuple with
    `doi` and `ref` fields.
    """
    params = {'id_list': ','.join(ids),
              'max_results': len(ids)}
    arxiv_data = arxiv_query('query', params=params, agent=agent)

    return {
        i: Publication(
            doi=entry.get('arxiv_doi'),
            ref=entry.get('arxiv_journal_ref')
        ) for i, entry in zip(ids, arxiv_data['entries'])
    }
