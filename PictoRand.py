import os, wget, tweepy, json, datetime
import numpy as np
from tweepy import OAuthHandler
from tweepy import models as m
from PIL import Image
DEBUG = False
def initTwitter():
    @classmethod
    def parse(cls, api, raw):
        status = cls.first_parse(api, raw)
        setattr(status, 'json', json.dumps(raw))
        return status
    m.Status.first_parse = tweepy.models.Status.parse
    m.Status.parse = parse

    m.User.first_parse = tweepy.models.User.parse
    m.User.parse = parse

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth)
    return api

def getNormalizedRand(offset):
    now = datetime.datetime.now()
    return now.microsecond % offset

def getImage():
    twitter = initTwitter()
    tags = ['#maga','#art','#weather', '#nofilter']
    tweets = tweepy.Cursor(twitter.search, q=(tags[getNormalizedRand(len(tags))])).items(25)
    media_files = []
    for status in tweets:
        media = status.entities.get('media', [])
        if(len(media) > 0):
            media_files.append(media[0]['media_url'])
    if(len(media_files) < 1):
        print("ERROR: Not enough images...")
        return -1
    return media_files

def clean_image_file():
    fileList = [f for f in  os.listdir("images/")]
    for f in fileList:
        if(DEBUG): print("Removing: ", f)
        os.remove(os.path.join("images/", f))

def getImageFromFile():
    now = datetime.datetime.now()
    fileList = [f for f in os.listdir("images/")]
    return fileList[getNormalizedRand(len(fileList))]

def dwnld():
    clean_image_file()
    image = getImage()
    for i in image:
        if(DEBUG): print("\nDownloading:{}".format(i) )
        wget.download(i, out="images/")

def generateBitslices(offset=0):
    image = Image.open("images/" + getImageFromFile()).convert('1')

    bitmap = np.array(image).flatten().astype(int)
    bitslice = np.array_split(bitmap, 1000);
    return bitslice

def randGen(bitslice, size=8, seed=2, mod=10, offset=0):
    time_format =''.join(["%y%H%f%S%M%y%f" for s in range(50)])
    now = bin(int(datetime.datetime.now().strftime(time_format)))
    now = ''.join(str(now).strip("0b"))
    nowBin = []
    for item in now: nowBin.append(item)
    nowBin = np.array(nowBin).flatten().astype(int)

    mainslice = nowBin
    for item in bitslice: 
        if(len(item) == len(mainslice)): mainslice = mainslice ^ item 

    hexslice = [mainslice[start:start+size] for start in range(0, len(mainslice), size)]
    num_list = []

    for indiv in hexslice:
        tmp = ''.join([str(s) for s in indiv])
        num_list.append(int(tmp, 2))
    
    return (np.sum(num_list[::seed]) % mod) + 1


def main():
    dwnld() # Get all images
    n = randGen(generateBitslices(), mod=500)
    print("\n---PictoRang Generation ---\nGenerated: {}".format(n))
    clean_image_file()
    return 0;
    
if __name__ == "__main__":
    main()
