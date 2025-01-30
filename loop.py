import time

def time_passed(start):
    elapsed_time = time.time() - start
    hours = int(elapsed_time // 3600)
    minutes = int((elapsed_time % 3600) // 60)
    seconds = int(elapsed_time % 60)

    return (hours, minutes, seconds)

start = time.time()

i = 0
for i in range(1_000_000):
    i += 1

elapsed = time_passed(start)
print(elapsed)