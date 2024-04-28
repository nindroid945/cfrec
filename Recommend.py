import requests
import json
import random

def get_link(problem: dict) -> str:
    i = problem["contestId"]
    j = problem["index"]
    return f"https://codeforces.com/problemset/problem/{i}/{j}"

def recommend(rating, tags, num):
    # The API endpoint
    # A GET request to the API
    response = requests.get("https://codeforces.com/api/problemset.problems?")

    # Print the response
    response_json = response.json()

    pool = []

    for problem in response_json["result"]["problems"]:
        if ("rating" in problem and problem["rating"] == rating) and (set(problem["tags"]) == tags):
            pool.append(problem)

    if len(pool) == 0:
        return "No problems found."
    out = []
    while len(out) < min(num, len(pool)):
        toadd = pool[random.randint(0, len(pool)-1)]
        if toadd not in out:
            out.append(toadd) # random inclusive [0, n-1]
    return out