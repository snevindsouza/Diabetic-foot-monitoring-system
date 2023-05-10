import machine
import utime

# configure PWM and ADC pins for sensor 1
pwm_pin1 = machine.Pin(0, machine.Pin.OUT)
adc_pin1 = machine.ADC(26)

# configure ADC pin for sensor 2
adc_pin2 = machine.ADC(27)

# set up variables for averaging
sample_count = 128
total_voltage1 = 0
total_voltage2 = 0

while True:
    j=0
    total_voltage1=0
    total_voltage2=0
    for i in range(sample_count):
        if i > 20 and i < 108:
            j+=1
            pwm_pin1.on()        
            utime.sleep_us(100)
            voltage_reading1 = adc_pin1.read_u16() * 3.3 / 65535
            total_voltage1 += voltage_reading1
            voltage_reading2 = adc_pin2.read_u16() * 3.3 / 65535
            total_voltage2 += voltage_reading2
            pwm_pin1.off()
            utime.sleep_us(100)
    average_voltage1 = total_voltage1 / j
    average_voltage2 = total_voltage2 / j
    print("Average voltage sensor 1:", average_voltage1)
    print("Average voltage sensor 2:", average_voltage2)
    utime.sleep(2)
