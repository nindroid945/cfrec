import requests
import re

def search(query: str):
    response = requests.get("https://codeforces.com/api/problemset.problems?")
    response_json = response.json()

    terms = query.lower().split()
    out = []
    for problem in response_json["result"]["problems"]:
        for t in terms:
            if re.search(t, problem["name"].lower()) == None:
                break
        else:
            out.append(problem)
    return out