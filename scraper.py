# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 14:11:31 2020
@author: aanup
"""

#Import Libraries
import requests
from bs4 import BeautifulSoup
import re
import unicodedata


# The Hindu Newspaper Scrapper
def scrape_hindu(urlLink):
    title = ''
    atext = ''
    try:
        page = requests.get(urlLink)
    except:
        print("Page not accessible")
    soup = BeautifulSoup(page.text, 'html.parser')
    
    # Extract the title
    title = soup.find('title')
    if title is None:
        print('NO TITLE')
    else:
        title = soup.find('title').text
        index = str(title).find('-')
        title = title[:index].strip()
    
    # Extract the header with the date and author information
    # Extract article image - NOT WORKING
    # Extract the article text
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.decompose()  # rip it out
    
    article = soup.find(id=re.compile('^content-body-14269002-')) #16835231
    if article is not None:
        atext = article.text
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in atext.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        atext = '\n'.join(chunk for chunk in chunks if chunk)
    
        
    if atext is not None and title is not None:
        #preprocess text to store text with escape character " for SQL database
        atext = re.sub(r"\\", "", atext)
        atext = re.sub(r"\"", "\\\" ", atext)
        title = re.sub(r"\"", "\\\" ", title)
       
    return atext

#Uncomment if you wish to test it 
#hindu = "https://www.thehindu.com/news/national/other-states/two-firs-lodged-in-rajasthan-over-congress-complaints-of-horse-trading/article32111508.ece"
#title, atext = scrape_hindu(hindu)
#print(title)
#print(atext)

# The pioneer Scraper
def scrape_pioneer(urlLink):
    title = ''
    text = ''
    try:
        html_page = requests.get(urlLink)
    except:
        print("Page Not accessible")
    soup = BeautifulSoup(html_page.content, 'html.parser')
    if soup.find(itemprop="headline") is not None:
        title = soup.find(itemprop="headline").get_text()
        
            ## Get Story details
        
        text = soup.find(itemprop="articleBody").get_text().strip()
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
 
        if text is not None and not title is None:
            # preprocess text to store text with escape character " for SQL database
            text = re.sub(r"\\", "", text)
            text = re.sub(r"\"", "\\\" ", text)
            title = re.sub(r"\"", "\\\" ", title)
        
    return text

#Uncomment if you wish to test it 
#pioneer = "https://www.dailypioneer.com/2020/top-stories/not-extending-lockdown-in-bengaluru-after-monday--cm.html"
#title, text = scrape_pioneer(pioneer)
#print(title)
#print(text)


# The Times of India Scraper
def scrape_timesofindia(urlLink):
    title = ''
    text = ''
    try:
        page = requests.get(urlLink)
    except:
        print("This page is not accessible")
    soup = BeautifulSoup(page.text, 'html.parser')

    # Extract the title
    title = soup.find('title')
    if title is None:
        print("Title not known")
    else:
        title = soup.find('title').text
        
    # Extract the header with the date and author information      
    # Extract the article text
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.decompose()  # rip it out

    article = soup.find(class_='Normal')
    if article is not None:
        text = article.text
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)

    else:
        article = soup.find(class_='_3WlLe clearfix')
        if article is not None:
            text = article.text
            # break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)

    if text is not None and title is not None:
        #preprocess text to store text with escape character " for SQL database
        text = re.sub(r"\\", "", text)
        text = re.sub(r"\"", "\\\" ", text)
        title = re.sub(r"\"", "\\\" ", title)
        
    return text

#Uncomment if you wish to test it 
#toi = "https://timesofindia.indiatimes.com/entertainment/tamil/movies/news/ranjit-bindus-movie-encourages-people-to-speak-up-without-fear/articleshow/74494780.cms?"
#title, text = scrape_timesofindia(toi)
#print(title)
#print(text)



#The Assam Tribune Scraper
def scrape_assamtribune(urlLink):
    title = ''
    cleantext = ''
    try:
        page = requests.get(urlLink)
        soup = BeautifulSoup(page.text, 'html.parser')

        # Extract the article text
        articleText = page.text
        # Extract the location and date information
        indexDate = articleText.index("<font face=\"Verdana\" color=\"#FFFFFF\" size=-2>")
        indexDateend = articleText.index("</b>", indexDate)
        aText = articleText[indexDate: indexDateend]
        ib = articleText.index("<font size=+1>")
        
        #extract title of the news article
        indexTitleend = articleText.index("<br>", ib)
        title = articleText[ib+ len('<font size=+1>'):indexTitleend]
        
        # Extract the body of the article
        indexBegin = articleText.index("<!-- EXT_AssamTribune_Web_ROS_AS_MID,position=1-->")
        indexEnd = articleText.index("<!-- EXT_AssamTribune_Web_ROS_AS_EOA,position=1-->")
        
        
        #get the index of content of the news
        indexContent = articleText.index("<br>", ib)
        indexContentstart = articleText.index("<br>", indexContent)
        content = articleText[indexContentstart: indexEnd]
                                
        aText += articleText[ib:indexBegin] + " "
        aText += articleText[indexBegin: indexEnd]

        # Remove any html tags from the article text
        #cleantext = BeautifulSoup(aText, "html.parser").text
        cleantext = BeautifulSoup(content, "html.parser").text
        
        # Remove extra line breaks
        lines = (line.strip() for line in cleantext.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        cleantext = '\n'.join(chunk for chunk in chunks if chunk)

        if cleantext is not None and title is not None:
        #preprocess text to store text with escape character " for SQL database
            cleantext = re.sub(r"\\", "", cleantext)
            cleantext = re.sub(r"\"", "\\\" ", cleantext)
            title = re.sub(r"\"", "\\\" ", title)
    except:
        print("Page not found")        
    return cleantext

#Uncomment if you wish to test it 
#assam = "http://www.assamtribune.com/scripts/detailsnew.asp?id=jul1720/at056"
#title, cleantext = scrape_assamtribune(assam)
#print(title)
#print(cleantext)


# Kashmir Observer Scraper
def scrape_kasmirobserver(urlLink):
    text = ''
    title = ''   
    try:
        html_page = requests.get(urlLink)
        print(html_page)
        soup = BeautifulSoup(html_page.content, 'html.parser')
        if soup.find('h1', class_="post-title") is not None:
            title = soup.find('h1', class_="post-title").get_text()
            dateTime = soup.find('p', class_="single_postmeta").get_text()
            dateTime = dateTime.split()
            dateTime = dateTime[1] + ','+ dateTime[2] + dateTime[3]
                ## Get Story details

            # Extract the article text
            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.decompose()  # rip it out

            article = soup.find('article')
            texts = article.find_all('p')
            text = ''
            for t in texts[0:-9]:
                text+= t.get_text() + '\n'
            # break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)

            if text is not None and title is not None:
                #preprocess text to store text with escape character " for SQL database
                text = re.sub(r"\\", "", text)
                text = re.sub(r"\"", "\\\" ", text)
                title = re.sub(r"\"", "\\\" ", title)
    except:
        print("Page not found")
    return text

#Uncomment if you wish to test it 
#kasmir = "https://kashmirobserver.net/2016/07/31/a-tale-of-two-kashmirs/"
#title, text = scrape_kasmirobserver(kasmir)
#print(title)
#print(text)
    
# The economic times scraper
def scrape_economictimes(urlLink):
    text = ''
    try:
        page = requests.get(urlLink)
    except:
        print("Page not found")
    if page is not None:
        soup = BeautifulSoup(page.text, 'html.parser')
        article = soup.find(class_='artText')
    if article is not None:
        text = article.text
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        #content = text
        
    if text is not None:
        # preprocess text to store text with escape character " for SQL database
        text = re.sub(r"\\", "", text)
        text = re.sub(r"\"", "\\\" ", text)
        
    return text

#Uncomment if you wish to test it 
#economic = "https://economictimes.indiatimes.com/markets/stocks/news/tvs-motor-may-lose-premium-edge-in-face-of-multiple-bumps/articleshow/76125340.cms"
#title, text = scrape_economictimes(economic)
#print(title, "\n")
#print(text)


# The incredibel Orissa Scraper
def scrape_incredibleOrissa(urlLink):
    title = ''
    text = ''
    try:
        html_page = requests.get(urlLink)
    except:
        print("Page not Found")
    soup = BeautifulSoup(html_page.content, 'html.parser')
    if soup.find('h1', class_="title single-title") is not None:
        title = soup.find('h1', class_="title single-title").get_text()
        dateTime = soup.find('span', class_="thetime").get_text()
        dateTime.replace(",", "")
        
        
        author = soup.find('span', class_="theauthor").get_text()
        article = soup.find('div', class_='post-single-content box mark-links')
        articleText = article.find_all('p')
            
        text = ''
        for p in articleText:
            text = text + p.get_text()
        
        if text is not None and title is not None:
            #preprocess text to store text with escape character " for SQL database
            text = re.sub(r"\\", "", text)
            text = re.sub(r"\"", "\\\" ", text)
            title = re.sub(r"\"", "\\\" ", title)
            author = dateTime + ' | ' + re.sub(r"\"", "\\\" ", author)
                
    return text


# The Deccan Herald Scraper
def scrape_deccanherald(urlLink):
    text = ''
    try:
        html_page = requests.get(urlLink)
    except:
        print("Page not Found")
    if html_page is not None:
        soup = BeautifulSoup(html_page.content, 'html.parser')
        article = soup.find(class_= 'content')
    if article is not None:
        text = article.text
        text = unicodedata.normalize("NFKD", text)
    if 'Sorry, the page you are looking is no longer available' in text:
        print('"Page no longer available"')
    else:
        return text

# The Indian Express Scraper   
def scrape_indianexpress(urlLink):
    atext = ''
    
    try:
        html_page = requests.get(urlLink)
    except:
        print("Page not Found")
    if html_page is not None:
        soup = BeautifulSoup(html_page.content, 'html.parser')
        article = soup.find(class_= 'articles')
    if article is not None:
        text = article.findAll('p')
        for i in text:
            atext = atext + i.text
        atext = re.sub(r"\"", "", atext)
    return atext

# The Deccan Chronicle Scraper
def scrape_deccanchronicle(urlLink):
    atext = ''
    text = ''
    try:
        html_page = requests.get(urlLink)
    except:
        print("Page not Found")
    if html_page is not None:
        soup = BeautifulSoup(html_page.content, 'html.parser')
        article = soup.find(id='storyBody')
    if article is not None:
        text = article.findAll('p')
        for i in text:
            atext = atext + i.text
        atext = unicodedata.normalize("NFKD", atext)
        atext = re.sub(r"\"", "", atext)
    return atext


# The News Minite Scraper
def scrape_newsminute(urlLink):
    atext = ''
    try:
        html_page = requests.get(urlLink)
    except:
        print("Page not Found")
    if html_page is not None:
        soup = BeautifulSoup(html_page.content, 'html.parser')
        article = soup.find(class_="views-field views-field-body article-content article-body")
    if article is not None:
        text = article.findAll('p')
        for i in text:
            atext = atext + i.text
        atext = unicodedata.normalize("NFKD", atext)
        atext = re.sub(r"\"", "", atext)
    return atext
