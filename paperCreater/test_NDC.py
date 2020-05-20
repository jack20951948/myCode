import pandas as pd
from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
import datetime
import random

NDC = ["prednisone", "methylprednisolone", "hydrocortisone"]

def testUrl(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        print(e)
        # return pages[-2]
    else:
        return html

for med_index, med in enumerate(NDC):
    print("start grab ", med, "................................................")
    startpage = 'https://ndclist.com/?s={}'.format(med)
    NDC_code = []
    pages = []

    html = testUrl(startpage)
    bs = BeautifulSoup(html, 'html.parser')

    course_links = bs.find_all('a', {'href': re.compile('https://ndclist.com/ndc/.*')})
    for link in course_links:
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in pages:
                pages.append(link.attrs['href'])
                link_string = int(str(link.string).replace('-', ''))
                NDC_code.append(link_string)

    for page_index, page in enumerate(pages):
        print("--------------------------------medicine:", NDC[med_index], "-----------------------------------")
        print("--------------------------------page:", page_index + 1, "/", len(pages), "------------------------------------------")
        html = testUrl(page)
        bs = BeautifulSoup(html, 'html.parser')
        packages = bs.find_all('ul', {'id': re.compile('product-packages.*')})
        for package in packages:
            sub_ndc = package.find_all('a')
            for ndc in sub_ndc:
                if ndc.string is not None:
                    if ndc.string not in NDC_code:
                        ndc_string = int(str(ndc.string).replace('-', ''))
                        NDC_code.append(ndc_string)
                        print("ndc:", ndc_string)

    print("pages:", pages)
    print("NDC_code", NDC_code)
    print("Done.............................")
    df = pd.DataFrame(NDC_code, columns=['NDC_code'])
    df.to_csv('paperCreater/{}_ndc.csv'.format(med),index=True)
    print("save csv successful!")