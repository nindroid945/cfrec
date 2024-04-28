import requests
import re
from Recommend import get_link

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
            problem["url"] = get_link(problem)
            out.append(problem)
    return out