#import string
import math
from web_scraper import clean_string
from web_scraper import web_scraper
from collections import Counter
from tabulate import tabulate

def get_collection(doc_collection):
    while True:  #Loop that aquires web-pages and builds doc_collection
       web_page = input('Enter URL: ')
       if web_page == 'stop':
           break
       try:
           title, body = web_scraper(web_page)
           doc_collection.append([title, body])
       except:
           print('Error: Invalid Webpage Entry')
    return(doc_collection)

def term_frequency(term_list):
    term_count = Counter(term_list)
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

#Just multiplies the IDF * TF_WT
def calculate_idfWT(query):
    for i in range (len(query)):
        query[i].append(query[i][2] * query[i][4])
    return(query)

def query_normalize(query):
    #Calculate the length of the query vector for normalization
    length = 0
    for i in range(len(query)):
        length += (query[i][5]**2)
    length = math.sqrt(length)
    #Normalize all values in the query vector.
    for i in range(len(query)):
        query[i].append(query[i][5] / length)

    return(query)

def document_normalize(document_body):
    #Calculate the length of the body vector for normalization
    length = 0
    for i in range(len(document_body)):
        length += (document_body[i][2]**2)
    length = math.sqrt(length)
    #Normalize all values in the body vector.
    for i in range(len(document_body)):
        document_body[i].append(document_body[i][2] / length)

    return(document_body)

#Calculates the cosine similarity between the query and body provided
def calculate_similarity(query, document_body):
    similarity_score = 0
    for i in range(len(query)):
        word = query[i][0]
        #Find all terms that are in both the document body and query
        #These are the only terms that matter for calculations, because
        #If the term is in the query and not in the body then it will result
        #in a 0 when multiplied.
        for term, tf, tf_wt, normalize in document_body:
            if word == term:
                #Multiply the IDF_WT-Normalized to the TF_WT normalized
                #Add this to the total similarity score to be returned
                output_file.write("Found: {0}.\n".format(term))
                output_file.write("Similarity calculation: {0}: {1} * {2} = {3}\n".format(term, query[i][6], normalize, query[i][6] * normalize))
                similarity_score += (query[i][6] * normalize)
                output_file.write("Current similarity score: {0}\n\n".format(similarity_score))

    return(similarity_score)

def file_output(query, doc_collection):
    #Create the output file
    #Put the query table at the top for viewing
    output_file.write('\n\nQUERY TABLE\n')
    output_file.write(tabulate(query, headers=['term', 'tf_raw', 'tf_wt', 'df', 'idf', 'wt', 'n\'lize']))
    output_file.write('\n\nDOCUMENT TABLES\n')
    for title, body in doc_collection:
        output_file.write(title)
        output_file.write('\n')
        body.sort(key = lambda x: x[1], reverse = True)
        output_file.write(tabulate(body, headers=['term', 'tf_raw', 'tf_wt', 'n\'lize']))
        output_file.write('\n')

if __name__ == "__main__":
    output_file = open("info_output.txt", "w+")

    doc_collection = []
    doc_collection = get_collection(doc_collection)
    query = term_frequency(clean_string(input('Enter Query: ')))

    #Calculate all of the term frequencies for the document_collection.
    for i in range(len(doc_collection)):
        doc_collection[i][1] = term_frequency(doc_collection[i][1])

    #calculate doc frequency for each word in the query
    query = document_frequency(query, doc_collection)
    #Calculate the IDF * TF_WT value.
    query = calculate_idfWT(query)
    #Normalize the IDF * TF_WT values for use in calculating cosine similarity score
    query = query_normalize(query)

    #Normalize the TF_WT for the document bodies
    for title, body in doc_collection:
        body = document_normalize(body)

    #Create a list that will store the title and similarity score for every doc
    doc_similarity = []
    output_file.write('CALCULATING SIMILARITY SCORES FOR DOCUMENTS\n')
    for title, body in doc_collection:
        output_file.write('\nDOCUMENT: {0}\n'.format(title))
        doc_similarity.append([title, calculate_similarity(query, body)])

    #Sort the list to provide the most similar documents on top
    doc_similarity.sort(key = lambda x: x[1], reverse = True)

    file_output(query, doc_collection)
    #Print the similarity scores most relevant to least with tabulate function
    #for increased readability
    print(tabulate(doc_similarity, headers=['Title', 'Score'], showindex="always", tablefmt="fancy_grid"), '\n')
    output_file.close()
