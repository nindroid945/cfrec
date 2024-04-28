import time
import problemRec

def main():
    start_time = time.time()

    p = problemRec.recommend(800, {'math'}, 3)
    print(p)

    end_time = time.time()
    exec_time = start_time - end_time
    print(exec_time)
    

main()