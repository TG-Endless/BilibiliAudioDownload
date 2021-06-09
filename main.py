import sys

import requests
import urllib
import time

def printA(s):
    sys.stdout.write(s + '\n')

def getCidAndTitle(bvid, p=1):
    url = 'https://api.bilibili.com/x/web-interface/view?bvid=' + bvid
    data = requests.get(url).json()['data']
    title = data['title']
    cid = data['pages'][p - 1]['cid']
    return str(cid), title


def getInformation(bvList):
    infoList = []
    for bvid in bvList:
        item = []
        bvid = bvid[-12:]
        if len(bvid) == 12:
            cid, title = getCidAndTitle(bvid)
            item.append(bvid)
        else:
            assert len(bvid) == 12
        item.append(cid)
        item.append(title)
        infoList.append(item)

    return infoList


def getAudio(item, folder=''):
    bvid, cid, title = item[0], item[1], item[2]
    try:
        baseUrl = 'https://api.bilibili.com/x/player/playurl?fnval=16&'
        st = time.time()
        printA('Start download: ' + title)
        url = baseUrl + 'bvid=' + bvid + '&cid=' + cid

        audioUrl = requests.get(url).json()['data']['dash']['audio'][0]['baseUrl']

        opener = urllib.request.build_opener()
        opener.addheaders = [
            ('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0) Gecko/20100101 Firefox/56.0'),
            ('Accept', '*/*'),
            ('Accept-Language', 'en-US,en;q=0.5'),
            ('Accept-Encoding', 'gzip, deflate, br'),
            ('Range', 'bytes=0-'),
            ('Referer', 'https://api.bilibili.com/x/web-interface/view?bvid=' + bvid),  # 注意修改referer,必须要加的!
            ('Origin', 'https://www.bilibili.com'),
            ('Connection', 'keep-alive'),
        ]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(url=audioUrl, filename=folder + '/' + title + '.mp3')
        ed = time.time()
        printA(str(round(ed - st, 2)) + ' seconds download finish: ' + title)
        time.sleep(1)
    except Exception as e:
        printA(e.__str__())
        printA("Error: 无法下载：" + title)


if __name__ == '__main__':
    folder = ''
    if sys.argv[1] == 'c':
        folder = '中文'
    elif sys.argv[1] == 'j':
        folder = '日文'
    elif sys.argv[1] == 'p':
        folder = '钢琴曲'
    else:
        folder = sys.argv[1]

    print("Download to: " + folder)
    BVList = sys.argv[2:]
    songs = getInformation(BVList)
    for item in songs:
        try:
            getAudio(item, folder)
        except:
            print("下载【%s】失败！", item[2])
