import mysql.connector
import requests
import json
import os
import numpy as np
import wikipedia
# /index.py
from flask import Flask, request, jsonify, render_template, url_for


from fuzzywuzzy import fuzz 
from fuzzywuzzy import process 



class queryFunctions():

    def  __init__(self, api_keys):

        self.API_KEYS = api_keys

        self.mydb = mysql.connector.connect(
        host="localhost",
        database = 'PythonDatabase',
        user="root",
        password="password"
        )

        mysql.connector.connect()

        self.mycursor = self.mydb.cursor()


#@params: input_query: something like "who is edward snowden". The wildcard query replaces spaces with %% to expand search
#@return: returns a stored_id, either from already existing in the database or brand new created one 
    def wolframAlphaQuery(self, input_query):
        stored_id = ""
        stored_json = ""
        wildcard_query = input_query.replace(" ", "%%")
        q = "SELECT * FROM previousQueries WHERE query LIKE '%s'"
        print(q)
        query_list = self.checkDatabaseForQueries( q, wildcard_query )

        if query_list:
            stored_id, stored_json = self.loopAndFind(query_list, input_query)

        if not stored_id:
            print("stored_id is empty")
            stored_id, stored_json = self.similarQueryNotFound(input_query) #inserting and creating

        return stored_id, stored_json


    # Select from database looking for queries similar to the query
    def checkDatabaseForQueries(self, input_query, word):
        self.mycursor.execute(input_query, word)
        myresult = self.mycursor.fetchall()
        # for x in myresult:
        #   print(x)
        return myresult


    # Takes the values that are returned from it and loop through and calculate the levenshtein ratio
    def loopAndFind(self, query_list, input_query):

        for item in query_list:
            stored_query = item[1]
            stored_id = item[2]
            stored_json = item[3]
            ratio = self.levenshtein_ratio_and_distance(stored_query, input_query, ratio_calc = True)
            print('Levenshtein Ratio: ', ratio)

            if(ratio >= 0.8):
                print("Match found --- OG Query: ", input_query, " foundQuery: ", stored_query)
                # similarQueryFound = True
                # foundID = stored_id
                # break
                return stored_id, stored_json
        return None, None


    def similarQueryNotFound(self, input_query):

        # response_dictionary = self.wolframDirectQuery(input_query)
        # stored_id = response_dictionary['queryresult']['id']

        response_value = self.wolframDirectQuery(input_query)
        stored_id = "idk"

        # path_stored_id = stored_id + ".json"
        # path = os.path.join('json_queries/', path_stored_id)

        # # with open(path, 'w') as fp:
        # #     json.dump(response_dictionary, fp)

        # Insert into the database
        sql = "INSERT INTO previousQueries (query, id, json) VALUES (%s, %s, %s)"
        val = (input_query, stored_id, response_value)

        self.mycursor.execute(sql, val)
        self.mydb.commit()
        return stored_id, response_value


    
    def wolframDirectQuery(self, input_query):
        print("Brand new query, searching online. ")
        # payload = {'appid': self.API_KEY , 'output': 'json', 'input': input_query}
        # response = requests.get('http://api.wolframalpha.com/v2/query', params = payload)
        # response_dictionary = response.json()

        querying = True
        returnVal = ""
        while(querying == True):

            for KEY in self.API_KEYS:
                # this is for v2 but i don't know how to parse it yet...

                # payload = {'appid': KEY , 'output': 'json', 'input': input_query}
                # response = requests.get('http://api.wolframalpha.com/v2/query', params = payload)
                # response_dictionary = response.json()
                print("THIS IS THE KEY, ", KEY)
                payload = {'appid': KEY , 'output': 'json', 'i': input_query}
                response = requests.get('https://api.wolframalpha.com/v1/result', params = payload)

                returnVal = response.content

                # isError = fuzz.ratio("Error 1: Invalid appid", returnVal) 
                # yeet = fuzz.ratio("b'No short answer available'", returnVal) 

                # print(isError)
                # print(yeet)

                encoding = 'utf-8'
                string_returnVal = returnVal.decode(encoding)

                res_error = string_returnVal == 'Error 1: Invalid appid'
                res_null = string_returnVal == 'No short answer available'
                noAnswer = string_returnVal == 'Wolfram|Alpha did not understand your input'
                print("reserror: ", res_error)

                print(type(returnVal))

                if( not res_error ):
                    querying = False
                    break

                
        if( res_null ):
            returnVal = "Hm... I'm not really sure. Try rephrasing the question."

        if( noAnswer ):
            returnVal = "Sorry boss...I don't think I understand."
        # Commented out because might not be the most accurate
        # GeneralInfo = response_dictionary['queryresult']['pods'][1]['subpods'][0]['plaintext']
        # print(GeneralInfo)
        # print(response_dictionary)
        print(response.content)
        return (returnVal)


        

# This is the actual algorithm to calculate the similarity between two different strings
    def levenshtein_ratio_and_distance(self, s, t, ratio_calc = False):
        """ levenshtein_ratio_and_distance:
            Calculates levenshtein distance between two strings.
            If ratio_calc = True, the function computes the
            levenshtein distance ratio of similarity between two strings
            For all i and j, distance[i,j] will contain the Levenshtein
            distance between the first i characters of s and the
            first j characters of t
        """
        # Initialize matrix of zeros
        rows = len(s)+1
        cols = len(t)+1
        distance = np.zeros((rows,cols),dtype = int)

        # Populate matrix of zeros with the indeces of each character of both strings
        for i in range(1, rows):
            for k in range(1,cols):
                distance[i][0] = i
                distance[0][k] = k

        # Iterate over the matrix to compute the cost of deletions,insertions and/or substitutions    
        for col in range(1, cols):
            for row in range(1, rows):
                if s[row-1] == t[col-1]:
                    cost = 0 # If the characters are the same in the two strings in a given position [i,j] then the cost is 0
                else:
                    # In order to align the results with those of the Python Levenshtein package, if we choose to calculate the ratio
                    # the cost of a substitution is 2. If we calculate just distance, then the cost of a substitution is 1.
                    if ratio_calc == True:
                        cost = 2
                    else:
                        cost = 1
                distance[row][col] = min(distance[row-1][col] + 1,      # Cost of deletions
                                    distance[row][col-1] + 1,          # Cost of insertions
                                    distance[row-1][col-1] + cost)     # Cost of substitutions
        if ratio_calc == True:
            # Computation of the Levenshtein Distance Ratio
            Ratio = ((len(s)+len(t)) - distance[row][col]) / (len(s)+len(t))
            return Ratio
        else:
            print(distance) # Uncomment if you want to see the matrix showing how the algorithm computes the cost of deletions,
            # insertions and/or substitutions
            # This is the minimum number of edits needed to convert string a to string b
            return "The strings are {} edits away".format(distance[row][col])


    def search_wiki(self, keyword=''):
        # running the query
        searchResults = wikipedia.search(keyword)
        # If there is no result, print no result
        if not searchResults:
            print("No result from Wikipedia")
            return
        # Search for page... try block 
        try:
            page = wikipedia.page(searchResults[0])
        except wikipedia.DisambiguationError as err:
            # Select the first item in the list
            page = wikipedia.page(err.options[0])
        #encoding the response to utf-8
        wikiTitle = str(page.title.encode('utf-8'))
        wikiSummary = str(page.summary.encode('utf-8'))
        # printing the result
        print(wikiSummary)
        return wikiSummary




















