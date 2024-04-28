import time
import problemRec

def main():
    start_time = time.time()

    rating = 800
    tags = {'math', 'implementation', 'blah'}
    num_rec = 3
    p = problemRec.recommend(rating, tags, num_rec)
    print(p)

    end_time = time.time()
    exec_time = start_time - end_time
    print(exec_time)
    

main()