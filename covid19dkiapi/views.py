import base64
from io import BytesIO, IOBase
from os import close
from typing import final
from urllib import parse
from django.shortcuts import render
from django.http import HttpResponse, response
from django.http import HttpRequest
from numpy import load
import pandas as pd
from pandas.core.frame import DataFrame
from sqlalchemy.sql.expression import bindparam
from . import DM as dm
from sqlalchemy import create_engine
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from sqlalchemy import text
import json

#url format:
#http://localhost:8000/covid19dkiapi/?start=20 4 2021&end=25 5 2021&update=FALSE

# Create your views here.

#link to target website
src_url="https://riwayat-file-covid-19-dki-jakarta-jakartagis.hub.arcgis.com/"

#create the database connection
engine = create_engine('mysql+mysqldb://root:@localhost/covid19-dki-kcm')

#funciton will be call from django
def index(request):
    #open the headless browser
    #set up the headless browser
    opts = Options()
    opts.set_headless()
    assert opts.headless
    opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36")
    browser = webdriver.Chrome(options=opts)
    #give time to wait until the element is loaded
    browser.implicitly_wait(60)

    #get webpage from url source
    browser.get(src_url)
    final_data=DataFrame()
    r=dm.range_date(request.GET['start'],request.GET['end'])
    update_flag=request.GET['update']
    for sd in r:
        not_exists=True
        #if user update data at certain range of date, update all of them
        #if not, dont update, add date that is not exist
        if(update_flag=="TRUE"):
            not_exists=False
        else:
            not_exists=dm.date_check(engine,sd)
        #if data not exists or update, else fetch the data from database
        print(not_exists)
        if(not_exists==False):
            print(sd)
            #load data from web
            df=dm.load_web(sd,browser)
            #return data or "not exist"
            if(df.empty):
                final_data=DataFrame()
                break
            #clean the data
            df=dm.clean_data(df)
            #cluster it with K-Means
            df=dm.create_clus(df,sd)
            #add image plot
            a=[BytesIO().getvalue()]*43
            a[0]=dm.draw_plot(df,sd)
            df["image"]=a
            #add or update the Database
            dm.add_sql(df,engine,sd)
            #encode to base64 for JSON delivery
            df.loc[1,'image']=base64.b64encode(df.loc[1,'image'])
            #if the final_data is "first" then get a copy from first date
            if(final_data.empty):
                final_data=df
            else:
                final_data=final_data.append(df,ignore_index=True)
        else:
            #fetch data from database with WHERE clause
            exec=text("SELECT * FROM `covid19-dki-kecamatan` WHERE tanggal=:dates")
            exec=exec.bindparams(dates=sd)
            df=pd.read_sql_query(exec,engine)
            df.loc[0,'image']=base64.b64encode(df.loc[0,'image'])
            #if the final_data is "first" then get a copy from first date
            if(final_data.empty):
                final_data=df
            else:
                final_data=final_data.append(df,ignore_index=True)

    #close the browser
    browser.close()
    if(final_data.empty):
        return response.HttpResponseNotFound("no such data exists")
    else:
        result=final_data.to_json(orient="columns")
        parsed=json.loads(result)
        return response.JsonResponse(parsed,safe=False)