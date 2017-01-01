# -*- coding: utf-8 -*-
"""
File:           translator.py
Description:    Using online Bing dictonry to translate from English to Chinese
                and vice verse
Author:         esc.chao@gmail.com
License:        Apache 2.0
"""
import json
import requests
import urllib
import sys
from xml.etree import ElementTree
from HTMLParser import HTMLParser

class ResultParser(HTMLParser):
    """
        Html parser class is used to parse translation result.
    """

    def __init__(self):
        HTMLParser.__init__(self)
        self.result = None

    def handle_starttag(self, tag, attrs):
        """Only hanlde tag like: <meta name='description' ..."""

        if (tag != 'meta'):
            return

        attrDict = dict(attrs)
        if ((not attrDict.has_key('name')) or
            attrDict.get('name') != 'description'):
            return

        self.result = attrDict.get('content').encode('utf-8')

class TranslateException(Exception):
    pass

class Translator:
    """
        Tranlator class is used to translate text from bing dictionry.
    """

    commaChar = u'，'.encode('utf-8')
    semicolonChar = u'；'.encode('utf-8')
    colonChar = u'：'.encode('utf-8')
    phoneticTag = u'美['.encode('utf-8')
    pinYinTag = u'拼音['.encode('utf-8')
    webTag = u'网络释义:'.encode('utf-8')
    bingDictUrl = 'http://cn.bing.com/dict?q={}'

    def __init__(self):
        self.result = {'phonetic':None, 'meaning':None, 'web':None}
        self.parser = ResultParser()

    def translateE2C(self, text):
        """
            Tranlate text from English to Chinese
        """

        queryUrl = self.bingDictUrl.format(text)
        self.result['phonetic'] = None
        self.result['meaning'] = None
        self.result['web'] = None

        try:
            response = requests.get(queryUrl)
            self.parser.feed(response.text)

            #print("Result: {}".format(self.parser.result))
            self.getMeaning(
                self.getWebMeaning(self.webTag,
                                   self.getPhonetic(
                                       self.phoneticTag,
                                       self.preprocess(self.parser.result))
                                   )
            )

        except OSError as e:
            print ("Can't translate: {0}".format(e))

        return self

    def translateC2E(self, text):
        """
            Tranlate text from Chinese to English
        """

        queryUrl = self.bingDictUrl.format(text)
        self.result['phonetic'] = None
        self.result['meaning'] = None
        self.result['web'] = None

        try:
            response = requests.get(queryUrl)
            self.parser.feed(response.text)

            #print("Result: {}".format(self.parser.result))
            self.getMeaning(
                self.getWebMeaning(self.webTag,
                                   self.getPhonetic(
                                       self.pinYinTag,
                                       self.preprocess(self.parser.result))
                                   )
            )

        except OSError as e:
            print ("Can't translate: {0}".format(e))

        return self

    def preprocess(self, data):
        """
            Prepocess result, locate the real start position, replace unicode
            delimiter with ascii.
        """
        if (data == None or len(data) < 1):
            return data

        tag = u'释义，'.encode('utf-8')
        start = data.find(tag)
        if (start >= 0):
            data = data[start + len(tag):]
        else:
            return None

        return data.replace(self.commaChar, ',') \
                   .replace(self.semicolonChar, ';') \
                   .replace(self.colonChar, ':')

    def getPhonetic(self, tag, data):
        """
            Extract phonetic symbol from result
        """
        if (data == None):
            return data

        length = len(data)
        if (length < 1):
            return data

        start = data.find(tag)
        if (start < 0):
            return data

        endPhonetic = u']'.encode('utf-8')
        end = data.find(endPhonetic, start)
        if (end < 0):
            return None

        end += len(endPhonetic)
        t = data.find(endPhonetic, end)
        if (t > end):
            end = t + len(endPhonetic)

        self.result['phonetic'] = data[start:end]

        for i in range(end, length):
            ch = data[i]
            if (ch != ' ' and ch != ',' and ch != ':' and ch != ';'):
                end = i
                break

        return data[end:].strip()

    def getWebMeaning(self, tag, data):
        """
            Extract web meaning from result
        """
        if (data == None or len(data) < 1):
            return data

        start = data.find(tag)
        if (start < 0):
            return data

        self.result['web'] = data[start:].strip('; ')
        return data[:start]

    def getMeaning(self, data):
        """
            Extract meaning from result
        """
        if (data == None):
            return

        end = len(data)
        if (end < 1):
            return

        start = 0
        start = data.rfind('.')
        meanings = []
        while (start >= 0):
            t = data.rfind(' ', 0, start)
            if (t >= 0):
                meanings.insert(0, data[t + 1:end].strip('; '))
                end = t
                start = data.rfind('.', 0, end)
            else:
                break

        if (end > 0):
            meanings.insert(0, data[:end].strip('; '))

        if (len(meanings) > 0):
            self.result['meaning'] = meanings

    def printResult(self):
        print("Phonetic: {}".format(self.result['phonetic']))
        if (self.result['meaning'] != None):
            print("Meaning:  {}".format('\n'.join(self.result['meaning'])))
        print("Web:      {}".format(self.result['web']))

if __name__ == "__main__":
    translator = Translator()
    translator.translateE2C('welcome to home').printResult()
    translator.translateE2C('smug').printResult()
    translator.translateC2E('自负').printResult()

