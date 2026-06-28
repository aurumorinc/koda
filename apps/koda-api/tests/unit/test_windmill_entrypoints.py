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
    assert inspect.iscoroutinefunction(scrape.main)

def test_batch_scrape_entrypoints():
    assert inspect.iscoroutinefunction(batch_scrape.main)

def test_crawl_entrypoints():
    assert inspect.iscoroutinefunction(crawl.main)

def test_scrape_yt_entrypoints():
    assert inspect.iscoroutinefunction(scrape_yt.main)
