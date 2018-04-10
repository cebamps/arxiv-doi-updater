import pytest
from arxiv_doi_updater import bib
from collections import namedtuple

#def test_arxiv_extraction(bibtext):
#    arxiv_ids = bib.get_arxiv_ids(bibtext)
#    assert arxiv_ids[key] == expected_arxiv_id

ArxivIdTestData = namedtuple('ArxivIdTestData', ['entry', 'expected'])

arxiv_id_test_data = {
    'url-new-versioned': ArxivIdTestData(
        {'url': 'http://arxiv.org/abs/1703.08618v1'},
        '1703.08618'
    ),
    'url-old-versioned': ArxivIdTestData(
        {'url': 'http://arxiv.org/abs/quant-ph/0210073v1'},
        'quant-ph/0210073'
    ),
    'mendeley-old-unversioned': ArxivIdTestData(
        {'archiveprefix': 'arXiv',
         'arxivid': 'quant-ph/0404076',
         'eprint': '0404076',
         'primaryclass': 'quant-ph'},
        'quant-ph/0404076'
    ),
    'mendeley-old-versioned': ArxivIdTestData(
        {'archiveprefix': 'arXiv',
         'arxivid': 'arXiv:quant-ph/0210073v1',
         'eprint': '0210073v1',
         'primaryclass': 'arXiv:quant-ph'},
        'quant-ph/0210073'
    ),
    'zotero-new': ArxivIdTestData(
        {'url': 'http://arxiv.org/abs/1703.08618',
         'journal': 'arXiv:1703.08618 [math-ph, physics:quant-ph]',
         'note': 'arXiv: 1703.08618'},
        '1703.08618'
    ),
    'zotero-old': ArxivIdTestData(
        {'url': 'http://arxiv.org/abs/quant-ph/0304127',
         'journal': 'arXiv:quant-ph/0304127',
         'note': 'arXiv: quant-ph/0304127'},
        'quant-ph/0304127'
    ),
}


@pytest.mark.parametrize("arxiv_id_test", arxiv_id_test_data.values(),
                         ids=list(arxiv_id_test_data.keys()))
def test_arxiv_id_extraction(arxiv_id_test):
    assert bib.extract_arxiv_id(arxiv_id_test.entry) == arxiv_id_test.expected
