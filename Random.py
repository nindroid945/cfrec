import requests
import random
from Recommend import get_link

from datetime import datetime

def daily():
    response = requests.get(f"https://codeforces.com/api/problemset.problems?")
    response_json = response.json()
    pool = []
    for problem in response_json["result"]["problems"]:
        if "rating" in problem and problem["rating"] <= 1500:
            problem["url"] = get_link(problem)
            pool.append(problem)
    index = hash(datetime.today().strftime('%Y-%m-%d')) % len(pool)
    return pool[index]