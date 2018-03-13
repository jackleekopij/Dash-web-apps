import time


def countdown(time_remaining):
    time.sleep(1)
    if time_remaining > 0:
        return time_remaining - 1
    else:
        return "Time Over"

