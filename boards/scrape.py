import requests

from lxml import html, etree
from itertools import chain

def scrape_indeed_posting(url):
    page = requests.get(url)
    page_html = html.fromstring(page.content)

    company = stringify_children(page_html.xpath('//*[contains(@class,"jobsearch-JobInfoHeader-subtitle")]/div/div'))[0]
    title = stringify_children(page_html.xpath('//*[contains(@class,"jobsearch-JobInfoHeader-title-container")]/h1'))[0]
    description = stringify_children(page_html.xpath('//div[@id="jobDescriptionText"]'))
    url = f'<a href={url} target="_blank">URL</a>'

    job_info = {
        'company': company,
        'title': title,
        'description': url + '<br><br>' + ' '.join(description)
    }
    
    return job_info

def stringify_children(node):
    parts = (
        [node[0].text] + list(chain(*([c.text, etree.tostring(c, encoding='unicode'), c.tail] for c in node[0].getchildren()))) + [node[0].tail]
    )
    return list(filter(None, parts))
