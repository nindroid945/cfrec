import time
import datetime
import Recommend
import requests

def duel_init(nums = 5, mins = 45, contestRating = 800, user1 = 'guy', user2 = 'guy'):
    #get num problems and start timer
    if user1 == 'guy' or user2 == 'guy':
        print("not enough users supplied")
        return
    p = Recommend.pub_recommend(rating=contestRating, tags={'implementation'}, num=nums)
    ids = []
    solved = []
    for problem in p:
        ids.append(str(problem['contestId']) + problem["index"])
        solved.append(None)
        # print(problem)
    
    print(ids)

    # x = input()
    # print(x)

    # duel_check("nindroid945", "rando", ids)

    total_seconds = mins * 60
    intervalTime = 5
    interval = intervalTime
    while total_seconds > 0:
        # Timer represents time left on countdown
        timer = datetime.timedelta(seconds = total_seconds)
        
        # Prints the time left on the timer
        print(timer)
        # print(interval)
        
        if interval == 0:
            duel_check(user1, user2, ids, solved)
            interval = intervalTime
 
        # Delays the program one second
        time.sleep(1)
 
        # Reduces total time by one second
        total_seconds -= 1
        interval -= 1
    
    duel_check(user1, user2, ids, solved)
    print("contest has finished!")

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
                print("this shit alr solved brother. by ur opp!")
            else:
                print("user1 has solved a problem!")
                sol[i] = 0
        else:
            print(f"{user1} fail at problem " + str(i))
        
        if (str(rdict2[0]['problem']['contestId']) + str(rdict2[0]['problem']['index'])) == str(ids[i]) and rdict2[0]['verdict'] == "TIME_LIMIT_EXCEEDED":
            if sol[i] == 0:
                print("this shit alr solved brother. by ur opp!")
            else:
                print("user2 has solved a problem!")
                sol[i] = 1
        else:
            print(f"{user2} fail at problem " + str(i))
    
    print("solved: ")
    print(sol)

duel_init(5, 0.5, 800, 'nindroid945', 'flashwhite')
# codes = ['1454B', '104064G', '263A', '344A', '599A']
# sol = [None, None, None, None, None]
# duel_check('nindroid945', 'flashwhite', codes, sol)