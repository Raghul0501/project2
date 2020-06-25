import requests
from bs4 import BeautifulSoup
import sqlite3
import argparse

def database(dbname):
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute("CREATE TABLE HPlaps(MODEL TEXT ,PROCESSOR TEXT,RAM TEXT,ROM TEXT,PRICE REAL)" )
    conn.close()
    
def upload(info,dbname):
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute("INSERT INTO HPlaps VALUES(?,?,?,?,?)",info)
    conn.commit()
    conn.close()

parser = argparse.ArgumentParser()
parser.add_argument("--pages",help="Enter number of pages",type=int) 
parser.add_argument("--dbname",help="Enter name of databse",type=str) 
args = parser.parse_args()
pages = args.pages
dbname = args.dbname

database(dbname)

main_url = "https://store.hp.com/in-en/default/laptops-tablets.html?p="
for page in range(pages):
    url = requests.get(main_url+str(page+1))
    soup = BeautifulSoup(url.content,'html.parser')   
    laptops = soup.find_all("div",{"class":"product details product-item-details"})
    for laptop in laptops:
        model = laptop.find("strong",{"class":"product name product-item-name"}).text.strip()
        processor = laptop.find("li",{"class":"processorfamily"}).text
        ram = laptop.find("li",{"class":"memstdes_01"}).text
        rom = laptop.find("li",{"class":"hd_01des"}).text
        price = laptop.find("span",{"class":"price"}).text
        info = (model , processor , ram , rom , price)
        upload(info,dbname)



    