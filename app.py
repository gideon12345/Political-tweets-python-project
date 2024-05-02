import time
import multiprocessing
# A CPU heavy calculation, just
# as an example. This can be
# anything you like
def heavy(n, myid):
    for x in range(1, n):
        for y in range(1, n):
            x**y
    print(myid, "is done")
def doit(n):
    heavy(500, n)
def pooled(n):
    # By default, our pool will have
    # numproc slots
    with multiprocessing.Pool() as pool:
       pool.map(doit, range(n))
if __name__ == "__main__":
    start = time.time()
    pooled(80)
    end = time.time()
    print("Took: ", end - start)