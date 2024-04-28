import time
import datetime
import Recommend
import requests
import random

def duel_init(nums = 5, mins = 45, contestRating = 800, user1 = 'guy', user2 = 'guy'):
    contestMin = max(800, contestRating - 200)
    contestMax = min(3000, contestRating + 200)
    #get num problems and start timer
    if user1 == 'guy' or user2 == 'guy':
        print("not enough users supplied")
        return

    # ratings = []
    print(contestMin, contestMax)
    p = []
    for _ in range(nums):
        curRating = random.randint(int(contestMin / 100), int(contestMax / 100))
        q = Recommend.pub_recommend(rating=curRating * 100, tags=set(), num=1)
        p.append(q[0])
    #     ratings.append(random.randint(int(contestMin / 100), int(contestMax / 100)))
    # print(ratings)
    # p = Recommend.pub_recommend(rating=contestRating, tags=set(), num=1)
    print(p)
    ids = []
    solved = []
    for problem in p:
        ids.append(str(problem['contestId']) + problem["index"])
        solved.append(None)
        # print(problem)
    
    # print(ids)

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
    
    duel_check(user1, user2, ids, solved)
    print("contest has finished!")
    # print(standings)
    return p[0]

def duel_check(user1, user2, ids, sol):
    #check for new submission every x seconds, if user1 or user2 is submitter
    response1 = requests.get(f"https://codeforces.com/api/user.status?handle={user1}&from=1&count=1")
    response2 = requests.get(f"https://codeforces.com/api/user.status?handle={user2}&from=1&count=1")
    rdict1 = response1.json()['result']
    rdict2 = response2.json()['result']
    #print(rdict1[0])
    # print(str(rdict[0]['problem']['contestId']) + str(rdict[0]['problem']['index']))
    # print(ids[0])
    # print(rdict[0]['verdict'])
    for i in range(len(ids)):
        if (str(rdict1[0]['problem']['contestId']) + str(rdict1[0]['problem']['index'])) == str(ids[i]) and rdict1[0]['verdict'] == "COMPILATION_ERROR":
            if sol[i] == 1:
                print("your opponent has already solved this problem!")
            else:
                print("user1 has solved a problem!")
                sol[i] = 0
        # else:
        #     print(f"{user1} fail at problem " + str(i))
        
        if (str(rdict2[0]['problem']['contestId']) + str(rdict2[0]['problem']['index'])) == str(ids[i]) and rdict2[0]['verdict'] == "TIME_LIMIT_EXCEEDED":
            if sol[i] == 0:
                print("your opponent has already solved this problem!")
            else:
                print("user2 has solved a problem!")
                sol[i] = 1
        # else:
            # print(f"{user2} fail at problem " + str(i))
    
    # print("solved: ")
    # sol = [1, 0, 1, 0, 1]
    # print(sol)
    return sol

duel_init(5, 0.2, 1000, 'nindroid945', 'flashwhite')
# codes = ['1454B', '104064G', '263A', '344A', '599A']
# sol = [None, None, None, None, None]
# duel_check('nindroid945', 'flashwhite', codes, sol)