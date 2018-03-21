import requests
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

def clean_string(string):
    #Split the block of text from website into seperate tokens
    tokens = word_tokenize(string)
    #Clean out the punctuation and other misc tokens
    words = [word for word in tokens if word.isalpha()]
    #Normalize the words to all lowercase
    words = [word.lower() for word in words]
    #Filter out stopwords
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]
    #Stemming of the words to their base forms
    porter = PorterStemmer()
    stemmed = [porter.stem(word) for word in words]
    return stemmed

def web_crawler(url_in):
    page = requests.get(url_in)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.title.text
    body_text = ""
    for body in soup.find_all('p'):
        body_text += " " + body.text
    body_text = clean_string(body_text)
    return(title, body_text)
