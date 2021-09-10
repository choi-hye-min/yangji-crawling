import requests
import re
import pymysql
from bs4 import BeautifulSoup
import configparser
import db
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import mailTemplate

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')
config.sections()

# 크롤링 키워드
SEARCH_KEY_WORDS = ['양지병원', 'H+양지병원', 'H PLUS 양지병원']
GMAIL_APP_CONFIG = {
    'fromMail': config['gmail']['formMail'],
    'password': config['gmail']['password']
}
RECEIVER_MAIL = config['gmail']['receiverMail']
CRAWLING_DATAS = []


def getBeautifulSoup(text):
    return BeautifulSoup(text, 'html.parser')


def keywordMatching(word):
    return word in SEARCH_KEY_WORDS


def naverMobileCrawling(url):
    response = requests.get(url, headers={
        'cookie': 'MM_NEW=1;MM_FS=fzoom;MM_v3_contents=NEWS%3BSPORTS%3BENT%3BDATA%3BSHOPPING%3BMYFEED%3BHEALTH;MM_TAB=CONTENTS;MM_MF_TAB_SVC=DISCOVER_RECOMMEND;MM_PANEL=HEALTH'})
    soup = getBeautifulSoup(response.text)

    healthContent = soup.select_one(
        '#mflick > div > div:nth-child(1) > div > div > div.grid1_wrap.brick-house > div:nth-child(1) > div:nth-child(1) > div')

    healthContentItems = getBeautifulSoup(healthContent.prettify()).select('li')
    # 모바일 4컷 컨텐츠 section
    for item in healthContentItems:
        itemContent = getBeautifulSoup(item.prettify()).select_one('li.cc_citem')
        if itemContent == None:
            continue

        itemBoxContent = getBeautifulSoup(itemContent.prettify())
        title = str.strip(itemBoxContent.select_one('div.cc_ct').getText())
        source = str.strip(itemBoxContent.select_one('span.aname').getText())
        link = itemBoxContent.select_one('a.cc_author_a[href]')['href']

        keywordMatchSave('mobile/post', link, source, title)

    # 모바일 건강TV
    naverMobileHealthTvCrawling(soup.select('.cc_citem a[data-video-launch]'))


def naverDesktopCrawling(url):
    response = requests.get(url)
    soup = getBeautifulSoup(response.text)

    # 일반 게시물 section
    for postItem in soup.select('a.theme_info'):
        post = getBeautifulSoup(postItem.prettify())

        title = str.strip(post.select_one('string.title,.elss').getText())
        source = str.strip(post.select_one('span.source_inner').getText())
        link = postItem['href']

        keywordMatchSave('pc/post', link, source, title)

    # 비디오 영상 section
    for videoItem in soup.select('a.media_area'):
        videoPost = getBeautifulSoup(videoItem.prettify())

        title = str.strip(videoPost.select_one('strong.title').getText())
        source = str.strip(videoPost.select_one('span.source_inner').getText())
        link = videoItem['href']

        keywordMatchSave('pc/video', link, source, title)


# 모바일 건강TV
def naverMobileHealthTvCrawling(healthTvContent):
    for post in healthTvContent:
        parentPost = post.parent
        title = parentPost.select_one('.cc_ct').text
        source = parentPost.select_one('.aname').text
        link = parentPost.select_one('a')['href']

        keywordMatchSave('mobile/healthTv', link, source, title)


def keywordMatchSave(type, link, source, title):
    if keywordMatching(source):
        CRAWLING_DATAS.append([type, title, source, link])
        print(f"[{source}] {title} - {link}")


def sendMail(bodyMsg):
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()  # say Hello
    smtp.starttls()  # TLS 사용시 필요
    smtp.login(GMAIL_APP_CONFIG.get('fromMail'), GMAIL_APP_CONFIG.get('password'))

    msg = MIMEText(bodyMsg, 'html')
    msg['Subject'] = '네이버 양지병원 키워드 알림'
    msg['To'] = RECEIVER_MAIL
    msg['From'] = formataddr(('네이버 양지병원 키워드 알림', GMAIL_APP_CONFIG.get('fromMail')))
    smtp.sendmail(msg['From'], msg['To'], msg.as_string())
    smtp.quit()
    print("MAIL SEND!")


if __name__ == '__main__':
    # PC 건강 탭 크롤링
    naverDesktopCrawling('https://www.naver.com/nvhaproxy/v1/panels/HEALTH/html')

    # 모바일 상단영역 크롤링
    naverMobileCrawling('https://m.naver.com/')

    # 메일발송
    sendMail(mailTemplate.createMessage(CRAWLING_DATAS))
