# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 14:48:31 2020
@author: aanup
"""

"""
Newspaper articles scpaer used to scrape the articles which are used as the source for by
the GDELT database (by their event detection system)
"""

import pandas as pd
import scraper
import logging

# Log file to keep record of the counting process
logging.basicConfig(filename="logfilename_kt19.log", level=logging.INFO)

'''
The "india_karnataka_with_districts_2019.csv" file contains all the events happened 
in Karnataka state with events geocoded to respective district for year 2019. This file
is aggregated GDELT daily event file which could be downloaded form GDELT. If you want the 
script to downlaod all the GDELT files and aggregate them yearly you can see my
other repositories. If you could not locate that contact me, I will be happy to help
'''

df = pd.read_csv("india_karnataka_with_districts_2019.csv")
#df_gdelt = df_gdelt_2016.loc[(df_gdelt_2016["EventRootCode"] == 3) | (df_gdelt_2016["EventRootCode"] == 6)]

# Here I only intend to download the events who have the following event codes 
Codes = ['013', '014', '015', '018', '019', '030', '031', '0311', '0312', '0313', '0314', '032',
                '033', '0331', '0332', '0333', '0334', '035', '0351', '0352', '0353', '0354', '0355', 
                '0356', '036', '037', '038', '039', '040', '041', '042', '043', '044', '045', '046', 
                '050', '051', '052', '053', '054', '055', '056', '057', '081', '0811', '0812', '0813',
                '0814', '082', '083', '0831', '0832', '0833', '0834', '084', '0841', '0842' '011', '012',
                '016', '123', '1231', '1232', '1234', '125', '126', '127', '128', '129', 
                '132', '1321', '1322', '1323', '1324', '134', '135', '136', '137', '139','150', '151',
                '152', '153', '154', '172', '1721', '1722', '1724', '173']

# filtering based on event codes
df_gdelt = df.loc[df["EventCode"].isin(Codes)]

#Tamil_dist = ['Ariyalur','Chennai','Coimbatore','Cuddalore','Dharmapuri','Dindigul','Erode',
#                   'Kanchipuram','Kanyakumari','Karur','Krishnagiri','Madurai','Nagapattinam',
#                   'Namakkal','Nilgiris','Perambalur','Pudukkottai','Ramanathapuram','Salem',
#                   'Sivaganga','Thanjavur','Theni','Thoothukudi','Tiruchirappalli','Tirunelveli',
#                   'Tiruppur','Tiruvallur','Tiruvannamalai','Tiruvarur','Vellore','Viluppuram',
#                   'Virudhunagar']

# Districts of Karnataka
Karnataka_dist = ['Bagalkot','Bangalore Rural','Bangalore Urban','Belgaum','Bellary','Bidar','Bijapur','Chamrajnagar',
    'Chikballapur','Chikmagalur','Chitradurga','Dakshin Kannad','Davanagere','Dharwad','Gadag','Gulbarga','Hassan','Haveri',
    'Kodagu','Kolar','Koppal','Mandya','Mysore','Raichur','Ramanagara''Shimoga','Tumkur','Udupi','Uttar Kannand','Yadgir']


# Also filtering based on Districts just to be sure if the events were encoded not codded properly
df_gdelt = df_gdelt.loc[df_gdelt["Districts"].isin(Karnataka_dist)]

# Prinitg the shape
print(df_gdelt.shape)

# Funtion to download Articles and other data
def download_data(df):
    sources = df.SOURCEURL
    g_source = []

    # Split the URL to and only get the newspaper link
    # We will use this to determine which scrpaer to use
    for source in sources:
        g_source.append(source.split("/")[2])
        
    df["SOURCE"] = g_source

    # Mapping categories
    df['EventCategory'] = df['EventRootCode'].map({1:'Make Public Statement', 2:'Appeal',
                    3:'Express intent to cooperate', 4:'Consult', 5:'Engage in diplomatic cooperation',
                    6:'Engage in material cooperation', 7:'Provide aid', 8:'Yield', 9:'Investigate', 10:'Demand',
                    11:'Disapprove', 12:'Reject', 13:'Threaten', 14:'Protest', 15:'Exhibit military posture', 
                    16:'Reduce realations', 17:'coerce', 18:'Assault', 19:'Fight', 20:'Engage in UMV'})
    
    # List of the Newspaper for which we have the scrpaers
    scrape = ["www.thehindu.com", "www.dailypioneer.com", "economictimes.indiatimes.com", "kashmirobserver.net", "www.assamtribune.com", "incredibleorissa.com", "timesofindia.indiatimes.com",
              "www.deccanchronicle.com", "www.deccanherald.com", "indianexpress.com", "www.thenewsminute.com"]
    
    # filter out the other newspaers
    df_scrape = df[df["SOURCE"].isin(scrape)]
    df_scrape = df_scrape.drop_duplicates(subset='SOURCEURL', keep="last")
    print(df_scrape.shape[0])
    
    # disctionary and list to save the data
    data = dict()
    sqlDate = []
    dataId = []
    article = []
    actor1Name = []
    actor2Name = []
    goldsteinScale = []
    averageTone = []
    eventCategory = []
    source = []
    sourceURL = []
    lat = []
    long = []
    eventCode = []

    # Loop over each event to capture the data and also scrape the newspaper articles
    for i in range(df_scrape.shape[0]):
        dataId.append(df_scrape.GLOBALEVENTID.iloc[i])
        sqlDate.append(df_scrape.SQLDATE.iloc[i])
        actor1Name.append(df_scrape.Actor1Name.iloc[i])
        actor2Name.append(df_scrape.Actor2Name.iloc[i])
        goldsteinScale.append(df_scrape.GoldsteinScale.iloc[i])
        averageTone.append(df_scrape.AvgTone.iloc[i])
        eventCategory.append(df_scrape.EventCategory.iloc[i])
        src = df_scrape.SOURCE.iloc[i]
        srcurl = df_scrape.SOURCEURL.iloc[i]
        source.append(src)
        sourceURL.append(srcurl)
        lat.append(df_scrape.ActionGeo_Lat.iloc[i])
        long.append(df_scrape.ActionGeo_Long.iloc[i])
        eventCode.append(df_scrape.EventCode.iloc[i])
        print(i)

        # run scraper 
        if src == "www.thehindu.com":
            te = scraper.scrape_hindu(srcurl)
            article.append(te)
            print("The hindu done")
        if src == "www.dailypioneer.com":
            te = scraper.scrape_pioneer(srcurl)
            article.append(te)
            print("The pioneer done")
        if src == "economictimes.indiatimes.com":
            te = scraper.scrape_economictimes(srcurl)
            article.append(te)
            print("The economic times done")
        if src == "kashmirobserver.net":
            te = scraper.scrape_kasmirobserver(srcurl)
            article.append(te)
            print("The kashmir observer done")
        if src == "www.assamtribune.com":
            te = scraper.scrape_assamtribune(srcurl)
            article.append(te)
            print("The Assam tribune done")
        if src == "incredibleorissa.com":
            te = scraper.scrape_incredibleOrissa(srcurl)
            article.append(te)
            print("The incredible orissa done")
        if src == "timesofindia.indiatimes.com":
            te = scraper.scrape_timesofindia(srcurl)
            article.append(te)
            print("The times of india done")
        if src == "www.deccanchronicle.com":
            te = scraper.scrape_deccanchronicle(srcurl)
            article.append(te)
            print("Deccan Chronicles")
        if src == "www.deccanherald.com":
            te = scraper.scrape_deccanherald(srcurl)
            article.append(te)
            print("Deccan Herald")
        if src == "indianexpress.com":
            te = scraper.scrape_indianexpress(srcurl)
            article.append(te)
            print("The Indian express")
        if src == "www.thenewsminute.com":
            te = scraper.scrape_newsminute(srcurl)
            article.append(te)
            print("The news Minute")
            
    # save in dictionary   
    data = {"GdeltID":dataId , "SqlDate": sqlDate, "Actor1Name": actor1Name, "Actor2Name": actor2Name, "GoldsteinScale":goldsteinScale,
            "AvgTone": averageTone, "EventCategory":eventCategory, "Source":src, "SourceURL":sourceURL, "Latitude":lat, "Londitude":long,
             "Article":article}
    
    # disctionary to dataframe
    df_new = pd.DataFrame(data)

    # return data frame
    return df_new

size = int(df_gdelt.shape[0]/10)


'''
Below I divide the dataframe into 10 different smaller dataframes
and download accordingly. You may completely ignore this and download 
in the single file.
'''

# divide into 10 different 
df_1 = df_gdelt[:size]
df_2 = df_gdelt[size:2*size]
df_3 = df_gdelt[2*size:3*size]
df_4 = df_gdelt[3*size:4*size]
df_5 = df_gdelt[4*size:5*size]
df_6 = df_gdelt[5*size:6*size]
df_7 = df_gdelt[6*size:7*size]
df_8 = df_gdelt[7*size:8*size]
df_9 = df_gdelt[8*size:9*size]
df_10 = df_gdelt[9*size:10*size]

# download into ten different files
df_art1 = download_data(df_1)
df_art1.to_csv("k18_art1.csv", index=False)
df_art2 = download_data(df_2)
df_art2.to_csv("k18_art2.csv", index=False)
df_art3 = download_data(df_3)
df_art3.to_csv("k18_art3.csv", index=False)
df_art4 = download_data(df_4)
df_art4.to_csv("k18_art4.csv", index=False)
df_art5 = download_data(df_5)
df_art5.to_csv("k18_art5.csv", index=False)
df_art6 = download_data(df_6)
df_art6.to_csv("k18\9_art6.csv", index=False)
df_art7 = download_data(df_7)
df_art7.to_csv("k19_art7.csv", index=False)
df_art8 = download_data(df_8)
df_art8.to_csv("k19_art8.csv", index=False)
df_art9 = download_data(df_9)
df_art9.to_csv("k19_art9.csv", index=False)
df_art10 = download_data(df_10)
df_art10.to_csv("k19_art10.csv", index=False)
