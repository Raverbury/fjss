import time
import numpy as np

SIZE = 10000000

arr = []
dic = dict()
for i in range(SIZE):
    arr.append(0)
    dic[i] = 0
arr = np.array(arr, dtype=np.int32)

start = time.time()
for i in range(SIZE):
    z = arr[i]
end = time.time()
print(f"Took {end - start} seconds for list access")

start = time.time()
for i in range(SIZE):
    z = dic[i]
end = time.time()
print(f"Took {end - start} seconds for dict access")