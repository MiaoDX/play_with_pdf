#-*- coding: utf-8 -*-

import logging
import os
from functools import partial
from multiprocessing import Pool
from time import time

from download import setup_download_dir, get_links, get_links_with_exception, download_link


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('requests').setLevel(logging.CRITICAL)
logger = logging.getLogger(__name__)


from common import show_state



@show_state
def get_all_names_of_multi_lines(fileName): # multiline is what most reference are
    all_lines = []

    with open(fileName, 'r') as f:
        all = f.readlines();
    
    real_line_info = ''
    for line in all:
        line = line.strip()
        if (line == '' or line[0] == '[') and real_line_info!='': # this is when a seperate line happens, when line='\n' after strip line==''
            all_lines.append(real_line_info)
            real_line_info = ''
        line = line.replace('\n', '')
        real_line_info += line

    if real_line_info!='': # capture the last one
        all_lines.append(real_line_info)
    return all_lines

@show_state
def get_all_names_of_multi_lines_and_just_use_first_line(fileName): # multiline is what most reference are
    all_lines = []

    with open(fileName, 'r') as f:
        all = f.readlines();
    
    real_line_info = ''
    for line in all:
        line = line.strip()
        if line != '' and line[0] == '[':
            all_lines.append(line)

    return all_lines

@show_state
def get_all_names(fileName):
    all_lines = []

    with open(fileName, 'r') as f:
        all = f.readlines();

    for line in all:
        line = line.replace('\n', '')
        all_lines.append(line)
    
    return all_lines




@show_state
def put_links_and_names_to_file(to_save_file_name, links_and_names):
    with open(to_save_file_name, 'a') as f:
        for line in links_and_names:
            f.write(line[0] + '\n' + line[1] + '\n') # '^' is not so likely in a name

@show_state
def get_links_and_names_from_file(links_and_names_file_name):
    links_and_names = []

    with open(links_and_names_file_name, 'r') as f:
        all = f.readlines();

    for i in range(len(all)):
        line = all[i]
        line = line.strip()

        if line == '':
            continue

        if line[0] == '[':
            name = line
            link = all[i+1].strip()
            links_and_names.append((name,link))

    return links_and_names



@show_state
def get_links_and_names(names):
    for name in names:
        print(name)

    pool = Pool(processes = 2)
    # links_and_names = pool.map(get_links, names)
    links_and_names = pool.map(get_links_with_exception, names)
    pool.close()
    pool.join()
    return links_and_names

def download_all_from_links_names_sequence(dowload_dir, links_and_names):
    ts = time()

    download_dir = setup_download_dir(dowload_dir)
    
    for link_and_name in links_and_names:
        download_link('download', link_and_name)
        print('Took {}s'.format(time() - ts)) 
        ts = time()

def download_all_from_links_names(dowload_dir, links_and_names):
    ts = time()

    download_dir = setup_download_dir(dowload_dir)
    
    download = partial(download_link, 'download')

    pool = Pool(processes = 4)

    pool.map(download, links_and_names)
    
    pool.close()
    pool.join()

    print('Took {}s'.format(time() - ts))



def get_all_links_and_names_and_save_to_file():
    base = 'H:/practice/play_with_pdf/pdf_downloader/pool/'

    to_download_file_name = base+'test.txt'
    to_save_file_name = base+'save.txt'


    # allNames = get_all_names(to_download_file_name)
    # allNames = get_all_names_of_multi_lines(to_download_file_name)    
    allNames = get_all_names_of_multi_lines_and_just_use_first_line(to_download_file_name)    


    links_and_names = get_links_and_names(allNames)

    put_links_and_names_to_file(to_save_file_name, links_and_names)



def just_download_all():
    base = 'H:/practice/play_with_pdf/pdf_downloader/pool/'

    to_save_file_name = base+'save.txt'

    links_and_names = get_links_and_names_from_file(to_save_file_name)
    print len(links_and_names)


    start = 100
    num = 40
    
    to_download_links_and_names = links_and_names[start:start+num]

    download_all_from_links_names('download', to_download_links_and_names)
    # download_all_from_links_names_sequence('download', to_download_links_and_names)
    




if __name__ == '__main__':
    # get_all_links_and_names_and_save_to_file()
    just_download_all()