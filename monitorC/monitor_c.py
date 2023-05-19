import random
import time


def main():
    while True:
        print("\n------------------------------------\n" +
              "\nCPU: \n")
        cpu_usage = random.random()
        print(cpu_usage)
        time.sleep(1)


if __name__ == "__main__":
    main()

