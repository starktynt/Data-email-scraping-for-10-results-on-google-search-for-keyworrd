# -*- coding: utf-8 -*-


import pandas as pd 
df = pd.read_excel("source.xlsx")

from urllib.error import HTTPError
import urllib

ass = []
for i in df:
  ass.append(i)

var = list(df[ass[0]])

no_scrape = list(df[ass[1]])

import requests, lxml
from bs4 import BeautifulSoup

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3538.102 Safari/537.36 Edge/18.19582"
}
noval = no_scrape
def get_link(varr):
  params = {
    'q': varr+" contactos",  # search query
    'hl': 'en',                # language
    'num': '17'               # number of results
  }


  html = requests.get('https://www.google.pt/search', headers=headers, params=params)
  soup = BeautifulSoup(html.text, 'lxml')
  link_lis = []
  
  # container with all needed data
  for result in soup.select('.tF2Cxc'):
    link = result.select_one('.yuRUbf a')['href']
    domain_name = ''.join(re.findall(r'^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/?\n]+)', link))
    count = 0
    for yx in noval:
      
      if domain_name in str(yx) :
        count +=1
    if count==0:
      if "pdf" in link:
        x=0
      else:
        link_lis.append(link)

    #displayed_link = result.select_one('.TbwUpd.NJjxre').text

    
    #domain_name = ''.join(re.findall(r'^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/?\n]+)', link))

  print(link_lis[:10])
    #print(displayed_link)
    #print(domain_name)
    #print('---------------')

  return link_lis[:10]

from bs4 import BeautifulSoup
from requests import get
import re

def mail_id(link):
  ans = []
  req = urllib.request.Request(link,headers={
        'User-Agent':"PostmanRuntime/7.6.0"
    })
  try:
      html = urllib.request.urlopen(req)
  except HTTPError as e:
      content = e.read()
  soup = BeautifulSoup(html)
 

  exp = re.compile(r"(?:.*?='(.*?)')")
  # Find any element with the mail icon
  for icon in soup.findAll("i", {"class": "icon-mail"}):
      # the 'a' element doesn't exist, there is a script tag instead
      script = icon.next_sibling
      # the script tag builds a long array of single characters- lets gra
      chars = exp.findall(script.text)
      output = []
      # the javascript array is iterated backwards
      for char in reversed(list(chars)):
          # many characters use their ascii representation instead of simple text
          if char.startswith("|"):
              output.append(chr(int(char[1:])))
          else:
              output.append(char)
      # putting the array back together gets us an `a` element
      link = BeautifulSoup("".join(output))
      email = link.findAll("a")[0]["href"][8:]
      # the email is the part of the href after `mailto: `
      print(email)
      ans.extend(email)

  mailtos = soup.select('a[href^=mailto]')
  for i in mailtos:
    pattern = '\".*\"'
    s = re.findall(pattern,str(mailtos[0]))
    s = re.sub('\"',"" ,s[0])
    s = re.sub("mailto:","",s)
    match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', s)
    try:
      xxx = match.group(0)
      
    except:
      xxx=s
    
    ans.append(xxx)


  return ans

import re
def mail_find(line):
  #line = "should we use regex more often? let me know at  321dsasdsa@dasdsa.com.lol"
  match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', line)
  try:
    xxx = match.group(0)
    return xxx
  except:
    return ""

def find_mail(link , xxxx):

  domain_name = ''.join(re.findall(r'^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/?\n]+)', link))
  #print(domain_name)
  extra=[]
  req = urllib.request.Request(link,headers={
        'User-Agent':"PostmanRuntime/7.6.0"
    })
  try:
      html = urllib.request.urlopen(req)
  except HTTPError as e:
      content = e.read()

  res_list = []
  html_list = []

  lis=[]
  for line in html:
      
      html_list.append(line) 

  try:
    req = urllib.request.Request(link,headers={
          'User-Agent':"PostmanRuntime/7.6.0"
    })
    try:
        html = urllib.request.urlopen(req)
    except HTTPError as e:
        content = e.read()


    soup = BeautifulSoup(html)
      #soup = BeautifulSoup(content, "lxml")

    exp = re.compile(r"(?:.*?='(.*?)')")
    # Find any element with the mail icon
    for icon in soup.findAll("i", {"class": "icon-mail"}):
        # the 'a' element doesn't exist, there is a script tag instead
        script = icon.next_sibling
        # the script tag builds a long array of single characters- lets gra
        chars = exp.findall(script.text)
        output = []
        # the javascript array is iterated backwards
        for char in reversed(list(chars)):
            # many characters use their ascii representation instead of simple text
            if char.startswith("|"):
                output.append(chr(int(char[1:])))
            else:
                output.append(char)
        # putting the array back together gets us an `a` element
        link = BeautifulSoup("".join(output))
        email = link.findAll("a")[0]["href"][8:]
        # the email is the part of the href after `mailto: `
        print(email)
        lis.extend(email)
  except :
    x = 0


  try:
    for line in html_list:
      if b'@' in line:
        #line = line.replace(b'<img id="video_jacket_img', b'').replace(b'</td>', b'')
        try:
          line = line.strip().decode()
        except:
          line = line.decode("latin-1")
        line = mail_find(line)
        
        if line!="":
          lis.append(line)

    if xxxx == False :

      for line in html_list:
        if bytes(domain_name, 'utf-8') in line:
          #line = line.replace(b'<img id="video_jacket_img', b'').replace(b'</td>', b'')
          
          try:
            line = line.strip().decode()
          except:
            line = line.decode("latin-1")
          line = re.search("(?P<url>https?://[^\s]+)", line).group("url")
          line = re.sub("\".*" , "" , line)
          #line = mail_find(line)
          #print("------",line)
          extra.append(line)


  except:
    x=0
  if len(extra) >=5:
    extra = extra[:5]
  return lis , extra

data={
    "name":[],
    "url_1":[],
    "url_2":[],
    "url_3":[],
    "url_4":[],
    "url_5":[],
    "url_6":[],
    "url_7":[],
    "url_8":[],
    "url_9":[],
    "url_10":[]

}

from tqdm.notebook import tqdm_notebook
import time




for i in tqdm_notebook(range(len(var)):
  try:
    
    linkss = get_link(var[i])
    data["name"].append(var[i])
    data["name"].append("emails found")
    for ids in range(len(linkss)) :
      stri = "url_"+str(ids+1)
      try :
        emailss ,extras = find_mail(linkss[ids] , False)
        if len(extras)!=0:
          for j in extras[:2]:
            try:
              extra_mail , xyz = find_mail(j , True)
              emailss.extend(extra_mail)
            except:
              continue

        data[stri].append(linkss[ids])
        data[stri].append(emailss)
      except:
        data[stri].append(linkss[ids])
        data[stri].append("NA")

  except :
    continue

df1 = pd.DataFrame(data)

df1.to_excel("extraction.xlsx")



