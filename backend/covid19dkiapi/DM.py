from datetime import date, datetime
from io import BytesIO
from numpy import integer
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import pandas as pd
from pandas.core.frame import DataFrame
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import matplotlib as mpl
import matplotlib.pyplot as plt
import MySQLdb
from sqlalchemy import engine
from sklearn.cluster import KMeans
from sqlalchemy import text
from sqlalchemy.sql.expression import true
import requests


######################################################
#Collections of necessasry functions
######################################################

#function to create range of dates
def range_date(start_date,end_date):
    #date format frow web d m yyyy
    #generate date from start_date to end_date
    start=start_date.split(' ')
    end=end_date.split(' ')
    sdate=datetime(int(start[2]),int(start[1]),int(start[0])).strftime("%d %m %Y")
    edate=datetime(int(end[2]),int(end[1]),int(end[0])).strftime("%d %m %Y")
    index=pd.date_range(sdate,edate,freq='D').strftime("%d %b %Y")
    #converting month to local languange
    index=index.to_frame(index=False,name="dates")
    # index=index
    d={
        'Jan':'Januari',
        'Feb':'Februari',
        'Mar':'Maret',
        'Apr':'April',
        'May':'Mei',
        'Jun':'Juni',
        'Jul':'Juli',
        'Aug':'Agustus',
        'Sep':'September',
        'Oct':'Oktober',
        'Nov':'November',
        'Dec':'Desember'
    }
    index["dates"]=index["dates"].replace(d,regex=True)
    return index["dates"].values.tolist()

#function to check date available in database
def date_check(sqleng,sh_date):
    exec=text("SELECT COUNT(*) AS C FROM `covid19-dki-kecamatan` WHERE tanggal=:dates")
    exec=exec.bindparams(dates=sh_date)
    msg=pd.read_sql_query(exec,sqleng)
    print(msg.loc[0,"C"])
    if msg.loc[0,"C"]==0:
        return False
    else:
        return True

#function to load data frow web for each date
def load_web(sh_date,browser):
    #find download link with search date
    #set exception here
    try:
        search_result=browser.find_element_by_partial_link_text(sh_date)
    except:
        print("element not found")
        return DataFrame()
    glink=search_result.get_property("href")

    #convert it downloadable link
    #split by "/" character to get the file id
    idg=glink.split("/")[-2]

    #concatenate id file to this link format to create downloadable link
    gdlink="https://drive.google.com/u/0/uc?id="+idg+"&export=download"

    #check exception for 403 forbidden error
    try:
        hdr = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"} #change the version of the browser accordingly
        resp=requests.get(gdlink,headers=hdr)
        df=pd.read_excel(resp.content,sheet_name="data_kecamatan",header=0)
    except:
        print("403 Forbidden")
        return DataFrame()
    return df

#funtion to clean data
def clean_data(df):
    #do cleaning here
    l=df["nama_kecamatan"].size
    for i in range(l):
        if(df.loc[i,"nama_kecamatan"] == "KEP. SERIBU SELATAN"):
            df.loc[i,"nama_kecamatan"] = "Kep. Seribu"
            df.loc[i,"POSITIF"]+=df.loc[i+1,"POSITIF"] 
            df.loc[i,"Dirawat"]+=df.loc[i+1,"Dirawat"] 
            df.loc[i,"Sembuh"]+=df.loc[i+1,"Sembuh"] 
            df.loc[i,"Meninggal.1"]+=df.loc[i+1,"Meninggal.1"]
            df.loc[i,"Self Isolation"]+=df.loc[i+1,"Self Isolation"] 
        elif(df.loc[i,"nama_kecamatan"]=="KOJA"):
            df.loc[i,"nama_kecamatan"]="K o j a"
        else:
            df.loc[i,"nama_kecamatan"]=df.loc[i,"nama_kecamatan"].title()

    #choose province which is "DKI JAKARTA" and choose the important column
    #Nama_provinsi, nama_kecamatan
    df =  df.loc[(df["Nama_provinsi"]=="DKI JAKARTA")
                &(df["nama_kecamatan"]!="Kep. Seribu Utara"),
            ["Nama_provinsi",
            "nama_kota",
            "nama_kecamatan",
            "POSITIF",
            "Dirawat",
            "Sembuh",
            "Meninggal.1",
            "Self Isolation"
            ]
        ]
    #rename the column Meninggal.1 to Meninggal
    df.rename({'Meninggal.1':'Meninggal'},axis=1,inplace=True)
    return df
    # print(slice_df.head())

#funtion to perform clustering, adding group column for each dataset
def create_clus(df,sh_date):
    #perform clustering

    #choose variable and normalize

    clus_df=df.loc[:,["POSITIF","Meninggal"]]

    clus_df=((clus_df-clus_df.mean()))/clus_df.std()

    #clustering with K-Means of k=4

    clus_km=KMeans(n_clusters=4,precompute_distances='auto',random_state=0).fit(clus_df)

    #add to the dataframe

    df["group"]=clus_km.labels_
    df["tanggal"]=sh_date

    return df

#function to add data to MySQL
def add_sql(df,sqlengine,sh_date):
    #write the cleaned table in MySQL with date as table tittle

    Table='covid19-dki-kecamatan'

    #create table in MySQL
    flag=date_check(sqlengine,sh_date)

    #chech if such date exists,IF it is then update the data ELSE append data
    if flag==True:
        #update
        txt=text("DELETE FROM `covid19-dki-kecamatan` WHERE tanggal=:dates")
        sqlengine.execute(txt,{"dates":sh_date})
        df.to_sql(Table,con=sqlengine,if_exists='append')
    else:
        df.to_sql(Table,con=sqlengine,if_exists='append')

#function to draw plot
def draw_plot(df,sh_date):
    #create the graphical representation
    #choose the x axis
    x_axis_choose="nama_kota"

    #choose the data
    data_plot="POSITIF"

    #create graphical representation based on x axis and the data

    fig, axs=plt.subplots(6,1,figsize=(10,16), dpi=50)



    axs[0].bar(df["nama_kecamatan"].to_numpy(),df["POSITIF"].to_numpy())
    axs[0].set_title("Kasus Positif Per Kecamatan di DKI Jakarta tanggal = "+sh_date)
    axs[0].set_ylabel("Jumlah Kasus Positif")
    axs[0].set_xlabel("Kecamatan")

    
    #create class IOBase to store plot png
    f=BytesIO()
    #save to this binary like object

    plt.savefig(f,format="png",dpi=300)

    #return the png from binary like object

    return f.getvalue()

######################################################