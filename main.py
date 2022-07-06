from cgi import test
from lib2to3.pgen2 import token
from ntpath import join
from django.shortcuts import render
from django.http import HttpResponse
import os
from dotenv import load_dotenv
import dotenv
import requests
import json
import urllib
from urllib.parse import urljoin
# Create your views here.
load_dotenv()
API_SECRET_KEY =os.getenv('api_key')
EMAIL =os.getenv('email')
BASE_URL ="https://api.cloudways.com/api/v1/"
load_dotenv()

class CloudwaysApiCalls():
    url=""
    access_token=os.getenv('access_token'), 
    headers= {}
    payload={}
    req={}
    server_id=''
    def setupvariables(self):
        self.url = urljoin(BASE_URL, 'oauth/access_token',)  
        self.payload = {'email': EMAIL, 'api_key': API_SECRET_KEY}
        self.req = requests.post(self.url, data=self.payload)
        self.access_token= json.loads(self.req.text).get('access_token')
        dotenv.set_key(dotenv.find_dotenv(), 'access_token', self.access_token)
        print(self.access_token)
        self.headers = {'Authorization': 'Bearer %s' % self.access_token}       
        return HttpResponse('Succes')      

    # def getFun(self , url, headers, data,):
    #     try:
    #         self.req = requests.get(self.url, headers=self.headers, data=self.payload)
    #         print(self.req.text)
    #     except Exception as e:
    #         print(e)
    def getServer(self):  
        self.url = urljoin(BASE_URL, 'server')
        try:
            self.req = requests.get(self.url, headers=self.headers)
            res = json.loads(self.req.text)
            self.server_id = res['servers'][1]['id']
            print(res['servers'][1]['id'])
        except Exception as e: 
            print(e) 
        return HttpResponse('success')


    def createApp(self):
        self.url = urljoin(BASE_URL, 'app')
        app_label=input("Enter The Name of your App")
        self.payload = {'server_id': int(self.server_id), 'application': 'phplaravel', 'app_label': app_label}
        print(self.payload)
        try:
            self.req = requests.post(self.url, headers=self.headers, data=self.payload)
        except Exception as e:
            print(e)
    def addDomain(self):
        self.url =urljoin(BASE_URL, 'app/manage/cname')
        
        self.payload= {'server_id': int(self.server_id), 'app_id': 2735040, 'cname': 'www.dev.stalis.co.ke' }
        print(self.headers)
        print(self.payload)
        try:
            self.req = requests.post(self.url, headers=self.headers, data=self.payload)
            print(self.req)
        except Exception as e:
            print(e)

    def aliasesDomain(self):
        self.url =urljoin(BASE_URL, 'app/manage/aliases')
        aliasesdomain= ['www.dev.stalis.co.ke', 'dev.stalis.co.ke']
        self.payload= {'server_id': int(self.server_id), 'app_id': 2735040, 'aliases': aliasesdomain }
        print(self.headers)
        print(self.payload)
        try:
            self.req = requests.post(self.url, headers=self.headers, data=self.payload)
            print(self.req)
        except Exception as e:
            print(e)
    def gitkeyGenerate(self):
        self.url =urljoin(BASE_URL, 'git/generateKey')
        self.payload= {'server_id': int(self.server_id), 'app_id': 2735029}
        try:
            self.req = requests.post(self.url, headers=self.headers, data=self.payload)
            print('Git Key Generate ')
            print(self.req.content)
        except Exception as e:
            print(e)
    def gitdeployHistory(self):
        self.url = urljoin(BASE_URL,'git/history')
        self.payload= {'server_id': int(self.server_id), 'app_id': 2735040}
        try:
            self.req = requests.get(self.url, headers=self.headers, data=self.payload)
            print('Git HIstory deploy')
            print(self.req.text)
        except Exception as e:
            print(e)




def main(request):
    
    c= CloudwaysApiCalls()
    c.setupvariables()
    c.getServer()
    #c.createApp()
    c.addDomain()
    c.aliasesDomain()
    c.gitkeyGenerate()
    c.gitdeployHistory()
    return HttpResponse('succes')

if __name__ == "__main__":
    main()