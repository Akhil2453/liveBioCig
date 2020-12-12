import RPi.GPIO as GPIO
import time

s2 = 5
s3 = 6
signal = 26
NUM_CYCLES = 10


def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(signal,GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(s2,GPIO.OUT)
    GPIO.setup(s3,GPIO.OUT)
    print("\n")
  
def loop():
    temp = 1
    while(1):  
        GPIO.output(s2,GPIO.LOW)
        GPIO.output(s3,GPIO.LOW)
        time.sleep(0.3)
        start = time.time()
        for impulse_count in range(NUM_CYCLES):
            GPIO.wait_for_edge(signal, GPIO.FALLING)
        duration = time.time() - start      #seconds to run for loop
        red  = NUM_CYCLES / duration   #in Hz
        #print("red value - ",red)
        GPIO.output(s2,GPIO.LOW)
        GPIO.output(s3,GPIO.HIGH)
        time.sleep(0.3)
        start = time.time()
        for impulse_count in range(NUM_CYCLES):
            GPIO.wait_for_edge(signal, GPIO.FALLING)
        duration = time.time() - start
        blue = NUM_CYCLES / duration
        #print("blue value - ",blue)
        GPIO.output(s2,GPIO.HIGH)
        GPIO.output(s3,GPIO.HIGH)
        time.sleep(0.3)
        start = time.time()
        for impulse_count in range(NUM_CYCLES):
            GPIO.wait_for_edge(signal, GPIO.FALLING)
        duration = time.time() - start
        green = NUM_CYCLES / duration
        #print("green value - ",green)
        time.sleep(2)
        if (((red >= 4150 or red >= 4000 or red >= 3000 or (red >= 2200 and red <= 3000) or (red >= 150 and red <= 170)) and red <= 4689) and ((blue >= 5150 or blue >= 4300 or (blue >= 2700 and blue <= 2799)) and blue <= 5699) and  ((green >= 4000 or green >= 3200 or (green >= 2200 and green <= 3100)) and green <= 4650)):
            print("Nothing Detected")
        else:
            print("red value: ", red)
            print("blue value: ", blue)
            print("green value: ", green)
             
def endprogram():
    GPIO.cleanup()

if __name__=='__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        endprogram()