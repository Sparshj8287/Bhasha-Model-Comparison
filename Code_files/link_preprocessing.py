import numpy as np 
import pandas as pd
from urllib.parse import urlparse, urlsplit


def main_part_of_url(url):
    parsed_url = urlparse(url)
    return parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path


def link_preprocessing(links):
    valid_urls = []
    domains=[]
    india_gov = {}
    valid_urls = []
    domains=[]
    for url in links:
            parsed_url = urlparse(url)
            domain = urlsplit(url).netloc
            schema=parsed_url.scheme
            domains.append(schema+'://'+domain)
            final_domains=list(set(domains))
            valid_urls.append((url, domain))


    for url, url_domain in valid_urls:
            if url_domain == 'www.india.gov.in':
                india_gov.setdefault(url_domain, []).append(url)
    return final_domains, india_gov
