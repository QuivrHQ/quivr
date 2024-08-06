import pytest

from quivr_worker.parsers.crawler import URL, extract_from_url


@pytest.mark.skip
def test_crawl():
    url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    crawl_website = URL(url=url)
    extracted_content = extract_from_url(crawl_website)
    assert len(extracted_content) > 1
