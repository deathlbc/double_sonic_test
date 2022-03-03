import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

TRIG = 16
ECHO = 18

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

t_count = 0.2 # 時間靈敏度
detect_range = 100  # 沒人的距離，小於此距離則表示有人在範圍內

def get_distance():
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(t_count)
    GPIO.output(TRIG, GPIO.LOW)

    while GPIO.input(ECHO) == 0:
        start = time.time()
        # print("start:", start)
    while GPIO.input(ECHO) == 1:
        end = time.time()
        # print("end", end)

    D = (end - start) * 17150
    return D

def countp():
    while True:
        a = get_distance()
        # print(f"distance {a:.1f} cm")
        print(a)
        if a < detect_range:
            print(a)
            while True:
                b = get_distance()
                print(b)
                if b > detect_range:
                    global x
                    x = x + 1  # 經過人數+1
                    print("\n\n", x, "\n\n")
                    break

x = 0
try:
    countp()

except KeyboardInterrupt:
    print("bye")
finally:
    GPIO.cleanup()
    print("total pass:",x)
