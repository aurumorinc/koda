import inspect
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils import import_script  # type: ignore

scrape = import_script("f/koda/scrape.py", "scrape")
batch_scrape = import_script("f/koda/batch_scrape.py", "batch_scrape")
crawl = import_script("f/koda/crawl.py", "crawl")
scrape_yt = import_script("f/koda/scouts/scrape_youtube_profile.py", "scrape_yt")

def test_scrape_entrypoints():
    assert not inspect.iscoroutinefunction(scrape.main)
    assert inspect.iscoroutinefunction(scrape.async_main)

def test_batch_scrape_entrypoints():
    assert not inspect.iscoroutinefunction(batch_scrape.main)
    assert inspect.iscoroutinefunction(batch_scrape.async_main)

def test_crawl_entrypoints():
    assert not inspect.iscoroutinefunction(crawl.main)
    assert inspect.iscoroutinefunction(crawl.async_main)

def test_scrape_yt_entrypoints():
    assert not inspect.iscoroutinefunction(scrape_yt.main)
    assert inspect.iscoroutinefunction(scrape_yt.async_main)
