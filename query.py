from bs4 import BeautifulSoup
from requests import get


'''
Requests the raw HTML content of a
duckduckgo search filtered to cppreference.com
searching for the term paramater

Raises exception if content is empty/unavailable/other

Returns raw HTML content in text format
'''
def search(term, site, proxy=None):
    usr_agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/61.0.3163.100 Safari/537.36'
    }

    duckduckgo_url = f'https://html.duckduckgo.com/html?q={term}%20site%3A{site}'
    proxies = None
    if proxy:
        if proxy[:5]=="https":
            proxies = {"https":proxy} 
        else:
            proxies = {"http":proxy}

    response = get(duckduckgo_url, headers=usr_agent)    
    response.raise_for_status()

    return response.text
    
'''
Parses the raw HTML content from search() by
searching for any valid hrefs that would lead to
the term that was searched for at cppreference.com

Returns the first link if available, otherwise
returns None
'''
def parse_results(raw_html):
    soup = BeautifulSoup(raw_html, 'html.parser')
    result = soup.find('div', attrs={'class': 'links_main links_deep result__body'})
    
    if result:
        link = result.find('a', href=True)
        title = result.find('h2')
        if link and title:
            return link['href']
        else:
            return None