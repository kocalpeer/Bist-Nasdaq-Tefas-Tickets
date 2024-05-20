import json
import numpy as np
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def takebist100list():
    url = 'https://www.kap.org.tr/tr/Endeksler'
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text,'lxml')
    body = soup.find_all('div', {"class":"w-clearfix w-inline-block comp-row"})
    body = soup.find_all('a', {"class":"vcell"})[:300]
    listBist = [div.text for div in body]
    new_list = [item for item in listBist if any(char.isalpha() for char in item)]
    bist100list = [new_list[i] for i in range(0,len(new_list),2)]
    bist100namelist = [new_list[i] for i in range(1,len(new_list),2)]
    return dict(zip(bist100list, bist100namelist))
 
 
def takenasdaqlist():

    headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"}
    res=requests.get("https://api.nasdaq.com/api/quote/list-type/nasdaq100",headers=headers)
    main_data=res.json()['data']['data']['rows']
 
    nasdaqList = [main_data[i]['symbol'] for i in range(len(main_data))]
    nasdaqNameList = [main_data[i]['companyName'] for i in range(len(main_data))]
    return dict(zip(nasdaqList, nasdaqNameList))
 
def takefonlist():
    url = 'https://www.kap.org.tr/tr/YatirimFonlari/YF'
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text,'lxml')
    #body = soup.find_all('div', {"class":"column-type7 wmargin"})
    body = soup.find_all('a', {"class":"vcell"})
    listFon = [div.text for div in body]
    if len([div.text for div in soup.find_all('span', {"class":"vcell"})])>=1:
        listFon = np.insert(listFon,4202,'YAPI KREDİ PORTFÖY YÖNETİMİ A.Ş.') #fill NA values now manuel..
    FonList = [listFon[i] for i in range(0,len(listFon),3)]
    FonNameList = [listFon[i] for i in range(1,len(listFon),3)]
    FonCompList = [listFon[i] for i in range(2,len(listFon),3)]
    Fondict = [{'key': FonList[i], 'value': FonNameList[i], 'info': FonCompList[i]} for i in range(len(FonList))]
    return Fondict
 
def takealltickets():
    bis100Listdict = takebist100list()
    nasdaqListdict = takenasdaqlist()
    fonListdict = takefonlist()
    return bis100Listdict, nasdaqListdict, fonListdict

takealltickets()