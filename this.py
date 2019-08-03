from mq import *
import sys, time
import RPi.GPIO as GPIO
import smtplib
ok=0
server = smtplib.SMTP('smtp.gmail.com',587)
server.connect("smtp.gmail.com",587)
server.ehlo()
server.starttls()
server.ehlo()
server.login("","")

msg = "Atentie!!! Gaze inflamabile sau fum au fost detectate de catre sistem"
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
try:
    print("Press CTRL+C to abort.")
    
    mq = MQ();
    while True:
        perc = mq.MQPercentage()
        sys.stdout.write("\r")
        sys.stdout.write("\033[K")
        if perc["CO"] > 1200 or perc["SMOKE"] > 1500 or perc["GAS_LPG"] > 1200:
            if ok==0:
                ok=1
                server.sendmail("Eu","silviu_dinu@yahoo.com",msg + "\n\n\nIn momentul in care acest mail a fost trimis, au fost inregistrate: \nGAZ = " + str(perc["GAS_LPG"]) + " ppm, \nFUM = " + str(perc["SMOKE"])  +" ppm, \nCO = "+ str(perc["CO"])  + " ppm")
            GPIO.output(18,GPIO.HIGH)
        sys.stdout.write("GAZ: %g ppm, CO: %g ppm, Smoke: %g ppm" % (perc["GAS_LPG"], perc["CO"], perc["SMOKE"]))
        sys.stdout.flush()
        time.sleep(0.1)
        GPIO.output(18,GPIO.LOW)

except:
    logging.debug.message("caca")
    print("\nAbort by user")
    GPIO.output(18,GPIO.LOW)
