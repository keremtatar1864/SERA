import RPi.GPIO as GPIO
import dht11
import time
import datetime
from time import sleep
import pigpio 

#Raspberry PI GPIO'larını kullanıyoruz
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

in1 = 24 #Motor sürücüsünün IN1 pini GPIO 24'e tanımlı
in2 = 23 #Motor sürücüsünün IN2 pini GPIO 23'e tanımlı
en = 25  #Motor sürücüsünün EN pini GPIO 25'e tanımlı
temp1=1
ledRole=26
servo1=17
servo2=4

GPIO.setup(in1,GPIO.OUT) #Burada motor sürücüsü ve rölenin çıkış vermesi için gerekli olan OUT atama işlemlerini yapıyoruz
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.setup(ledRole,GPIO.OUT)
GPIO.output(ledRole,GPIO.HIGH)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.setup(17, GPIO.OUT)
p=GPIO.PWM(en,1000)   #Fana PWM çıkış veriyoruz
p.start(25)


pwm = pigpio.pi()   #Pigpio kütüphanesi üzerinden servo motorları kontrol ettim çünkü jitter efektini ortadan kaldırıyor
pwm.set_mode(servo1, pigpio.OUTPUT)


pwm = pigpio.pi()
pwm.set_mode(servo2, pigpio.OUTPUT)

# GPIO14 pinini kullanarak DHT11'den veri aldım
instance = dht11.DHT11(pin=14)

try:
    while True:
        result = instance.read()
        if result.is_valid():
            print("Son geçerli değişken: " + str(datetime.datetime.now()))
            print("Sıcaklık: %-3.1f C" % result.temperature)
            print("Nem: %-3.1f %%" % result.humidity)
            if result.humidity>50 and result.humidity<65:    #Verileri nem üzerinden almamın sebebi DHT11'in nem okurken çok hızlı olması fakat sıcaklık okurken hem yavaş hem de doğru değerleri vermemesi
                p.ChangeDutyCycle(35)                        #Duty cycle ayarlayarak fana belirli miktarda sinyal gönderiyoruz böylelikle istediğimiz hızda dönüyor
                pwm.set_servo_pulsewidth( servo1, 2500)      # Servo1'in konumunu ayarla
                pwm.set_servo_pulsewidth( servo2, 500)       # Servo2'nin konumunu ayarla
                GPIO.output(in1,GPIO.LOW)                    #Motor sürücüde IN1 bacağını low yap
                GPIO.output(in2,GPIO.HIGH)                   #Motor sürücüde IN2 bacağını HIGH yap
                GPIO.output(ledRole,GPIO.HIGH)               #Işığı söndür
                print("Fan %35 hızla çalışıyor")
            elif result.humidity>65 and result.humidity<75:
                p.ChangeDutyCycle(75)
                pwm.set_servo_pulsewidth( servo1, 2500)
                pwm.set_servo_pulsewidth( servo2, 500)
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.HIGH)
                GPIO.output(ledRole,GPIO.HIGH)
                print("Fan %75 hızla çalışıyor")
            elif result.humidity>75:
                p.ChangeDutyCycle(100)
                pwm.set_servo_pulsewidth( servo1, 2500)
                pwm.set_servo_pulsewidth( servo2, 500)
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.HIGH)
                GPIO.output(ledRole,GPIO.HIGH)
                print("Fan %100 hızla çalışıyor")
            else:
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.LOW)
                pwm.set_servo_pulsewidth( servo1, 1600)
                pwm.set_servo_pulsewidth( servo2, 1500)
                GPIO.output(ledRole,GPIO.LOW)          #Işığı yak
                print("Fan kapalı\n")
        time.sleep(1)

except KeyboardInterrupt:
    
    time.sleep(1)
    p.stop()
    pwm.set_PWM_dutycycle(servo1, 0)
    pwm.set_PWM_frequency( servo1, 0 )
    pwm.set_PWM_dutycycle(servo2, 0)
    pwm.set_PWM_frequency( servo2, 0 )
    
    print("Temizle")
    GPIO.cleanup()

    # SENE SONUNA KADAR OTOMATİK SULAMA SİSTEMİ VE TELEFON ÜZERİNDEN VERİ GÖRME EKLENECEK # 