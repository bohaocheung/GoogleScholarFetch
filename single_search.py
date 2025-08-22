import requests
from bs4 import BeautifulSoup
import time
import re
from urllib.parse import quote_plus
import yaml

with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

# Header 一定要携带 User-Agent 和 Cookie！！！
HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
        'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cookie': config["cookie"]
}

ALL_CITES = config["cites"]

def make_scholar_url(title):
    """构建Google Scholar搜索URL"""
    base_url = "https://scholar.google.com/scholar"
    params = {
        "q": title,
        "hl": "en",
        "as_sdt": "0,5"
    }
    return f"{base_url}?{'&'.join(f'{k}={quote_plus(str(v))}' for k, v in params.items())}"

def get_soup(url):
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')


def get_citing_papers(title, start_item):
    """获取引用论文的列表"""    
    page = start_item
    item = 0
    try:
        # 1. 找到引用链接
        # time.sleep(1)
        search_url  = make_scholar_url(title)
        search_soup = get_soup(search_url)
        print("Search URL:", search_url)
        citing_link = None
        for link in search_soup.find_all('a'):
            # print(link.text)
            if '被引用次数' in link.text or 'Cited by' in link.text:
                citing_link = link
                break
        
        if not citing_link:
            print("未找到引用链接")
            return []
            
        # 2. 获取引用页面
        pattern = r'cites=([^&]+)'
        match = re.search(pattern, citing_link['href'])
        if not match:
            print("没有提取到cites值")
            return []
        
        cites_value = match.group(1)
        citing_url = f"https://scholar.google.com/scholar?cites={cites_value}&hl=en&start="
        
        over = False
        # 3. 每页10条被引文章
        while not over:
            item = 0
            page_url = citing_url + str(page)
            print(f"{title} 引用的第 {page} 条")
            # time.sleep(1)
            page_soup = get_soup(page_url)
            print("Page URL:", page_url)
            h3_tags = page_soup.find_all('h3')
            
            if len(h3_tags) == 0:
                print("没有找到文章")
                break
            
            # 4. 针对每条被引文章
            for j, h3 in enumerate(h3_tags):
                a_tag = h3.find('a')
                if a_tag and 'id' in a_tag.attrs:  
                    res = title + ", " + a_tag.get_text() # 获取文章标题
                    # print(f"a标签的id: ")
                    article_url = f"https://scholar.google.com/scholar?q=info:{a_tag['id']}:scholar.google.com/&hl=en&output=cite"
                    # time.sleep(1)
                    print("Article URL:", article_url)
                    article_soup = get_soup(article_url)
                    div_tags = article_soup.find_all('div', class_='gs_citr', tabindex="0")

                    # 提取作者信息
                    author_info = ""
                    for div in div_tags:
                        text = div.get_text()
                        # 根据不同格式的文本特点，提取作者信息
                        if "Chicago" in div.find_parent('tr').find('th').get_text():
                            # Chicago格式：作者信息在第一个双引号前
                            author_info = text.split('"')[0].strip()
                        elif "Vancouver" in div.find_parent('tr').find('th').get_text():
                            # Vancouver格式：作者信息在第一个句号前
                            author_info = text.split('.')[0].strip()
                        else:
                            continue
                        author_info = "\"" + author_info + "\""
                        # print(author_info)
                        res += (", " + author_info)
                    # print(author_info)
                    with open("res.csv", "a", encoding="utf-8") as f:
                        f.write(res+"\n")
                        item += 1
                        # print("inlineitem:", item)
                    
            if page == (ALL_CITES - 1) // 10 * 10:
                print("全部搜索完成")
                over = True
                item = 0
                break

            # 因为 Cookie 设定的每页呈现搜索结果为 10    
            page += 10
            item = 0

    except Exception as e:
        print(f"爬取失败: {str(e)}")
        while item > 0:
            print("item:", item)
            with open("res.csv", "r", encoding="utf-8") as f:
                lines = f.readlines()
            with open("res.csv", "w", encoding="utf-8") as f:
                f.writelines(lines[:-1])
            item -= 1
            
        with open("config.yaml", "w", encoding="utf-8") as f:
            config["start_item"] = page
            yaml.dump(config, f)
        over = True
    
    if not over:
        while item > 0:
            with open("res.csv", "r", encoding="utf-8") as f:
                lines = f.readlines()
            with open("res.csv", "w", encoding="utf-8") as f:
                f.writelines(lines[:-1])
            item -= 1
        with open("config.yaml", "w", encoding="utf-8") as f:
            config["start_item"] = page
            yaml.dump(config, f)

        
    
    
def main():
    title = config["title"]
    start_item = config["start_item"]
    get_citing_papers(title, start_item)


if __name__ == "__main__":
    main() 