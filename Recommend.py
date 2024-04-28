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
    
    # fetch the 5 tags that have the least work in it
    a = [[key, tag_count[key]] for key in tag_count]
    a.sort(key=lambda x: x[1])
    tags = a[:min(5, len(a))]

    # get potential recommend problems
    tagged = []
    untagged = []

    for pid, problem in data.items():
        if "rating" in problem and avg_difficulty-200 <= problem["rating"] <= max_difficulty+200 and pid not in solved:
            for t in problem["tags"]:
                if t in tags:
                    tagged.append(problem) # one of the least-done tags
                    break
            else:
                untagged.append(problem) # a never-done tag
    
    if len(tagged) == 0 and len(untagged) == 0:
        return "No problems found."
    elif len(tagged) == 0:
        return untagged[:min(5, len(untagged))]
    elif len(untagged) == 0:
        return tagged[:min(5, len(tagged))]
    
    # randomly pick some 5 problems from both tagged and untagged
    out = []
    while len(out) < min(5, len(untagged)+len(tagged)):
        choice = random.randint(0,1)
        if choice == 0: # untagged
            toadd = untagged[random.randint(0, len(untagged)-1)]
            if toadd not in out:
                out.append(toadd)
        else:
            toadd = tagged[random.randint(0, len(tagged))]
            if toadd not in out:
                out.append(toadd)
    return out
        
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