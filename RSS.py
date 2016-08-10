#!/usr/bin/python
import feedparser
import re


def main():
    test = feedparser.parse('https://teslan.thor.edu/post.atom')
    FeedTexts, FeedLinks, FeedTitles = [], [], []
    for i in range(0, len(test.entries)):
        FeedText = test.entries[i].description
        FeedText = re.sub("<.*?>", "", FeedText)
        FeedText = FeedText.strip()
        FeedTitles = FeedTitles + [test.entries[i].title]
        FeedTexts = FeedTexts + [FeedText]
        FeedLinks = FeedLinks + [test.entries[i].link]

    return FeedTitles,FeedLinks,FeedTexts

