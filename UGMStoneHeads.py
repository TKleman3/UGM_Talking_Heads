import time
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
import lib8relind as relay
import RPi.GPIO as GPIO
from adafruit_servokit import ServoKit

i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c, address=0x40)

GPIO.setmode(GPIO.BCM)
#channel_list = [6,13,19,26]
#GPIO.setup(channel_list,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
'''
#Audio channels
audio_01 = 26
audio_02 = 19
audio_03 = 13
audio_05 = 6
'''
#Head servo channels
kit = ServoKit(channels=16)
head_01 = kit.servo[0]
head_02 = kit.servo[1]
head_03 = kit.servo[2]
head_05 = kit.servo[4]

def head_move(start,end,delta):
    print("calling head movement!")
    incMove = (end-start)/100.0
    incTime = delta/100.0
    for x in range(100):
        head_01.angle = start + x*incMove
        head_02.angle = start + x*incMove
        head_03.angle = start + x*incMove
        head_05.angle = start + x*incMove
        time.sleep(incTime)
def head_reset(start,end,delta):
    incMove = (end-start)/100.0
    incTime = delta/100.0
    for x in range(100):
        head_01.angle = end - x*incMove
        head_02.angle = end - x*incMove
        head_03.angle = end - x*incMove
        head_05.angle = end - x*incMove
        time.sleep(incTime)
#relays for lights and audio
def audio_trigger():
    relay.set(0,1,1)
    time.sleep(0.1)
    relay.set(0,1,0)
    
def audio_reset():
    relay.set(0,2,1)
    time.sleep(0.5)
    relay.set(0,2,0)
#Relays for head lights    
'''
head_01_light = 5
head_02_light = 6
head_03_light = 7
head_05_light = 8

def light_on(head):
    relay.set(0,head,1)

def light_off(head):
    relay.set(0,head,0)
'''
#countdown timer
seconds = 90
my_timer = seconds
audio_reset()
playing = True
while playing:    
    if my_timer <= 0:        
        head_move(0,90,7)
        audio_trigger()
        #audio_reset()
        my_timer = seconds
    '''
    #head 01 lights with audio
    if GPIO.input(audio_01):
        #print("head 01 high")
        light_on(head_01_light)
    else:
        #print("head_01 low")
        light_off(head_01_light)        
        
    #head 02 lights with audio    
    if GPIO.input(audio_02):
        #print("head 02 high")
        light_on(head_02_light)
    else:        
        light_off(head_02_light)
        #print("head_02 low")        
    #head 03 lights with audio    
    if GPIO.input(audio_03):
        #print("head 03 high")
        light_on(head_03_light)
    else:        
        light_off(head_03_light)
        #print("head_03 low")        
    #head 05 lights with audio    
    if GPIO.input(audio_05):
        #print("head 05 high")
        light_on(head_05_light)
    else:        
        light_off(head_05_light)
        #print("head_05 low")
    '''
    time.sleep(1)    
    my_timer -= 1
    print(str(my_timer) + "seconds left in countdown")
    if my_timer == (seconds/9):
        head_reset(0,90,7)    


GPIO.cleanup()
pca.deinit()
pca.reset()