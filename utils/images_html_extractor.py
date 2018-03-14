import requests
from bs4 import BeautifulSoup
import urllib.parse

base = 'http://arquivo.pt'

with open('urls.txt', mode='r') as f:
    for url in f.readlines():
        try:
            r = requests.get(url.strip())
            html = r.content

            soup = BeautifulSoup(html)

            for imgtag in soup.find_all('img'):
                img_url = urllib.parse.urljoin(base, imgtag['src'])
                print(img_url)
                with open('extracted_img_urls.txt', mode='a') as output:
                    output.writelines(img_url + '\n')
        except Exception as error:
            with open('errors.log', mode='a') as error_output:
                error_output.writelines(str(error))
