from quivr_api.packages.files.crawl.crawler import CrawlWebsite


def test_crawl():
    url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    crawl_website = CrawlWebsite(url=url)
    extracted_content = crawl_website.process()

    assert len(extracted_content) > 1
