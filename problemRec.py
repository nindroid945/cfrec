import requests
import json
import random

def recommend(rating, tags, num):
    # The API endpoint
    url = "https://codeforces.com/api/problemset.problems?"

    # A GET request to the API
    response = requests.get(url)

    # Print the response
    response_json = response.json()
    #print(response_json['result']['problems'][900]['rating'])
    #print(len(response_json['result']['problems']))
    probs = []
    # tagset = set()
    # for tag in tags:
    #     tagset.add(tag)
    
    # print(tags)
    for i in range(len(response_json['result']['problems'])):
        if 'rating' in response_json['result']['problems'][i].keys() and response_json['result']['problems'][i]['rating'] == rating:
            # if 'tags' in response_json['result']['problems'][i].keys():
            curtags = set(response_json['result']['problems'][i]['tags'])
            # for tag in response_json['result']['problems'][i]['tags']:
            #     curtags.add(tag)
            #print(response_json['result']['problems'][i])
            if curtags == tags:
                probs.append(response_json['result']['problems'][i])
        #for prob in response_json['result']['problems']:
            #if prob['rating'] == 800:
                #eighthundred[prob['name']] = prob['rating']
    
    reclen = len(probs)
    recprobs = []
    print(reclen)
    for i in range(num):
        recprobs.append(probs[random.randint(0, reclen)])
    return(recprobs)
    #return "just do it bruh"