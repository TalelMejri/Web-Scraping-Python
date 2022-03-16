import requests 
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

names=[]
prices=[]
links=[]
DTs=[]
page_num=1
while True:
    result=requests.get(f"https://www.jumia.com.tn/catalog/?q=smart+watches&page={page_num}#catalog-listing")
    src=result.content
    soup=BeautifulSoup(src,'lxml')
    res=soup.find("p",{"class":"-gy5 -phs"}).text.split()
    page_lim=int(res[0])
    if page_num > (page_lim//40):
        print("endedpage")
        break

    name = soup.find_all("h3",{"class":"name"})
    price = soup.find_all("div",{"class":"prc"})
    article = soup.find_all("article",{"class":"prd _fb col c-prd"})

    for i in range(len(article)):
        names.append(name[i].text)
        prices.append(price[i].text)
        links.append("https://www.jumia.com.tn"+article[i].find("a").attrs['href'])
    page_num+=1
    print("page_switched")

for link in links:
    result=requests.get(link)
    src=result.content
    soup=BeautifulSoup(src,"lxml")
    DT=soup.find("ul",{"class":"-pvs -mvxs -phm -lsn"})
    ch=""
    for li in DT.find_all("li"):
        ch+= li.text + "| "
    ch=ch[:-2]
    DTs.append(ch)
    print("article num°"+str(links.index(link)))

file_list=[names,prices,DTs,links]
exported=zip_longest(*file_list)
with open("C:\\Users\\asus\\Desktop\\projet python\\smart_w.csv","w") as myfile:
    wr=csv.writer(myfile)
    wr.writerow(["name","price", "DESCRIPTIF TECHNIQUE","links"])
    wr.writerows(exported)