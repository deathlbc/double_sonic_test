import RPi.GPIO as GPIO
import time
import threading

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

detect_range = 100
t_count = 0.1 # 時間靈敏度
# 裡機
TRIG = 16
ECHO = 18
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# 外機
TRIG2 = 22
ECHO2 = 24
GPIO.setup(TRIG2, GPIO.OUT)
GPIO.setup(ECHO2, GPIO.IN)

# 裡機距離
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

    D1 = (end - start) * 17150
    return D1

# 外機距離
def get_distance2():
    GPIO.output(TRIG2, GPIO.HIGH)
    time.sleep(t_count)
    GPIO.output(TRIG2, GPIO.LOW)

    while GPIO.input(ECHO2) == 0:
        start = time.time()
        # print("start:", start)
    while GPIO.input(ECHO2) == 1:
        end = time.time()
        # print("end", end)

    D2 = (end - start) * 17150
    return D2

def countp():
    while True:
        a = get_distance()  # 裡
        a2 = get_distance2()  #外
        # print(f"distance {a:.1f} cm")
        print(a,"step 0", a2)
        if a < detect_range and a2 > detect_range:
            print(a," ===內先感測到了=== ",a2)
            while True:
                b = get_distance()
                b2 = get_distance2()
                # print(f"distance {a:.1f} cm")
                print(b, "step 1", b2)
                if b > detect_range and b2 > detect_range:
                    print(b, " ======== ", b2)
                    global x
                    x = x + 1
                    print("\n",f"有人離開，目前離開人數{x}人", "\n")
                    break
        elif a2 < detect_range and a > detect_range:
            print(a," ===外先感測到了=== ",a2)
            while True:
                b = get_distance()
                b2 = get_distance2()
                # print(f"distance {a:.1f} cm")
                print(b, "+step 2+", b2)
                if b > detect_range and b2 > detect_range:
                    print(b, " ======== ", b2)
                    global y
                    y = y + 1
                    print("\n",f"有人進入，目前進入人數{y}人", "\n")
                    break
x = 0
y = 0
try:
    countp()

except KeyboardInterrupt:
    print("bye")
finally:
    GPIO.cleanup()
    print("total pass:",y)
    print("total out:", x)
