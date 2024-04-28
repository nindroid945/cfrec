import time
import Recommend

def main():
    start_time = time.time()
    rating = 800
    tags = {'math', 'implementation'}
    num_rec = 3
    problems = Recommend.recommend(rating, tags, num_rec)
    for p in problems:
        print(p)
        print(Recommend.get_link(p))

    end_time = time.time()
    exec_time = end_time - start_time
    print(exec_time)

    test = Recommend.smart_recommend("flashwhite")
    for t in test:
        print(t)
    

main()