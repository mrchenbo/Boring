"""
从笔下文学下载小说
参数1：小说目录页地址
参数2：小说保存文件名
"""
import re
import sys
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

web_url = "https://www.bixia.org"


def get_content(page_url):
    r = requests.get(page_url)
    soup = BeautifulSoup(r.text, "lxml")
    content = soup.find_all('div', attrs={'id': 'content'})

    content = str(content).replace(r'<br/>', '\n')

    text = re.findall(
        '[\n\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b\u4e00-\u9fa5]', str(content))
    return ''.join(text)


def get_catalog(book_url):
    r = requests.get(book_url)
    soup = BeautifulSoup(r.text, "lxml")
    catalog = soup.find_all('a', string=re.compile('第\d+章'))

    logs = []
    for ele in catalog:
        title = ele.get_text()
        href = ele.get('href')
        if not href.startswith('/'):
            continue
        id = int(re.findall('\d+', title)[0])
        logs.append((id, title, href))
        # print(ele.get('href'), ele.get_text())
    return logs


def write_file(contents, fname):
    print("write content to ", fname)
    with open('{0}.txt'.format(fname), 'w') as f:
        f.writelines(contents)


def downlod(book_url, bname):
    catalog = get_catalog(book_url)
    sorted(catalog)
    executor = ThreadPoolExecutor(max_workers=50)

    contents = []

    def get_page(info):
        print("dowload ", info[1])
        text = get_content(web_url + info[2])
        contents.append((info[0], info[1], text))

    future_to_page = {executor.submit(
        get_page, info): info for info in catalog}

    for future in as_completed(future_to_page):
        info = future_to_page[future]
        try:
            data = future.result()
        except Exception as exc:
            print('{0} generated an exception: {1}'.format(info, exc))
        else:
            print('{0} page is downalod'.format(info))

    contents.sort()

    book_contents = []
    for ele in contents:
        book_contents.append('\n')
        book_contents.append(ele[1])
        book_contents.append('\n')
        book_contents.append(ele[2])
        book_contents.append('\n')

    write_file(book_contents, bname)


if __name__ == "__main__":
    print(sys.argv[1], sys.argv[2])
    downlod(sys.argv[1], sys.argv[2])
