import random
import time


def main():
    while True:
        print("\n------------------------------------\n" +
              "\nCPU: \n")
        cpu_usage = random.random()
        print(cpu_usage)
        time.sleep(2)

def get_number(prev=None, direction=None, range=0.1):
    if prev is None:
        cpu_usage = random.random()
        return cpu_usage
    else:
        if direction is None:
            lower_limit = prev - range
            upper_limit = prev + range

            cpu_usage = random.uniform(lower_limit, upper_limit)
            return cpu_usage
        elif direction == "down":
            lower_limit = prev
            upper_limit = prev - range
            
            cpu_usage = random.uniform(lower_limit, upper_limit)
            return cpu_usage
        elif direction == "up":
            lower_limit = prev
            upper_limit = prev + range

            cpu_usage = random.uniform(lower_limit, upper_limit)
            return cpu_usage

if __name__ == "__main__":
    main()