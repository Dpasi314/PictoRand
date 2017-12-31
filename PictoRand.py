import os, sys, wget, tweepy, json, datetime
import numpy as np
from tweepy import OAuthHandler
from tweepy import models as m
from PIL import Image
from io import BytesIO
    
def initTwitter():
    #[REDACTED - Twitter Authentication]
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


def getImage(offset=0):
    now = datetime.datetime.now()
    twitter = initTwitter()
    tags = ['#maga','#art','#weather', '#nofilter']
    #tweets = twitter.user_timeline(screen_name=random.choice(users), count=500, include_rts=False,exclude_replies=False)
    tweets = tweepy.Cursor(twitter.search, q=(tags[now.second % len(tags)])).items(50)
    media_files = []
    for status in tweets:
        media = status.entities.get('media', [])
        if(len(media) > 0):
            media_files.append(media[0]['media_url'])
    if(len(media_files) < 1):
        print("ERROR: Not enough images...")
        return -1
    if(offset > 499): offset=499
    return media_files

def clean_image_file():
    fileList = [f for f in  os.listdir("images/")]
    for f in fileList:
        print("Removing: ", f)
        os.remove(os.path.join("images/", f))

def getImageFromFile(offset=0):
    now = datetime.datetime.now()
    fileList = [f for f in os.listdir("images/")]
    return fileList[now.microsecond % len(fileList)]

def dwnld():
    clean_image_file()
    image = getImage()
    for i in image:
        wget.download(i, out="images/")

def generateBitslices(offset=0):
    image = Image.open("images/" + getImageFromFile())
    image = image.convert('1')

    bitmap = np.array(image).flatten().astype(int)
    bitslice = np.array_split(bitmap, 1000);
    return bitslice

def randGen(bitslice, size=8, seed=2, mod=10, offset=0):
    now = bin(int(datetime.datetime.now().strftime("%y%m%d%H%M%S%f%y%m%d%H%M%S%f%y%m%d%H%M%S%f%y%m%d%H%M%S%f")))
    now = ''.join(str(now).strip("0b"))
    nowBin = []
    for item in now: nowBin.append(item)
    nowBin = np.array(nowBin).flatten().astype(int)

    mainslice = nowBin
    for item in bitslice: 
        if(len(item) == len(mainslice)): mainslice = mainslice ^ item 

    hexslice = [mainslice[start:start+size] for start in range(0, len(mainslice), size)]
    string_list, num_list = [],[]


    for indiv in hexslice:
        tmp = ''.join([str(s) for s in indiv])
        string_list.append(tmp)
    
    for item in string_list:
        num_list.append(int(item, 2))

    return np.sum(num_list[::seed]) % mod


def main():
    dwnld() # Get all images
    sys.setrecursionlimit(1000)
    bitslice = generateBitslices()
    n = randGen(bitslice, mod=100)
    if(False):
        nums = []
        for i in range(1000):
            nums.append(randGen(bitslice, mod=500))
            if(i % 200):
                bitslice = generateBitslices()
        print(nums)
    print("\n\nRand Number Generated: ",n )
    return 0;
    
if __name__ == "__main__":
    main()


