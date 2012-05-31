#!/usr/bin/python

from urlparse import urljoin
import urllib2
import os

BASE_URL = 'http://www.dialabc.com/i/cache/dtmfgen/'
FORMATS = {
    'wav': {
        '80': 'wavpcm8.300',
        '160': 'wavpcm16.300',
        '441': 'wavpcm44.300',
    }
}

if __name__ == '__main__':
    
    if not os.path.exists('dtmf'):
        os.mkdir('dtmf')
    
    for (ext, formats) in FORMATS.iteritems():
        for (format, sub_url) in formats.iteritems():
            for i in range(10):
                url = '%s/%d.%s' % (sub_url, i, ext)
                url = urljoin(BASE_URL, url)
                localpath = '%d_%s.%s' % (i, format, ext)
                localpath = os.path.join('dtmf', localpath)
                
                print 'Downloading %s to %s' % (url, localpath)
                
                try:
                    f = urllib2.urlopen(url)
                    with open(localpath, 'w') as lf:
                        lf.write(f.read())
                    
                    print 'Download complete.'
                except Exception as e:
                    print 'Download failed!'
                    print e
                