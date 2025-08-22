import requests
from bs4 import BeautifulSoup
import time
import re
from urllib.parse import quote_plus

USER_ID = "-QtVtNEAAAAJ"

COOKIE = "HSID=ABgNCrvx1LktuIkPt; SSID=AkUJBG1lv0q1PYPAp; APISID=DUajD8nAWi6S_PIa/AJW86Wjl1a00rvPxe; SAPISID=8vDoZFtQJv0APIjn/AOvO0tV7AfbNubuXS; __Secure-1PAPISID=8vDoZFtQJv0APIjn/AOvO0tV7AfbNubuXS; __Secure-3PAPISID=8vDoZFtQJv0APIjn/AOvO0tV7AfbNubuXS; SEARCH_SAMESITE=CgQIpp4B; SID=g.a000zgirF3rd-p1_a2m3gosbazJgPfz97VmR1l15eFAjCF0sXlDONy6E1mPJX3pZFVZ6h9528AACgYKAQUSARASFQHGX2MiUfkCxSSXjacUU7gUszh-XRoVAUF8yKpgtYDUqdzdKsHNX0atKt1X0076; __Secure-1PSID=g.a000zgirF3rd-p1_a2m3gosbazJgPfz97VmR1l15eFAjCF0sXlDOlVgz52p3KZEjOS8BCwAL1QACgYKAY0SARASFQHGX2Mi1Gl1SctVh7NeAvhddlZGdBoVAUF8yKq1Tn0bYMKKnWTjcdmYZQSL0076; __Secure-3PSID=g.a000zgirF3rd-p1_a2m3gosbazJgPfz97VmR1l15eFAjCF0sXlDOojxHz4TvA7ALL8eXBJ2LlgACgYKAZ4SARASFQHGX2MiubdSXvfSromvM0O-aWMv7xoVAUF8yKpB8ngrIciVGTVkIKVcAP-O0076; AEC=AVh_V2i24vsGHEMzb1HZpPNPNwnNB-3T8YpKfU3Xfjl6fb_0VznnqPWCQg; NID=525=f4g5umGDHmEs0Mdmz9FFKAeqfTvSyGFfF6QmmwXH2f72nrCDZn-s0YAWEmWngCVyZH-BYOXMrzgXhFPhGB9WqtPR5RUH2NulyziXn4qs3Ddiis4uDW721PHzJOaJRF8iqI2tC4l-IiFy3to4C77-ys_E0ZoVgUbp5_mT6ZXFA4wbKow5TsxJOMFB-6cT0jydrCQ-6wGBaese5VDHNsws_IV3rnuzzRA2XYTnokGBSnNdVgzbMUChunnsafMlOXJxt3dwGEL1ULMOhX_X5oB83-pzGb4jFkJyB6Rmnk0ekaSa6lZY1GpBUG8C1vf0jrJF16NMciOCyH2y6RJL1UGqccAG0UQ9IK7e6o-PLjXwyhBf0SqlTMgPyNuGwELesiiUb4bGwGvjAsjD2gX7C7BqeYTUE-05C3fld29zCzkiXNixqnBtjn0ZoaoL1l_8lv8gPvVigY2ATlFnUEmwrhAqs1oJFO5pl0jfG6reTzauqwLtxzIt59PUPW9EBm9MkUt5NIx3Mm1VY08DOxsEthppkcfGZz1I5hMD6I4kbQNKFdCWogSOoATCoRyJBSFWBPji3XSBaksTiU1KJ21qn113fVygp4yL6YSoMZG3aSvnSuR3GLoEmg96R02YjOffuHmKJC81Dodhf9OtzB0HzLDXun6mz9FQebfCNHGGWUzSNrKPCREsybr2RNtYB3nbhJuPkYFeWyvXFtz2NH4OMYrnIffTYg-gqWvUDMkdNHzrVkVqFjd4IjsJhh9tjYhBPA34cyVqrcr2Hls4FL9wPg1VZDffQcnslJCuFWg; __Secure-1PSIDTS=sidts-CjEB5H03P_KX9423RQUMzQ4NjQ9zsjJKjTsYQfGsy-c9pnvYMS7REhgA-ZxECm0rKKNBEAA; __Secure-3PSIDTS=sidts-CjEB5H03P_KX9423RQUMzQ4NjQ9zsjJKjTsYQfGsy-c9pnvYMS7REhgA-ZxECm0rKKNBEAA; GSP=LD=en:NR=20:A=_X2YDA:CPTS=1755594699:SRD=66848:RTS=20319:LM=1755594699:S=MgWH-MmFYuu9PtJf; GOOGLE_ABUSE_EXEMPTION=ID=93d4b843015a703e:TM=1755594984:C=r:IP=103.151.173.100-:S=mFAy7BQPCDASSL185Tcie0k; SIDCC=AKEyXzXQJTsr2wlHMH-IkYg_llH7Cxmsh5Akc0ix6VBTepPoRz65LuDmqtdkT3_UZ3OUiVU2cw; __Secure-1PSIDCC=AKEyXzWPD5x9fuC-VcV6RTfVq5iL56ZyWQSbl5prXaHMm0h0YWoVxe_71O_Po8pkUTqurtHntD4; __Secure-3PSIDCC=AKEyXzVkBipsCajgvEnerqyy6MQHwxkeNw7QtwDjI_kgLP-_6crJAAQaPtZU2YRpF1Tnur_phw"
# Header 一定要携带 User-Agent 和 Cookie！！！
HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
        'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cookie': COOKIE
}

def get_soup(url):
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

def get_all_papers( ):
    url_base = f"https://scholar.google.com/citations?user={USER_ID}&hl=en"
    # Loop settings
    cstart = 0      # Starting index of papers
    pagesize = 100  # Number of papers per page
    # 每次爬取100篇，直到爬取所有文章
    res = []
    while True:
        url = f'{url_base}&cstart={cstart}&pagesize={pagesize}'
        # time.sleep(1)
        soup = get_soup(url)
        rows = soup.find_all('tr', class_='gsc_a_tr')
        try:
            for row in rows:
                title = row.find('a', class_='gsc_a_at').text
                cites = row.find('a', class_='gsc_a_ac gs_ibl').text
                if cites == "":
                    cites = "0"
                info = title + ", " + cites
                res.append(info)
                with open("test.txt", "a", encoding="utf-8") as f:
                    f.write(info + "\n")
            cstart += 100
        except:
            break
    return res

if __name__ == "__main__":
    res = get_all_papers()
    