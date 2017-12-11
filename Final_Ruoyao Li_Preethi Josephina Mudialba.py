#Author Name : Preethi Josephina Mudialba ,Ruoyao Li
#Original Creating Date : Feb 26th 2017
#Last Modification Date : March 4th 2017
#Brief Description : Project Final Milestone
#we generated 2 files - index.html(which has the list of keywords) and
#inventor.html (which is the list of inventors)
#on clicking on any keyword in the index_milestone4.html file you will be
#directed to another html file titled keyword.html which 
#contains all the application name(s), application number(s), and inventor(s)
#on clicking on each inventors name you will be directed to the an html page
#titled inventorname.html and this page lists all the application the inventor is a part of 
#and similarly on clicking on any authors name  you will be directed to html file
#titled - author.html which contains  all patent application numbers and names
#for every patent application that the inventor is linked to.

from bs4 import BeautifulSoup
import requests
import re
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.compat import Counter
import csv
import math

NUMBER = 15

#Funcion which reads the CSV file and saves the content in a dictionary
def read_csv_file(file):
    replace_dictionary = {}
    line_number = 0
    with open(file,'r', encoding = "ISO-8859-1") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',', quotechar = '|')    #reads the CSV file
        for row in csv_reader:
            if line_number == 0:
                line_number += 1
                continue
            replace_dictionary[row[0].strip()] = row[1].strip()          
    csv_file.close()
    return replace_dictionary

# Scrape the website, and returns all the urls of the 15 applications
def get_urls(index_url):
    web_content = requests.get(index_url)
    soup = BeautifulSoup(web_content.text, "html.parser")
    # This set stores all the patent application URLs
    web_links = [""] * 15
    index = 0
    for item in soup.findAll('a', attrs = {'href':re.compile("^/netacgi/")}):
        temp = item.get('href')
        if temp not in web_links:
            web_links[index] = temp
            index += 1
    return web_links[:index]



# Crawl the content of each url in the list, and concatenate all the content to
# the string "file_content"
def get_urls_content(web_links):
    file_content = ""
    for curr_url in web_links:
        curr_content = requests.get("http://appft.uspto.gov/" + curr_url)
        soup = BeautifulSoup(curr_content.text, "html.parser")
        file_content = file_content + soup.get_text()
    return file_content

#Funtion to split the file content ino different lines
def split_file_content(file_content):
    new_file_content = [""]
    index = 0
    temp_content = file_content.split("\n")
    new_file_content = new_file_content * len(temp_content)
    for item in temp_content:
        if item.strip() != "":
            new_file_content[index] = item.strip()
            index += 1
    return new_file_content


# Function of finding the application abstarct of each application 
def application_abstract(file_content):
    appl_abstract = [""]
    appl_abstract = appl_abstract * NUMBER
    appl_numbers = [""]
    appl_numbers = appl_numbers * NUMBER
    temp_dictionary = {}
    index = 0
    index_appl_no =0
    start = 0
    end = 0
    flag = 0
    temp = ""
    for i in range(len(file_content)):
        #if( flag == 0):
        #    temp_split = file_content[i].split(":")
        #    for j in range(len(temp_split)):
        #        if(temp_split[j] == "United States Patent Application"):
        #            print("2"+ str(temp_split[j+1]))
        #            flag = 1
        if(file_content[i] == "Appl. No.:"):
           appl_numbers[index_appl_no] = file_content[i+1]
           #print( appl_numbers[index_appl_no])
           #print (index_appl_no)
           #print("---------------------------------")
           index_appl_no = index_appl_no + 1
        if(file_content[i] == "Abstract"):
           start = i
        if(file_content[i] == "Inventors:"):
            end = i
        if(end-start > 0):
            for j in range(start+1, end):
                temp = temp + " " + file_content[j]
            appl_abstract[index] = temp
            #print(appl_abstract[index])
            #print(index)
            index = index + 1
            start = 0
            end = 0
            temp = ""
            flag = 0

    for index in range(len(appl_abstract)):
           key = appl_numbers[index]
           value = (appl_abstract[index])          
           #print("--------------------------------")          
           temp_dictionary[key] = value
           
