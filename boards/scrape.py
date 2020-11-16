import requests

from urllib.parse import urlparse
from lxml import html, etree

# dict that holds xpaths for each job board
xpaths = {
    'indeed': {
        'company': '//div[contains(@class,"jobsearch-InlineCompanyRating")]/div[1]',
        'title': '//div[contains(@class,"jobsearch-JobInfoHeader-title")]',
        'description': '//div[@id="jobDescriptionText"]'
    },
    'totaljobs': {
        'company': '//a[@id="companyJobsLink"]',
        'title': '//h1[@class="brand-font"]',
        'description': '//div[@class="job-description"]'
    },
    'reed': {
        'company': '//span[@itemprop="hiringOrganization"]/a/span',
        'title': '//header[contains(@class,"job-header")]/div[1]/h1',
        'description': '//span[@itemprop="description"]'
    }
}


def get_job_info(url):
    sl_domain = urlparse(url).netloc.split('.')[1]  # second level domain
    page_html = get_page_html(url)

    # grab relevant xpaths dict
    rel_xpaths = xpaths[sl_domain]
    
    # extract nodes from html
    company_node = page_html.xpath(rel_xpaths['company'])[0]
    title_node = page_html.xpath(rel_xpaths['title'])[0]
    description_node = page_html.xpath(rel_xpaths['description'])[0]
    url = f'<a href={url} target="_blank">URL</a>'
    
    job_info = {
        'company': company_node.text_content(),
        'title': title_node.text_content(),
        'description': url + etree.tostring(description_node, encoding='unicode')
    }
    
    return job_info


def get_page_html(url):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
    headers = {'User-Agent': user_agent}
    page = requests.get(url, headers=headers)
    page_html = html.fromstring(page.content)
    
    return page_html
