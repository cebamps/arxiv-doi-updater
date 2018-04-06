from .arxiv import get_publication_data
from bibtexparser.bparser import BibTexParser


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
    ids = {key: entries[key]['eprint']
           for key, entry in entries.items()
           if 'eprint' in entry}
    return ids


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
