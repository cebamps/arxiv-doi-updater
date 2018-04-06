from .arxiv import get_publication_data
from bibtexparser.bparser import BibTexParser

import re


def parse_bib(bibtext):
    '''Parse a string containing BibTeX data using bibtexparser

    Identical to `bibtexparser.loads`, but with common strings (month names)
    enabled, assuming that the bib file relies on the .bst file to provide
    their definitions.
    '''
    parser = BibTexParser(common_strings=True)
    return parser.parse(bibtext)


def get_arxiv_ids(bibtext):
    '''Get BibTeX data of arXiv entries in a BibTeX string

    Returns a dict mapping each cite key for arXiv publications to the arXiv id
    encoded in the entry.
    '''
    entries = parse_bib(bibtext).entries_dict
    ids = {key: extract_arxiv_id(entry) for key, entry in entries.items()}
    return {k:v for k, v in ids.items() if v is not None}


def extract_arxiv_id(entry):
    '''Extract an API-compatible arXiv ID from a BibTeX entry'''

    # The entry field names are lowercased by bibtexparser.
    if 'arxivid' in entry:
        # Mendeley
        return re.match(r'^(?:arXiv:)?(.+?)(?:v[0-9]+)?$', entry['arxivid']).group(1)

    if entry.get('archiveprefix', '').lower() == 'arxiv' and 'eprint' in entry:
        # arXiv-recommended eprint syntax
        # Mendeley matches but does not follow the spec. Fortunately we already
        # dealt with it above.
        return entry['eprint']

    url_match = re.match(r'^https?://arxiv.org/abs/(.+?)(?:v[0-9]+)?$', entry.get('url', ''))
    if url_match:
        # Zotero, Mendeley
        return url_match.group(1)

    note_match = re.match(r'\barXiv: (.+?)(?:v[0-9]+)?\b', entry.get('note', ''))
    if note_match:
        # Zotero, should match above
        return note_match.group(1)

    return


def arxiv_pub_link(entry):
    '''Get a link to the published work from an arXiv entry'''
    if entry.doi:
        return 'https://dx.doi.org/{}'.format(entry.doi)
    elif entry.ref:
        return entry.ref
    else:
        return None


def find_published_entries(bibtext, agent=None):
    '''Get URLs to the published text of arXiv entries in a BibTeX string

    Returns a dict mapping each cite key to the indicated URL in arXiv
    metadata, or the dx.doi.org URL if the former is not present.

    Entries without URL data are not returned.
    '''
    bib_entries = get_arxiv_ids(bibtext)
    arxiv_entries = get_publication_data(list(bib_entries.values()),
                                         agent=agent)

    # we want to filter out entries without URLs
    return {
        k: v for k, v in (
            (key, arxiv_pub_link(arxiv_entries[arxiv_id]))
            for key, arxiv_id in bib_entries.items()
        )
        if v is not None
    }
