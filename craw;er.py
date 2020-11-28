import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from time import sleep

current_chapter_number = 0

#章节URL迭代器
file_path = input(r'请输入保存图片文件的文件夹路径(比如C:\Users\Foksay\Desktop\都市鞋匠):')
chapter_first_number = int(input('请输入您要爬取的开始章节数：'))
chapter_last_number = int(input('请输入您要爬取的结束章节数：'))
sleep_time = float(input('为了防止IP被封或被请求重新定向，请输入每两次下载图片之间的休眠时间(建议0.1~0.5之间):'))
chapter_first_rank = chapter_first_number - 1
chapter_last_rank = chapter_last_number

url = list()
for i in range(chapter_first_rank, chapter_last_rank):
    url.append(r'https://www.hmba.vip/0_528/' + str(i))
urliter = iter(url)

current_chapter_number = chapter_first_number


#拿到URL的BeautifulSoup对象
def _bs(url):
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    response = requests.get(url, headers=headers)
    return BeautifulSoup(response.text, 'html.parser')


#拿到BeautifulSoup对象包含的图片链接的迭代器
def pic_url_iter(bso):
    return iter(x['src'] for x in iter(
        bso.findAll(alt="《都市鞋匠》漫画 第 %s 话" % current_chapter_number)))


#拿到PIC_URL的content对象（图片）
def get_img(pic_url):
    response = requests.get(pic_url)
    if response.status_code == 200:
        return response.content


#写入
for each_url in urliter:
    bsobject = _bs(each_url)
    pic_url_container = pic_url_iter(bsobject)
    page_pic_count = 1
    for i in pic_url_container:
        path = r'%s\%s-%s.jpg' % (file_path, current_chapter_number,
                                  page_pic_count)
        with open(path, 'wb') as file:
            file.write(get_img(i))
        page_pic_count += 1
        sleep(sleep_time)
    current_chapter_number += 1
