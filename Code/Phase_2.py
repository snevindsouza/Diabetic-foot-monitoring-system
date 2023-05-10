import machine
import utime

# configure PWM pin for sensor readings
pwm_pin = machine.Pin(2, machine.Pin.OUT)

# configure ADC pin for multiplexer output
adc_pin = machine.ADC(26)

# configure analog multiplexer pins
mux_s0 = machine.Pin(3, machine.Pin.OUT)
mux_s1 = machine.Pin(4, machine.Pin.OUT)
mux_s2 = machine.Pin(5, machine.Pin.OUT)
mux_s3 = machine.Pin(6, machine.Pin.OUT)
mux_en = machine.Pin(7, machine.Pin.OUT)

# set up variables for averaging
sample_count = 128
total_voltage = [0] * 16

# configure UART communication
uart = machine.UART(0, baudrate=9600, bits=8, parity=None, stop=1)

while True:
    print('\n')
    for channel in range(16):
        # set the analog multiplexer to the current channel
        for i in range(4):
            pin = [mux_s0, mux_s1, mux_s2, mux_s3][i]
            value = (channel >> i) & 1
            pin.value(value)
        # enable the multiplexer output
        mux_en.on()
        # take readings from the current sensor
        j = 0
        total_voltage[channel] = 0
        for i in range(sample_count):
            if i > 20 and i < 108:
                j+=1
                pwm_pin.on()
                utime.sleep_us(100)
                voltage_reading = adc_pin.read_u16() * 3.3 / 65535
                total_voltage[channel] += voltage_reading
                pwm_pin.off()
                utime.sleep_us(100)
        # calculate the average voltage for the current sensor
        average_voltage = total_voltage[channel] / j
        print("Average voltage sensor", channel, ":", average_voltage)
        
        # send data to Bluetooth terminal
        uart.write("Sensor {}: {:.2f}V\n".format(channel, average_voltage))
        # disable the multiplexer output
        mux_en.off()
    
    utime.sleep(2)
    uart.write("\n")