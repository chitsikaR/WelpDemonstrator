"""Main module."""
###DemonstratorAPI
import RPi.GPIO as GPIO
import time
from time import sleep
import time
import smtplib # used for email 
import EEE3097S_project as testAPI

# define pins
btn_buzzer_email = 16 #orange
btn_email_only = 18 #purple
buzzer = 33

PWM_freq = 100 #fiddle with this if 100Hz is a bit much
global pwm # NB This is the variable that stores the PWM instance
global longPress
global buzz # for the buzzer
global buzzFlag
def setup():
    # Setup board mode
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(btn_buzzer_email, GPIO.IN, pull_up_down=GPIO.PUD_UP) # by default our thing is high
    GPIO.setup(btn_email_only, GPIO.IN, pull_up_down=GPIO.PUD_UP) # high by default
    GPIO.setup(buzzer, GPIO.OUT)

    GPIO.output(buzzer, GPIO.LOW)

    # Setup PWM channels
    global buzz
    buzz = GPIO.PWM(buzzer, PWM_freq)

    # Setup debouncing and callbacks

    GPIO.add_event_detect(btn_buzzer_email, GPIO.FALLING, callback= btn_buzzer_email_pressed, bouncetime=200) #200ms bounce time & falling edge since we were high

    GPIO.add_event_detect(btn_email_only, GPIO.FALLING, callback= btn_email_only_pressed, bouncetime= 2200)



def sendEmail():
    msmtpUser = 'testeraccforbianca@gmail.com'
    msmtpPass = 'thisismytestermail'

    toAdd = 'naidubianca@gmail.com'
    fromAdd = msmtpUser

    subject = 'demo test' 
    header = 'To: '+toAdd+'\n'+'From: '+fromAdd+'\n'+'Subject: '+subject
    body = testAPI.getTextMessage() #'From within a python script'

    print (header+'\n'+body)

    s = smtplib.SMTP('smtp.gmail.com',587)

    s.ehlo()
    s.starttls()
    s.ehlo()

    s.login(msmtpUser, msmtpPass)
    s.sendmail(fromAdd, toAdd, header +'\n\n' +body)

    s.quit()

def btn_buzzer_email_pressed(channel):
    #sendEmail()
    while GPIO.input(channel) == 0: #check if the button was released
        trigger_buzzer()
    buzz.stop()
    global buzzFlag
    buzzFlag = False

#only send email
def btn_email_only_pressed(channel):
    sendEmail()
    global buzzFlag
    buzzFlag = False


# Sound Buzzer
def trigger_buzzer():
    global buzz
    buzz.start(5) #start pwm
    buzz.ChangeFrequency(1) #set to 1 Hz


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