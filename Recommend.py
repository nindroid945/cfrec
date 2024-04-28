import requests
import json
import random

def get_link(problem: dict) -> str:
    i = problem["contestId"]
    j = problem["index"]
    return f"https://codeforces.com/problemset/problem/{i}/{j}"

def profile(handle: str):
    response = requests.get(f"https://codeforces.com/api/user.info?handles={handle}")
    return response.json()

def get_id(problem: dict) -> str:
    return str(problem["contestId"])+str(problem["index"])

def smart_recommend(handle: str) -> list:
    response = requests.get(f"https://codeforces.com/api/user.status?handle={handle}")
    response_json = response.json()

    tot_difficulty = 0
    max_difficulty = float("-inf")
    tag_count = dict()
    solved = set()

    for number in response_json["result"]:
        if "rating" not in number["problem"] or number["problem"]["tags"] == []:
            continue
        pid = get_id(number["problem"])
        if number["verdict"] == "OK" and pid not in solved:
            tot_difficulty += number["problem"]["rating"]
            if number["problem"]["rating"] > max_difficulty:
                max_difficulty = number["problem"]["rating"]
            solved.add(pid)
            for t in number["problem"]["tags"]:
                if t in tag_count:
                    tag_count[t] += 1
                else:
                    tag_count[t] = 1

    avg_difficulty = tot_difficulty // len(solved)
    #print(f"{handle}'s average difficulty solved is {avg_difficulty}")

    with open("problemset.json", "r") as problemset:
        data = json.load(problemset)

    # get potential recommend problems
    pool = []

    for pid, problem in data.items():
        if "rating" in problem and avg_difficulty-200 <= problem["rating"] <= max_difficulty+100 and pid not in solved:
            problem["url"] = get_link(problem)
            pool.append(problem)
    
    if len(pool) < 5:
        return pool
    
    # randomly pick some 5 problems from both tagged and untagged
    out = []
    while len(out) < 5:
        toadd = pool[random.randint(0, len(pool)-1)]
        if toadd not in out:
            out.append(toadd)
    return out
        
def pub_recommend(rating: int, tags: set, num: int):
    # The API endpoint
    # A GET request to the API
    response = requests.get("https://codeforces.com/api/problemset.problems?")

    # Print the response
    response_json = response.json()

    pool = []

    for problem in response_json["result"]["problems"]:
        if ("rating" in problem and problem["rating"] == rating) and (tags.issubset(set(problem["tags"]))):
            problem["url"] = get_link(problem)
            pool.append(problem)

    if len(pool) == 0:
        return "No problems found."
    out = []
    while len(out) < min(num, len(pool)):
        toadd = pool[random.randint(0, len(pool)-1)]
        if toadd not in out:
            out.append(toadd) # random inclusive [0, n-1]
    return out