#   for k, v in temp_dictionary.items():
#            print(k, v)
#            print("--------------------------")
    return temp_dictionary
       

#Function which is used to perform the summary of bag text processing,
#replaces the word --> Perform normalization , joining compound words, Perform stemming
def replace_words(file_content, replace_dictionary):
    for key in replace_dictionary.keys():
        for index in range(len(file_content)):
            file_content[index] = file_content[index].strip()
            start_index = file_content[index].find(key)
            if(start_index != -1):
                end_index = start_index + len(key)     
                file_content[index] = file_content[index].replace(file_content[index][start_index: end_index], \
                                            replace_dictionary[key])
    return file_content

def tokenize_content(file_content):
    result = [""]
    result = result * 24000
    index = 0
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    for line in file_content: 
        tokens = tokenizer.tokenize(line)
        for token in tokens:
            result[index] = token.strip()
            index += 1
    return result[:index]

def read_symbols(file):
    with open(file,'r', encoding = "utf-8") as symbol_file:
        symbols = symbol_file.read().split("\n")
    symbol_file.close()
    return symbols   #returns symbols

def remove_symbols(symbols, replaced_file_content):
    for index in range(len(replaced_file_content)):
        for symbol in symbols:
            if replaced_file_content[index].find(symbol) != -1:
                replaced_file_content[index] = replaced_file_content[index].replace(symbol, "")   #replace symbol with an empty string
    return replaced_file_content

def split_tokens(tokens):
    res = set()   
    for token in tokens:
        temp = token.split()
        for item in temp:
            res.add(item)
    return res

def lemmatize_content(tokens):
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return tokens

def remove_stopwords(tokens):
    stop_words = stopwords.words('english')
    tokens = [token for token in tokens if token not in stop_words]
    return tokens

def compute_term_frequency(tokens):
    tf = Counter(tokens)
    return tf

def compute_inverse_document_frequency(tf, tokens):
    idf = Counter()
    for t in tokens:
        if tf[t] > 0:
            idf[t] = math.log(1 / tf[t])
    return idf

def compute_tf_idf(tokens, tf, idf):
    tfidf = Counter()
    for t in tokens:
        tfidf[t] = tf[t] * idf[t]
    return tfidf

def choose_top_k_words(tfidf, k):
    result = [""]
    result = result * k
    index = 0
    terms_sorted_tfidf_desc = sorted(tfidf.items(), key=lambda x: -x[1])
    terms, scores = zip(*terms_sorted_tfidf_desc)
    keywords = terms[len(terms) - k:]
    for keyword in keywords:
        if(len(keyword) >= 3):
            result[index] = keyword
            index += 1
    return sorted(result)

#Funtion to output the content to the html file
def output_index_html(keywords, file):
      outfile = open(file + ".html", 'w')      #creates a html file 
      
      for item in keywords:
          message = """<html>               
          <head></head>
          <body><p>"""  + item + """</p></body> """
            
          outfile.write('<a href="' + item + '.html">{}</a>'.format(message))
          #writes the output to the html file

      outfile.close()

#Funcion which reads the lines form the text file and saves
#the necessary info in lists
def read_filter_data(file_content):                     
    appl_no = [""]
    appl_no = appl_no * NUMBER
    inventor = [""]
    inventor = inventor * 40
    index_1 = 0
    index_2 = 0
    for index in range(len(file_content)):
        if contains_inventor_info(file_content[index]):
            i = index + 1
            while file_content[i].find("Applicant") == -1:
                inventor[index_1] += file_content[i]
                i += 1
            index = i
            index_1 += 1
        elif contains_application_no_info(file_content[index]):
            appl_no[index_2] = file_content[index + 1]
            index_2 += 1
    return appl_no, inventor[:index_1]


#Funtion to check if the inventor's details is present 
def contains_inventor_info(line):                                                       #Function to check if a line contains the word "Inventors" 
    start_index = line.find("Inventors:")                                               #Returns the index of the line else returns -1
    if start_index != -1:
        return True
    return False

#Funtion to check if the application number is present 
def contains_application_no_info(line):                                                 #function to check if a line containts the word "Appl. No. :"                                                                                       
    start_index = line.find("Appl. No.:")                                               #returns the index of the line else returns -1
    if start_index != -1:
        return True
    return False


