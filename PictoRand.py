import os, sys, wget, tweepy, json, random
import numpy as np
from tweepy import OAuthHandler
from tweepy import models as m
from PIL import Image
from io import BytesIO
    
def initTwitter():
    #REDACTED
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

def getImage():
    twitter = initTwitter()
    users = ['realDonaldTrump', 'NYCDailyPics','dpasi314','TractorPictures']
    tweets = twitter.user_timeline(screen_name=random.choice(users), count=500, include_rts=False,exclude_replies=True)
    media_files = []
    for status in tweets:
        media = status.entities.get('media', [])
        if(len(media) > 0):
            media_files.append(media[0]['media_url'])
    if(len(media_files) < 1):
        print("ERROR: Not enough images...")
        return -1
    return random.choice(media_files)

def clean_image_file():
    fileList = [f for f in  os.listdir("images/")]
    for f in fileList:
        print("Removing: ", f)
        os.remove(os.path.join("images/", f))

def getImageFromFile():
    fileList = [f for f in os.listdir("images/")]
    return random.choice(fileList)

def dwnld():
    clean_image_file()
    image = getImage()
    wget.download(image, out="images/")

def generateBitslices():
    image = Image.open("images/" + getImageFromFile())
    image = image.convert('1')
    image.save("images/" + getImageFromFile())

    bitmap = np.array(image).flatten().astype(int)
    bitslice = np.array_split(bitmap, 50);
    random.shuffle(bitslice)
    return bitslice

def randGen(bitslice, size=8, seed=2, mod=10):
    mainslice = bitslice[0]
    for item in bitslice[1:]:
        if(len(item) == len(mainslice)): mainslice = mainslice ^ item 
    
    hexslice = [mainslice[start:start+size] for start in range(0, len(mainslice), size)]
    random.shuffle(hexslice)
    string_list, num_list = [],[]

    for indiv in hexslice:
        tmp = ''.join([str(s) for s in indiv])
        string_list.append(tmp)
    
    for item in string_list:
        num_list.append(int(item, 2))
    return np.sum(num_list[::seed]) % mod


def main():
    dwnld() # Get all images
    nums = []
    bitslice = generateBitslices()
    for i in range(500):
        nums.append(randGen(bitslice, mod=500))
        if(i % 100): bitslice = generateBitslices()
    print()
    print(nums)
    return 0;
    
if __name__ == "__main__":
    main()


