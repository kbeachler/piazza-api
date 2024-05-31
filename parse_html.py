# pip install beautifulsoup4 lxml

from bs4 import BeautifulSoup

def parse_def(text):
    html_text = text
    soup = BeautifulSoup(html_text, 'lxml')
    plain_text = soup.get_text()
    return plain_text