#Function of finding the application names of each application 
def application_name(file_content):
    url = "http://appft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.html&r=0&p=1&f=S&l=50&Query=aanm%2F%22carnegie+mellon%22+AND+PD%2F4%2F1%2F2016-%3E6%2F30%2F2016&d=PG01"
    appl_name = [""]
    appl_name = appl_name * NUMBER
    index = 0
    web_content = requests.get(url)
    soup = BeautifulSoup(web_content.text, "html.parser")
    for a_tag in soup.find_all('a'):
        temp = a_tag.text.strip()
        if temp != "" and not(temp.isdigit()):
            appl_name[index] = temp;
            index += 1
    return appl_name

#Function which extract the inventor details for the line , by stripping away
#any extra spaces and text and returns a list of inventors
def extract_inventor_info(inventor):                                                    #Function to extract the inventors from the line 
    row = NUMBER
    col = 25
    length = 0
    temp = [""]
    temp = temp * NUMBER
    temp_list = []
    for i in range(row):
        temp_list.append([])
        for j in range(col):
            temp_list[i].append("")
    index_3 = 0 
    invt_list = []
    for i in range(row):
        invt_list.append([])
        for j in range(col):
            invt_list[i].append("")
 
    for index_1 in range(len(inventor)):
        inventor[index_1] = inventor[index_1].strip()         #removes the word inventors from the line and strip removes the empty spaces
        temp = inventor[index_1].split(";")                                #splits the line
        index_3 = 0
        for index_2 in range(len(temp)):                                   #for loop to iterate through the list of the the newly split words
            if temp[index_2].find("(") != -1:                              #if a '(" is present the word  is ignored and the next iteration is carried out.
                continue
            else:
                temp_list[index_1][index_3] = temp[index_2].strip()
                index_3 += 1               
    for index_1 in range(row):
        index_3 = 0
        for index_2 in range(col):
            if index_2 % 2 == 1 and temp_list[index_1][index_2].strip() != "":
                invt_list[index_1][index_3] = temp_list[index_1][index_2]
                index_3 += 1
    return invt_list

#Function which stores the application content
def store_application(content):
    res = [""]
    res = res * 15
    index = 0
    list_of_applications = content.split("United States Patent Application")
    for item in list_of_applications:
        if len(item) >= 500:
            res[index] = item
            index += 1
    return res


# Function to search for the keyword in the list, and call the corresponding function
# to output the html file
def search_keyword(output_set, list_of_applications, appl_no, invt_list, appl_name,temp_dictionary):
    application_no = [""]
    application_no = application_no * 15
    application_name = [""]
    application_name = application_name * 15
    inventors_list = []
    row = 15
    col = 25
    for i in range(row):
        inventors_list.append([])
        for j in range(col):
            inventors_list[i].append("")
    for item in output_set:
        i = 0
        j = 0
        k = 0
        l = 0
        content = [""] * 100
        for application in list_of_applications:
            flag = False
            appl_new = application.split(" ")
            for word in appl_new:  # to be checked
                if flag == True:
                    break
                if word == item:  # checks if the keyword is present in an applcaition
                    index = list_of_applications.index(application)   # gets the index no

                    application_no[i] = appl_no[index]
                    application_name[l] = appl_name[index]
                    inventors_list[j] = invt_list[index]
                    key = application_no[i]
                    content[k] = "Application No.: " + application_no[i]
                    k += 1
                    content[k] = " Application Name.:" + application_name[l]
                    k += 1
                    content[k] = "Application Abstract: " + temp_dictionary[key]                   
                    k += 1
                    tmp = "Inventors:"
                    for invt in inventors_list[j]:
                        if invt != "":
                            link = '<a href="{}.html">{}</a>'.format(invt, invt)
                            tmp = tmp + " " + link + ";"

                    content[k] = tmp
                    i += 1
                    j += 1
                    k += 1
                    l += 1
                    flag = True
                    
            output_keywords_html(content, item)


