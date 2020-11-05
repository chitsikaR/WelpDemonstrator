"""Imports packages needed for the demonstrator to work"""
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

    GPIO.add_event_detect(btn_buzzer_email, GPIO.FALLING, callback= btn_buzzer_email_pressed, bouncetime=200) 
    GPIO.add_event_detect(btn_email_only, GPIO.FALLING, callback= btn_email_only_pressed, bouncetime= 2200)



def sendEmail():
    """
       Sets up the email and drafts email message
       Gets textmessage from within a python script
    """
    # email sender
    msmtpUser = 'testeraccforbianca@gmail.com'
    msmtpPass = 'thisismytestermail'

    # name of person who sent the distress signal
    username = 'Laurentia'

    # recipient of distress signal
    toAdd = 'naidubianca@gmail.com'
    fromAdd = msmtpUser

    subject = 'DISTRESS MESSAGE FORM WELP' 
    header = 'To: '+ toAdd + '\n' + 'From: ' + fromAdd + '\n' + 'Subject: ' + subject

    # email body
    text_message = '***DISTRESS SIGNAL*** \n'
    text_message = text_message + username + ' is in danger now at:\n'
    body = text_message + testAPI.getTextMessage() 

    print (header + '\n' + body)

    message = smtplib.SMTP('smtp.gmail.com', 587)

    message.ehlo()
    message.starttls()
    message.ehlo()

    message.login(msmtpUser, msmtpPass)
    message.sendmail(fromAdd, toAdd, header +'\n\n' +body)

    message.quit()

def btn_buzzer_email_pressed(channel):
    """Automatically sends email and sounds the buzzer when pushbutton is pressed
       
    """
 
    while GPIO.input(channel) == 0: #check if the button was released
        trigger_buzzer()

    # when button is released, turn off buzzer
    GPIO.output(buzzer, GPIO.LOW)

    global buzzFlag
    buzzFlag = False


def btn_email_only_pressed(channel):
    """"Automatically sends email only when pushbutton is pressed"""

    sendEmail()
    global buzzFlag
    buzzFlag = False

def trigger_buzzer():
    """
       Sounds the buzzer with maximum output noise level 
    """
    
    GPIO.output(buzzer, GPIO.HIGH)


if __name__ == "__main__":
    try:

        setup()
        print("ready")
        global buzzFlag
        buzzFlag = True
        # true indicates program is still running
        # flag is set to false when buttons are pressed
        while buzzFlag:
            testAPI.formatData()

    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()
