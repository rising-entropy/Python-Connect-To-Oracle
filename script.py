from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import threading 
import bs4 as bs
import csv
import eel
import urllib
import requests
import re
import json
import validators


import cx_Oracle
con = cx_Oracle.connect('mydb/mydb@localhost:1521/xe')
cursor = con.cursor()


eel.init("web")

@eel.expose
def getMeTheLinks(queryToAsk, numberOfPages):
    
    numberOfPages = int(numberOfPages)
    queryVal = queryToAsk
    queryToAsk = queryToAsk.replace(" ", "%20")

    browser= webdriver.Chrome('chromedriver')

    browser.get('https://www.linkedin.com')
    sleep(1)

    userid = browser.find_element_by_xpath(".//*[@id='session_key']")
    userid.send_keys('devangtechcurve@gmail.com')
    sleep(1)
    userpass = browser.find_element_by_xpath(".//*[@id='session_password']")
    userpass.send_keys('Admin@123')
    sleep(1)
    userpass = browser.find_element_by_xpath("/html/body/main/section[1]/div[2]/form/button")
    userpass.click()

    sleep(5)

    lstOfCompanyLinks = []
    

    for i in range(numberOfPages):
        if i == 0:
            thatLink = "https://www.linkedin.com/search/results/companies/?companyHqGeo=%5B%22102713980%22%5D&keywords=" + queryToAsk + "&origin=FACETED_SEARCH"
        else:
            thatLink = "https://www.linkedin.com/search/results/companies/?companyHqGeo=%5B%22102713980%22%5D&keywords=" + queryToAsk + "&origin=FACETED_SEARCH"+"&page="+str(i+1)
        sleep(1)
        
        browser.get(thatLink)
        sleep(2)
        valData = browser.page_source

        allCompanyLinks = re.findall(r"https:\/\/www\.linkedin\.com\/company\/.*?\/", valData)

        lstOfCompanyLinks += list(set(allCompanyLinks))
        
        sleep(0.1)
    
    #unique list of all company links on linkedIn    
    lstOfCompanyLinks = list(set(lstOfCompanyLinks))
    
    companyToEmployees = {}
    companyToAbout = {}
    
    lstToSend = []
    
    with open('companyData.csv', mode='w') as wfile:
        writer = csv.writer(wfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Company Name", "Company LinkedIn Link", "Company Website", "Phone Number", "Company Size"])
    
        for company in lstOfCompanyLinks:
            companyAboutUs = company+"about/"
            browser.get(companyAboutUs)
            
            sleep(2)
            aboutUsPage = browser.page_source
            
            #website name
            try:
                websiteName = re.findall(r"\<span class\=\"link\-without\-visited\-state\" dir\=\"ltr\"\>.*?\<\/span\>", aboutUsPage, re.MULTILINE | re.DOTALL)[0]
                websiteName = websiteName.split(">")[1].strip()
                websiteName = websiteName.split("<")[0].strip()
            except:
                websiteName = ""
                
            
            #phone
            try:
                phoneNumber = re.findall(r"\<span aria\-hidden\=\"true\" class\=\"link\-without\-visited\-state\" dir\=\"ltr\"\>.*?\<\/span\>", aboutUsPage, re.MULTILINE | re.DOTALL)[0]
                phoneNumber = phoneNumber.split(">")[1].strip()
                phoneNumber = phoneNumber.split("<")[0].strip()
            except:
                phoneNumber=""
                
            #company size
            try:
                companySize = re.findall(r"Company size.*?\<\/dt\>.*?\<dd class\=\"org\-about\-company\-module\_\_company\-size\-definition\-text t\-14 t\-black\-\-light mb1 fl\"\>.*?\<\/dd\>", aboutUsPage, re.MULTILINE | re.DOTALL)[0]
                companySize = companySize.split(">")[2].strip()
                companySize = companySize.split("<")[0].strip()
            except:
                companySize = ""
                
            #company name
            try:
                companyName = re.findall(r"\<h1 class\=\"t\-24 t\-black t\-bold full\-width\" title\=\".*?\"\>", aboutUsPage, re.MULTILINE | re.DOTALL)[0]
                companyName = companyName.split("title=")[1]
                companyName = companyName.split("\"")[1]
            except:
                companyName = ""
            
            writer.writerow([companyName, company, websiteName, phoneNumber, companySize, queryVal])
            lstToSend.append([companyName, company, websiteName, phoneNumber, companySize, queryVal]) 
            
            cursor.execute('insert into linkedin values(\''+ companyName +'\',\''+ company +'\', \''+ websiteName +'\', \''+ phoneNumber +'\', \''+ companySize +'\', \''+ queryVal +'\')')
            con.commit()
            
    browser.quit()
    if cursor:
        cursor.close()
    if con:
        con.close()
    return lstToSend
            
eel.start('main.html', size=(1000, 1000))
