"""
   Main module
   Imports packages needed for the demonstrator to work
"""
import RPi.GPIO as GPIO
import time
from time import sleep
import time
"""package used to send email"""

import smtplib 

"""Importing python script to be implemented using the hardware"""

import EEE3097S_project as testAPI

"""Definition of pins on the Raspberry pi zero w"""

btn_buzzer_email = 16 
btn_email_only = 18 
buzzer = 33

"""Definition of global variables
   @PWM_freq changes the noise level of the buzzer
   @pwm stores the PWM instance
   @buzz is used for the buzzer
"""

PWM_freq = 100 
global pwm 
global longPress
global buzz 
global buzzFlag


def setup():
    """
       Sets up the board mode
       @GPIO.PWM sets up the PWM channels
       @.add_event_detect - sets up debouncing and callbacks
    """
    
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(btn_buzzer_email, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
    GPIO.setup(btn_email_only, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
    GPIO.setup(buzzer, GPIO.OUT)

    GPIO.output(buzzer, GPIO.LOW)

   
    global buzz
    buzz = GPIO.PWM(buzzer, PWM_freq)

    GPIO.add_event_detect(btn_buzzer_email, GPIO.FALLING, callback= btn_buzzer_email_pressed, bouncetime=200) 
    GPIO.add_event_detect(btn_email_only, GPIO.FALLING, callback= btn_email_only_pressed, bouncetime= 2200)



def sendEmail():
    """
       Sets up the email and drafts email message
       Gets textmessage from within a python script
    """
    
    msmtpUser = 'testeraccforbianca@gmail.com'
    msmtpPass = 'thisismytestermail'

    toAdd = 'naidubianca@gmail.com'
    fromAdd = msmtpUser

    subject = 'demo test' 
    header = 'To: '+toAdd+'\n'+'From: '+fromAdd+'\n'+'Subject: '+subject
    body = testAPI.getTextMessage() 

    print (header+'\n'+body)

    s = smtplib.SMTP('smtp.gmail.com',587)

    s.ehlo()
    s.starttls()
    s.ehlo()

    s.login(msmtpUser, msmtpPass)
    s.sendmail(fromAdd, toAdd, header +'\n\n' +body)

    s.quit()

def btn_buzzer_email_pressed(channel):
    """Automatically sends email and sounds the buzzer when pushbutton is pressed
       
    """
 
    while GPIO.input(channel) == 0: #check if the button was released
        trigger_buzzer()
    buzz.stop()
    global buzzFlag
    buzzFlag = False


def btn_email_only_pressed(channel):
    """"Automatically sends email only when pushbutton is pressed"""

    sendEmail()
    global buzzFlag
    buzzFlag = False

def trigger_buzzer():
    """
       Sounds the buzzer with a noise level of 1Hz
       @.start - starts the pwm
       @.ChangeFrequency sets noise level of buzzer to frequency if 1Hz
    """
    
    global buzz
    buzz.start(5) 
    buzz.ChangeFrequency(1) 


if __name__ == "__main__":
    try:

        setup()
        print("ready")
        testAPI.formatData()
        global buzzFlag
        buzzFlag = True
        while buzzFlag:
            pass
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()
