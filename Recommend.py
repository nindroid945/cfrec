import requests
import json
import random
BIGNUMBER = 10e9

def get_link(problem: dict) -> str:
    i = problem["contestId"]
    j = problem["index"]
    return f"https://codeforces.com/problemset/problem/{i}/{j}"

def profile(handle: str):
    response = requests.get(f"https://codeforces.com/api/user.info?handles={handle}")
    return response.json()

def id(problem: dict) -> str:
    return str(problem["contestId"]+str(problem["index"]))

def smart_recommend(handle: str):
    response = requests.get(f"https://codeforces.com/api/user.status?handle={handle}&from=1&count={BIGNUMBER}")
    response_json = response.json()

    tot_difficulty = 0
    max_difficulty = float("-inf")
    tag_count = dict()
    solved = set()

    for problem in response_json["result"]["problems"]:
        id = id(problem)
        if problem["verdict"] == "OK" and id not in solved:
            tot_difficulty += problem["rating"]
            if problem["rating"] > max_difficulty:
                max_difficulty = problem["rating"]
            solved.add(id)
            for t in problem["tags"]:
                if t in tag_count:
                    tag_count[t] += 1
                else:
                    tag_count[t] = 1
    avg_difficulty = tot_difficulty // len(solved)

    # fetch 3 tags that have the least work in it
    
    print(f"{handle}'s average difficulty solved is {avg_difficulty}")

def recommend(rating: int, tags: set, num: int):
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