import requests
import json
import time

import problemRec

def main():
    start_time = time.time()

    # The API endpoint
    url = "https://codeforces.com/api/problemset.problems?"

    # A GET request to the API
    response = requests.get(url)

    # Print the response
    response_json = response.json()
    #print(response_json['result']['problems'][900]['rating'])
    #print(len(response_json['result']['problems']))
    eighthundred = []
    for i in range(len(response_json['result']['problems'])):
        if 'rating' in response_json['result']['problems'][i].keys() and response_json['result']['problems'][i]['rating'] == 800:
            print(response_json['result']['problems'][i])
            eighthundred.append(response_json['result']['problems'][i])
        #for prob in response_json['result']['problems']:
            #if prob['rating'] == 800:
                #eighthundred[prob['name']] = prob['rating']

    print(eighthundred)
#print(response_json['result']['problems'])
#input_dict = json.load(response)
#output_dict = [x for x in response_json['result']['problems'] if x['rating'] == '800']
#print(output_dict)

    end_time = time.time()
    exec_time = start_time - end_time
    print(exec_time)
    print("Hello World")
    p = problemRec.recommend()
    print(p)

main()