# Function to search for the inventors of each application, and 
# output the necessary information to the html file
def inventor_appl_index(invt_list, inventor_list, appl_no, appl_name,temp_dictionary):
    application_no = [""]
    application_no = application_no * 15
    application_name = [""]
    application_name = application_name * 15
    for inventor in inventor_list:
        content = [""] * 50
        i = 0
        l = 0
        k = 0
        for index in range(len(invt_list)):
            for name in invt_list[index]:
                if name.strip() == inventor.strip():
                    application_no[i] = appl_no[index]
                    key = application_no[i]
                    application_name[l] = appl_name[index]
                    content[k] = "Inventors Name:" + name
                    k += 1
                    content[k] = "Application No.: " + application_no[i] 
                    k += 1
                    content[k] = "Application Name:" + application_name[l]
                    k += 1
                    content[k] = "Application Abstract: " + temp_dictionary[key]
                    i += 1
                    l += 1
                    k += 1
        output_keywords_html(content, inventor)

#Function which checks for duplicates and deletes them

def extract_non_duplicate_inventor_info(inventor):                                                    #Fucntion to extract the inventors from the line 
    dictionary = {}
    i = 0
    length = 0
    temp_list = [""]
    temp_list = temp_list * 200
    inventor_list = [""]
    inventor_list = inventor_list * 60
    index_3 = 0
    for index_1 in range(len(inventor)):
        inventor[index_1] = inventor[index_1].replace("Inventors:", "").strip()         #removes the word inventors from the line and strip removes the empty spaces
        inventor[index_1] = inventor[index_1].split(";")                                #splits the line
        for index_2 in range(len(inventor[index_1])):                                   #for loop to iterate through the list of the the newly split words
            if inventor[index_1][index_2].find("(") != -1:                              #if a '(" is present the word  is ignored and the next iteration is carried out.
                continue
            else:
                temp_list[index_3] = inventor[index_1][index_2]
                index_3 += 1
                
    for index_4 in range(index_3):
        if index_4 % 2 == 1:
            if dictionary.get(temp_list[index_4].strip(), -1) == -1:        #Checks if the invertor alrady exists 
                dictionary[temp_list[index_4].strip()] = 1
            else:
                dictionary[temp_list[index_4].strip()] += 1                 #increments the index of the list 
    for key in dictionary.keys():
        inventor_list[i] = key
        i += 1
    return inventor_list[0:i]

#Function which creates an html file and outputs content to this file
def output_keywords_html(content, keyword):
    outfile = open(keyword + ".html", 'w')  # creates a html file called test
    message = """<html>
            <head></head>
            <body>"""
    for item in content:
        message = message + "<p>" + item + "</p>"
    message += """</body> """

    outfile.write(message)
        # writes the output to the html file
    outfile.close()


#Make the function calls
def main():
    index_url = 'http://appft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.html&r=0&p=1&f=S&l=50&Query=aanm%2F%22carnegie+mellon%22+AND+PD%2F4%2F1%2F2016-%3E6%2F30%2F2016&d=PG01'
    web_links = get_urls(index_url)
    content = get_urls_content(web_links)
    application_list = store_application(content)
    content = split_file_content(content)
    
    appl_no, inventor = read_filter_data(content)

        
    appl_name = application_name(content)
    appl_abtsract = application_abstract(content)
    invt_list = extract_inventor_info(inventor)
    
    tokens = tokenize_content(content)
    replace_dictionary = read_csv_file("./replacements.csv")
    symbols = read_symbols("./noisechar.txt")
    tokens = remove_symbols(symbols, tokens)
    tokens = replace_words(tokens, replace_dictionary)
    tokens = split_tokens(tokens)
    tokens = lemmatize_content(tokens)
    tokens = remove_stopwords(tokens)
    tf = compute_term_frequency(tokens)
    idf = compute_inverse_document_frequency(tf, tokens)
    tfidf = compute_tf_idf(tokens, tf, idf)
    keywords = choose_top_k_words(tfidf, 500)
    output_index_html(keywords, "index_milestone4")
    search_keyword(keywords, application_list, appl_no, invt_list,appl_name,appl_abtsract)

    inventor_list = extract_non_duplicate_inventor_info(inventor)
    output_index_html(inventor_list, "inventors")
    inventor_appl_index(invt_list, inventor_list, appl_no, appl_name,appl_abtsract)
    
main()