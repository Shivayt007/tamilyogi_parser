## install before run
# apt-get -y install python3-pip
# apt-get install python3-bs4
# pip3 install requests
# pip3 install BeautifulSoup4 
# pip3 install clint
# pip3 install -U gazpacho


import os
import requests
from bs4 import BeautifulSoup
from gazpacho import get,Soup
from clint.textui import progress
import argparse
#from lxml import html
#import urllib


# default var
home_url= 'http://tamilyogi.fm/category/tamilyogi-full-movie-online/'

# get optional arguments
parser = argparse.ArgumentParser()
parser.add_argument('-path', type = str, default='/opt')
parser.add_argument('-number', type=int, default=1)
parser.add_argument('-tmp_path', type=str, default='/opt')
args = parser.parse_args()

number_of_videos = args.number
download_link_path = args.path
tmp_path = args.tmp_path + '\dawnloaded_list.txt'

# 1.Get file names from directory
def file_list():
    file_names=os.listdir(download_link_path)
    return file_names

# Split and get text between two substring
# TODO may be can use json format to split inseast the function
def ind(begining, end, contenent):
    idx_begining = contenent.index(begining)
    idx_end = contenent.index(end)

    res = ''
    for idx in range(idx_begining + len(begining) + 1, idx_end):
        res = res + contenent[idx]
    #print("The extracted string : \n" + res,"\n")
    return res

# Download the  video
def download_file(url, path, title):
    filename = path + "/" + title + ".mp4"
    r = requests.get(url, stream=True)
    with open(filename, 'wb') as f:
        total_length = r.headers.get('content-length')
        print("Downloading Movie:", title)
        #print(total_length, url, path, title)
        # for print a progress bar during the dawnload
        for chunk in progress.bar(r.iter_content(chunk_size=1024),\
            expected_size=(int(total_length)/1024) + 1): 
             if chunk: # filter out keep-alive new chunks
                f.write(chunk)    
                f.flush()
        print ("Downloading Done\n")
        f.close()

# Get request contenent
page = requests.get(home_url)

soup = BeautifulSoup(page.content, 'html.parser')
id_postcontent = soup.find_all(class_='postcontent')

s = 0
titles = []
postcontent_links = []
for id_postcontent in id_postcontent:
    s += 1
    href_line = id_postcontent.find(href=True)
    postcontent_links.append(href_line['href'])
    #titles.append(href_line['title']\
    #   .replace(' ', '_').split("(")[0][:-1])
    titles.append(href_line['title']\
        .replace('- ', '')\
        .replace(' ', '_')\
        .replace(')', '')\
        .replace('(', '')\
        .replace('_Watch_Online', ''))
    if s == number_of_videos:
        break

iframe_src_link = []
for links in postcontent_links:
    page1 = requests.get(links)
    soup1 = BeautifulSoup(page1.content, 'html.parser')
    entry= soup1.find(class_='entry')
    iframe_link=entry.iframe.attrs['src']
    iframe_src_link.append(iframe_link)
    #print("link len: ", len(iframe_src_link))


video_links = []
for link in iframe_src_link:
    #print("ifrrame: ", link)
    soup2 = Soup.get(link)
    script_contenent = soup2.find('script', attrs={'type':'text/javascript'})

    in_sting = ""
    for i in script_contenent:
        in_sting += str(i)
    
    # get the begining and the end value to parse the iframe contenent
    begining = "sources: ["
    end = "}],"
    #print("out script link:", ind(begining, end, in_sting))
    script_link_contenent = ind(begining, end, in_sting)

    begining = "{file:"
    end = ",label"
    video_links.append(ind(begining, end, script_link_contenent)[:-1])
    #print(f"video_links: {ind(begining, end, script_link_contenent)[:-1]}\n")
    
f = open(tmp_path,'a+')
ignore_list=[]
for line in open(tmp_path,'r').readlines():
    ignore_list.append(line.strip())

# if one of the movie parsed from url alredy exists in local dawnload path,
# this movie will not be dawnloaded
names =  []
ignored_names =  []
zip_object = zip(titles, video_links)
for title, video_link in zip_object:
    file_name_list = file_list()
    full_title = title + ".mp4"
    if (full_title in file_list()) or (full_title in ignore_list):
        ignored_names.append(title)
        continue
    names.append(title)
    # download_file(video_link, download_link_path, title)
    with open(tmp_path,'a') as file:
        file.write(full_title + '\n')

# to have a log during the each execution from cron
print('Default Link Length: ', len(titles))
if len(names) == 0:
    print("No movie dawnloaded during this execution (Alredy Exists)\n")
else:
    print(f"Number of movie dawnloaded during this execution: {len(names)}\n")
    for i in names:
        print("Downloaded Movie:", i)

for i in ignored_names:
    print("Ignored Movie:", i)
