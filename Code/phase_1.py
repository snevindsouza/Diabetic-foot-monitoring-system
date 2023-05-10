import machine
import utime

# configure PWM and ADC pins for sensor 1
pwm_pin1 = machine.Pin(0, machine.Pin.OUT)
adc_pin1 = machine.ADC(26)

# configure ADC pins for sensors 2 and 3
adc_pin2 = machine.ADC(27)
adc_pin3 = machine.ADC(28)

# set up variables for averaging
sample_count = 128
total_voltage1 = 0
total_voltage2 = 0
total_voltage3 = 0

while True:
    j=0
    total_voltage1=0
    total_voltage2=0
    total_voltage3=0
    for i in range(sample_count):
        if i > 20 and i < 108:
            j+=1
            pwm_pin1.on()        
            utime.sleep_us(100)
            voltage_reading1 = adc_pin1.read_u16() * 3.3 / 65535
            total_voltage1 += voltage_reading1
            voltage_reading2 = adc_pin2.read_u16() * 3.3 / 65535
            total_voltage2 += voltage_reading2
            voltage_reading3 = adc_pin3.read_u16() * 3.3 / 65535
            total_voltage3 += voltage_reading3
            pwm_pin1.off()
            utime.sleep_us(100)
    average_voltage1 = total_voltage1 / j
    average_voltage2 = total_voltage2 / j
    average_voltage3 = total_voltage3 / j
    print("Average voltage sensor 1:", average_voltage1)
    print("Average voltage sensor 2:", average_voltage2)
    print("Average voltage sensor 3:", average_voltage3)
    utime.sleep(2)
