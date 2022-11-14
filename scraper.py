import sys
import json
import os
import requests
import re
import time
from bs4 import BeautifulSoup
from postClass import Post
    
def getPostno(div):
    postno = div['id']
    return postno[1:]
    
def getText(div):
    postText = div.find("p", {"itemprop": "text"})
    return postText.get_text()

def getTime(div):
    return div.find("span", {"class": "posttime"})['title']

def getSub(div):
    sub = div.find("span", {"class": "filetitle"})
    if sub != None:
        return sub.get_text()
    else:
        return ''

def scrape(board, page=0):
    page = requests.get(f'https://warosu.org/{board}/?task=page&page={str(page)}')
    soup = BeautifulSoup(page.content, 'html.parser')
    divs = soup.findAll("div", {"id" : re.compile("^p.")})
    brs = soup.findAll("br")
    for br in brs:
        br.replace_with('\n')

    postnos = list(map(getPostno, divs))
    texts = list(map(getText, divs))
    times = list(map(getTime, divs))
    subs = list(map(getSub, divs))
    
    zipped = zip(postnos, subs, texts, times)
    posts = [Post(num, sub, text, time) for num, sub, text, time in zipped]
    return posts

def dumpPost(post):
    if 'posts' not in os.listdir():
        os.mkdir('posts')
    postjson = post.postDict()
    with open(f'posts/{postjson["number"]}.json', 'w') as f:
        json.dump(postjson, f)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        board = sys.argv[1]
        i = 0
        while True:
            posts = scrape(board, i)
            for post in posts:
                dumpPost(post)
            i += 1
            time.sleep(1)
    else:
        print("Check out the README.md, dingus.")
        