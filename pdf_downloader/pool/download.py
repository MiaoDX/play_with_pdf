#-*- coding: utf-8 -*-
import json
import logging
import os
from pathlib import Path
# from urllib.request import urlopen, Request

import urllib
import httplib
from bs4 import BeautifulSoup
import re

from common import show_state 

# logging.basicConfig(filename='example.log',level=logging.DEBUG)
# logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('requests').setLevel(logging.CRITICAL)
logger = logging.getLogger(__name__)

# @show_state
def get_links(title):
    title = title.strip()
    print('This is get_links from name', title)
    pubTitle = ""
    pdfURL = ""

    params = urllib.urlencode({'q': title, 'num': 1})
    headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
    url = "/scholar"+"?"+params
    conn = httplib.HTTPConnection("scholar.google.com")
    conn.request("GET", url, "", headers)
    resp = conn.getresponse()

    if resp.status==200:
        html = resp.read().decode('ascii', 'ignore')
        soup = BeautifulSoup(html, "html.parser")
        for record in soup.findAll(True, {'class': 'gs_r'}):
            topPart = record.find('h3', {'class': 'gs_rt'})
            for part in topPart.a.contents:
                pubTitle += str(part.string)
            if pubTitle == None:
                continue

            pdfPart = record.find('div', {'class': 'gs_ggs gs_fl'})
            if pdfPart != None and re.search('\[PDF\]', str(pdfPart)) != None:
                pdfURL = pdfPart.a.get('href')

        pubTitle = pubTitle.replace(':', ' -')
        print "#", pubTitle
        if pubTitle != "" and pdfURL != "":
            pubTitle = re.sub(r'[/\\:*?"<>|]', '', pubTitle) # to avoid characters can not be filename in windows
            print('found', pubTitle, pdfURL)
            if(title[0] == '[' and title.find(']')>0 ): # this is what most references do
                pubTitle = title[:title.find(']')+1] + ' ' + pubTitle
        else:
            print "# not found."
    else:
        print "# connection error:", title, resp.status
    
    return pubTitle,pdfURL



# @show_state
def get_links_with_exception(title):
    title = title.strip()
    print('This is get_links from name', title)
    pubTitle = ""
    pdfURL = ""

    params = urllib.urlencode({'q': title, 'num': 1})
    headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
    url = "/scholar"+"?"+params
    conn = httplib.HTTPConnection("scholar.google.com")
    conn.request("GET", url, "", headers)
    resp = conn.getresponse()

    if resp.status==200:
        try:
            html = resp.read().decode('ascii', 'ignore')
            soup = BeautifulSoup(html, "html.parser")
            for record in soup.findAll(True, {'class': 'gs_r'}):
                topPart = record.find('h3', {'class': 'gs_rt'})
                for part in topPart.a.contents:
                    pubTitle += str(part.string)
                if pubTitle == None:
                    continue

                pdfPart = record.find('div', {'class': 'gs_ggs gs_fl'})
                if pdfPart != None and re.search('\[PDF\]', str(pdfPart)) != None:
                    pdfURL = pdfPart.a.get('href')

            pubTitle = pubTitle.replace(':', ' -')
            print "#", pubTitle
            if pubTitle != "" and pdfURL != "":
                pubTitle = re.sub(r'[/\\:*?"<>|]', '', pubTitle) # to avoid characters can not be filename in windows
                print('found', pubTitle, pdfURL)
                if(title[0] == '[' and title.find(']')>0 ): # this is what most references do
                    pubTitle = title[:title.find(']')+1] + ' ' + pubTitle
            else:
                print "# not found."
        except Exception:            
            logger.warn('Falid to find info of:' + title)
        finally:
            return pubTitle,pdfURL
    else:
        print "# connection error:", title, resp.status
    
    return pubTitle,pdfURL


    

# @show_state
def reporthook(block_read,block_size,total_size):
  if not block_read:
    print "connection opened";
    return
  if total_size<0:
    #unknown size
    print "read %d blocks (%dbytes)" %(block_read,block_read*block_size);
    # logger.warn('It seems wrong, since total_size cannot get, just skip this')
    # return
  else:
    amount_read=block_read*block_size;
    print 'Read %d blocks,or %d/%d, or %f' %(block_read,amount_read,total_size, (amount_read+0.0)/total_size);
  return

# @show_state
def download_link(directory, (pubTitle, link)):
    logger.info('Downloading %s', link)
    if(pubTitle == '' or link == ''):
        logger.warn('the link or pubTitle is just wrong!')
        return

    download_path = os.path.join(directory, pubTitle+'.pdf')
    # download_path = os.path.join(directory)
    print os.path.abspath(download_path)
    
    if os.path.isfile(download_path):
        print 'Alreay downloaded', pubTitle
        return
    try:
        urllib.urlretrieve(link,download_path,reporthook)
    except Exception:
        logger.warn('Wrong in download')
        return

# @show_state
def setup_download_dir(download_dir):
   download_dir = Path(download_dir)
   if not download_dir.exists():
       download_dir.mkdir()
   return download_dir

if __name__ == '__main__':

    logger.debug('Where are you?')

    dir =  setup_download_dir('download')

    print dir


    to_find = 'On the foundations of trust in networks of humans and computers'
    to_find = 'Attacking cryptographic schemes based on perturbation polynomials'
    to_find = '[1] Robust monocular SLAM in dynamic environments­'

    # pubTitle,pdfUrl =  get_links(to_find)

    pubTitle,pdfUrl = ('[157] 3d normal distributions transform occupancy maps','http://aass.oru.se/Research/mro/publications/2013/Saarinen_etal_2013-IJRR-Longterm_Occupancy_NDT_Mapping_and_Localization-TR.pdf')

    download_link('download', (pubTitle, pdfUrl))

