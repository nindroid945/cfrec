import time
import datetime
import Recommend
import requests
import random

def duel_init(nums = 5, mins=45, contestRating = 800, user1 = None, user2 = None):
    contestMin = max(800, contestRating - 200)
    contestMax = min(3000, contestRating + 200)
    #get num problems and start timer
    if not (user1 and user2):
        return "Not enough users given."

    #print(contestMin, contestMax)
    problems = []
    while len(problems) < nums:
        curRating = random.randint(contestMin // 100, contestMax // 100)
        q = Recommend.pub_recommend(rating=curRating * 100, tags=set(), num=1)
        if q not in problems:
            problems.append(q[0])
    
    #print(problems)
    ids = []
    solved = []
    for problem in problems:
        ids.append(str(problem['contestId']) + str(problem["index"]))
        solved.append(None)
        # print(problem)
    
    print(ids)

    # x = input()
    # print(x)

    # duel_check("nindroid945", "rando", ids)

    # total_seconds = mins * 60
    # intervalTime = 5
    # interval = intervalTime
    # print(solved)
    # while total_seconds > 0:
    #     # Timer represents time left on countdown
    #     timer = datetime.timedelta(seconds = total_seconds)
        
    #     # Prints the time left on the timer
    #     print(timer)
    #     # print(interval)
        
    #     if interval == 0:
    #         standings = duel_check(user1, user2, ids, solved)
    #         interval = intervalTime
 
    #     # Delays the program one second
    #     time.sleep(1)
 
    #     # Reduces total time by one second
    #     total_seconds -= 1
    #     interval -= 1
    
    # duel_check(user1, user2, ids, solved)
    print("contest has begun!")
    #print(problems)
    return problems

def duel_check(user1, user2, ids, sol):
    #check for new submission every x seconds, if user1 or user2 is submitter

    # intervalTime = 5
    # interval = intervalTime
    # while interval > 0:
    #     time.sleep(1)
    #     interval -= 1
    # print("checking duel")
    response1 = requests.get(f"https://codeforces.com/api/user.status?handle={user1}&from=1&count=1")
    response2 = requests.get(f"https://codeforces.com/api/user.status?handle={user2}&from=1&count=1")
    rdict1 = response1.json()['result']
    rdict2 = response2.json()['result']
    prob = None
    user = None
    for i in range(len(ids)): # for all problems in the contest, check
        if (str(rdict1[0]['problem']['contestId']) + str(rdict1[0]['problem']['index'])) == str(ids[i]) and rdict1[0]['verdict'] == "OK":
            if sol[i] != 1:
                sol[i] = 0
                prob = i
                user = 0
        if (str(rdict2[0]['problem']['contestId']) + str(rdict2[0]['problem']['index'])) == str(ids[i]) and rdict2[0]['verdict'] == "OK":
            if sol[i] != 0:
                sol[i] = 1
                prob = i
                user = 1


    """
    if sol[i] == 1:
        #print("your opponent has already solved this problem!")
    else:
        sol[i] = 0
        #print("user1 has solved a problem!")
    if sol[i] == 0:
        #print("your opponent has already solved this problem!")
    else:
        sol[i] = 1
        #print("user2 has solved a problem!")
    """
    # prob = 0
    # user = 0
    return prob, user # array of length nums representing who solved which problems.

# duel_init(5, 0.5, 1000, 'nindroid945', 'flashwhite')
# codes = ['1454B', '104064G', '263A', '344A', '599A']
# sol = [None, None, None, None, None]
# duel_check('nindroid945', 'flashwhite', codes, sol)