#import string
import math
from web_scraper import clean_string
from web_scraper import web_scraper
from collections import Counter
from tabulate import tabulate
from copy import deepcopy

def get_collection(doc_collection):
    while True:  #Loop that aquires web-pages and builds doc_collection
       web_page = input('Enter URL: ')
       if web_page == 'stop':
           break
       try:
           title, body = web_scraper(web_page)
           doc_collection.append([title, body])
           doc_dict.append(set(body))
       except:
           print('Error: Invalid Webpage Entry')
    return(doc_collection)

def term_frequency(list_in):
    term_count = Counter(list_in)
    count_list = []
    for word, count in term_count.items():
        count_log = (math.log1p(count))
        count_list.append([word,count,count_log])
    return(count_list)


def document_frequency(query, doc_collection):
    for i in range (len(query)):
        doc_freq = 0 #Set current doc_freq to 0 for new term
        term = query[i][0] #Define what the term we are finding df for is
        for j in range(len(doc_collection)): #Loop for searching each doc in collection
            body = doc_collection[j][1] #Define what the body list we are searching through is
            for word, tf, tf_wt in body: #Search the body of the list for the term
                if term == word:
                    doc_freq += 1 #If you find it, increase doc_freq
        query[i].append(doc_freq)
        query[i].append(1 + math.log((1 + len(doc_collection)) / (1 + doc_freq))) #Add the document frequency to the list
    return(query)

def query_normalize(query_in):
        #Calculate the length of the query vector for normalization
        length = 0
        for i in range(len(query_in)):
            length += (query_in[i][5]**2)
        length = math.sqrt(length)
        #Normalize all values in the query vector.
        for i in range(len(query_in)):
            query_in[i].append(query_in[i][5] / length)

        return(query_in)

def document_normalize(body):
    #Calculate the length of the body vector for normalization
    length = 0
    for i in range(len(body)):
        length += (body[i][2]**2)
    length = math.sqrt(length)
    #Normalize all values in the body vector.
    for i in range(len(body)):
        body[i].append(body[i][2] / length)

    return(body)

def calculate_simularity(query, document_body):
    simularity_score = 0
    for i in range(len(query)):
        word = query[i][0]
        for term, tf, tf_wt, normalize in body:
            if word == term:
                simularity_score += (query[i][6] * normalize)

    return(simularity_score)

if __name__ == "__main__":
    doc_collection = [] #This list will store the title and dictionary for our documents
    doc_dict = [] #Because of the way I am appending info as the program executes
                  #It is important to store just the raw terms for calc df
    doc_collection = get_collection(doc_collection)

    #Calculate all of the term frequencies for the document_collection.
    for i in range(len(doc_collection)):
        temp = term_frequency(doc_collection[i][1])
        doc_collection[i][1] = temp

    #Gets the query and cleans it. Counts the TF of the query.
    query = term_frequency(clean_string(input('Enter Query: ')))
    query_list = document_frequency(query, doc_collection)

    #Calculate the IDF * TF_WT value.
    for i in range (len(query_list)):
        query_list[i].append(query_list[i][3] * query_list[i][4])

    #Normalize the IDF * TF_WT values for use in calculating cosine simularity score
    query_list = query_normalize(query_list)

    for title, body in doc_collection:
        body = document_normalize(body)

    doc_simularity = []
    for title, body in doc_collection:
        doc_simularity.append([title, calculate_simularity(query, body)])

    print(tabulate(query, headers=['term','tf','tf_wt','df','idf','idf_wt','nmlize']))
    doc_simularity.sort(key = lambda x: x[1], reverse = True)

    print('\n\n', tabulate(doc_simularity, headers=['Title', 'Score']))
