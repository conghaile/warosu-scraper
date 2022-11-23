import sys
import json
import os
import requests
import re
import time
from bs4 import BeautifulSoup
from pymongo import MongoClient
import postgres
from postClass import Post
    
def getPostno(div):
    postno = div['id']
    return postno[1:]
    
def getText(div):
    postText = div.find("p", {"itemprop": "text"})
    text = postText.get_text()
    textlist = text.split("##")
    textlist = [sen for sen in textlist if sen != '']
    return textlist

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
        br.replace_with('##')

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

def flat(board):
    i = 0
    while True:
        posts = scrape(board, i)
        for post in posts:
            dumpPost(post)
        i += 1
        time.sleep(1)

def postgresDb(board, table):
    i = 0
    while True:
        posts = scrape(board, i)
        for post in posts:
            postgres.create(post, table)
        i += 1
        time.sleep(1)

def mongoDump(board, port=27017):
    client = MongoClient("mongodb://localhost:" + str(port))
    warosu = client["warosu"]
    posts = warosu["posts"]
    i = 0
    while True:
        scrapedPosts = scrape(board, i)
        for post in scrapedPosts:
            postDict = post.postDict()
            x = posts.insert_one(postDict)
            print(x.inserted_id)
        time.sleep(1)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        board = sys.argv[1]
        if sys.argv[2] == "flat":
            flat(board)
        elif sys.argv[2] == "postgres":
            if len(sys.argv) > 3:
                table = sys.argv[3]
                postgresDb(board, sys.argv[3])
            else:
                table = 'Warosu'
                postgres.verifyTable()
                postgresDb(board, table)
        elif sys.argv[2] == "mongo":
            if len(sys.argv) > 3:
                port = int(sys.argv[3])
                mongoDump(board, port)
            else:
                mongoDump(board)


    else:
        print('-' * 25, "Warosu Scraper", '-' * 25)
        print('\nFor more information, read the README.md')
        print('\nHere are the following flags:')
        print('\nflat:\n')
        string = 'Dumps posts into ./posts directory as raw .json files'
        print(string.rjust(64))
        print()
        print('\npostgres:\n')
        string = 'Dumps posts into Postgres database running at localhost:5432'
        print(string.rjust(64))
        string = 'Requires database.ini, see README.md for details'
        print(string.rjust(64))
        print('\nmongo:\n')
        string = 'Dumps posts into local mongodb instance runing at localhost:27017'
        print(string.rjust(64))
        string = "Creates database 'warosu', collection 'posts' automatically"
        print(string.rjust(64))
        string = "Alternative port may be specified"
        print(string.rjust(64))