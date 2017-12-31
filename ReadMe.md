# PictoRand

## An Overview
PictoRand is a way to generate random numbers based on pictures taken from twitter.
PictoRand will select a picture from the first 50 tweets taken from the following hashtags.
- MAGA
- nofilter
- art
- weather

PictoRand will take a picture found on twitter, and convert it to black and white. It will then take each of those pixels, associated as a binary number (0, 1) and create a flattened bitmap. 
A binary string of the current time, expanaded on itself in order to meet size requirements is also created. 
The time string, which is the main slice, will be XORed over 1,000 similarly sized slices out of the flattened bitmap

## The Inspiration
While on a quest to search for something truly random, PictoRand was meant to select pictures from twitter to use the thoughts from humans as something truly random. In an attempt to re-create the lava lamp wall that CloudFlare uses to create unique hashes based on pictures.

## The Proof is in the Numbers
See the math work out here: www.dantepasionek.com/stats.html
I was able to prove that my random number generator and Python's random number generator are not actually statistically different.

