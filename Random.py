import requests
import random

def daily():
    response = requests.get(f"https://codeforces.com/api/problemset.problems?")
    response_json = response.json()
    pool = []
    for problem in response_json["result"]["problems"]:
        if "rating" in problem and problem["rating"] <= 1500:
            pool.append(problem)
    return pool[random.randint(0, len(pool)-1)]