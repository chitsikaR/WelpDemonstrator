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

PWM_freq = 100 
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

    # Setup debouncing and callbacks
    GPIO.add_event_detect(btn_buzzer_email, GPIO.FALLING, callback= btn_buzzer_email_pressed, bou$

    GPIO.add_event_detect(btn_email_only, GPIO.FALLING, callback= btn_email_only_pressed, bouncet$


# function to compose and send email
def sendEmail():
    # set up account that will send the email
    msmtpUser = 'testeraccforbianca@gmail.com'
    msmtpPass = 'thisismytestermail'

    # name of the person who sends the distress signal 
    username = 'Laurentia'

    # email recipient can be set up via web app
    toAdd = 'naidubianca@gmail.com' # user can add their own target email address
    fromAdd = msmtpUser

    # email subject line
    subject = 'DISTRESS MESSAGE FROM WELP' 
    header = 'To: '+toAdd+'\n'+'From: '+fromAdd+'\n'+'Subject: '+subject

    # email body with distres message
    text_message = '***DISTRESS SIGNAL*** \n'
    text_message = text_message + username + ' is in danger now at:\n'
    body = text_message + testAPI.getTextMessage() 

    print (header + '\n' + body)

    message = smtplib.SMTP('smtp.gmail.com', 587)

    message.ehlo()
    message.starttls()
    message.ehlo()

    message.login(msmtpUser, msmtpPass)
    message.sendmail(fromAdd, toAdd, header + '\n\n' + body)

    message.quit()

# controls what happens when button1 is pressed
def btn_buzzer_email_pressed(channel):
    sendEmail()
    while GPIO.input(channel) == 0: #check if the button was released
        trigger_buzzer()
    GPIO.output(buzzer, GPIO.LOW)

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



