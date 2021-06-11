import requests
import json
import re

file1 = open("aboutUs.txt","r") 

yoBoys = file1.read()

websiteName = re.findall(r"\<span class\=\"link\-without\-visited\-state\" dir\=\"ltr\"\>.*?\<\/span\>", yoBoys, re.MULTILINE | re.DOTALL)[0]
websiteName = websiteName.split(">")[1].strip()
websiteName = websiteName.split("<")[0].strip()
print(websiteName)

phoneNumber = re.findall(r"\<span aria\-hidden\=\"true\" class\=\"link\-without\-visited\-state\" dir\=\"ltr\"\>.*?\<\/span\>", yoBoys, re.MULTILINE | re.DOTALL)[0]
phoneNumber = phoneNumber.split(">")[1].strip()
phoneNumber = phoneNumber.split("<")[0].strip()
print(phoneNumber)

companySize = re.findall(r"Company size.*?\<\/dt\>.*?\<dd class\=\"org\-about\-company\-module\_\_company\-size\-definition\-text t\-14 t\-black\-\-light mb1 fl\"\>.*?\<\/dd\>", yoBoys, re.MULTILINE | re.DOTALL)[0]
companySize = companySize.split(">")[2].strip()
companySize = companySize.split("<")[0].strip()
print(companySize)

companyName = re.findall(r"\<h1 class\=\"t\-24 t\-black t\-bold full\-width\" title\=\".*?\"\>", yoBoys, re.MULTILINE | re.DOTALL)[0]
companyName = companyName.split("title=")[1]
companyName = companyName.split("\"")[1]
print(companyName)




"""
<h1 class="t-24 t-black t-bold full-width" title="Animation Circle Studio">
"""