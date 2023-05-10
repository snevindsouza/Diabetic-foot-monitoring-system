import machine
import utime
import socket
import time
import network
import urequests

# WiFi credentials
ssid = 'S'
password = '12345678'

# Connect to WiFi network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Wait for WiFi connection
max_wait = 10
while max_wait > 0:
    if wlan.status() == network.STAT_GOT_IP:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

if wlan.status() != network.STAT_GOT_IP:
    raise RuntimeError('network connection failed')
else:
    print('Connected')
    status = wlan.ifconfig()
    print('ip =', status[0])
    
# configure PWM pin for sensor readings
pwm_pin = machine.Pin(0, machine.Pin.OUT)

# configure ADC pin for multiplexer output
adc_pin = machine.ADC(26)

# configure analog multiplexer pins
mux_s0 = machine.Pin(1, machine.Pin.OUT)
mux_s1 = machine.Pin(2, machine.Pin.OUT)
mux_s2 = machine.Pin(3, machine.Pin.OUT)
mux_s3 = machine.Pin(4, machine.Pin.OUT)
mux_en = machine.Pin(5, machine.Pin.OUT)

# set up variables for averaging
sample_count = 128
total_voltage = [0] * 16

# create a 4x4 matrix to store the average voltage values
average_voltage_matrix = [[0 for x in range(4)] for y in range(4)]


# Color coding for heatmap
color_codes = {
    "red": (255, 0, 0),
    "orange": (255, 165, 0),
    "yellow": (255, 255, 0),
    "green": (0, 255, 0)
}
# Set up socket to listen for incoming HTTP requests
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('listening on', addr)
# main loop    
while True:
    # Generate HTML for heatmap table
    def generate_heatmap(average_voltage_matrix):
        html = "<table>\n"
        for row in average_voltage_matrix:
            html += "<tr>\n"
            for val in row:
                color = get_color(val)
                html += f'<td style="background-color:rgb({color[0]},{color[1]},{color[2]})">{val}</td>\n'
            html += "</tr>\n"
        html += "</table>\n"
        return html
    
    # Determine the color for a given sensor value
    def get_color(val):
        if val < 0.9:
            return color_codes["red"]
        elif val < 1.8:
            return color_codes["orange"]
        elif val < 2.5:
            return color_codes["yellow"]
        else:
            return color_codes["green"]        

    for row in range(4):
        for col in range(4):
            # calculate the index of the current sensor
            channel = row * 4 + col
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
                    j += 1
                    pwm_pin.on()
                    utime.sleep_us(100)
                    voltage_reading = adc_pin.read_u16() * 3.3 / 65535
                    total_voltage[channel] += voltage_reading
                    pwm_pin.off()
                    utime.sleep_us(100)
            # calculate the average voltage for the current sensor
            average_voltage = total_voltage[channel] / j
            # store the average voltage in the matrix
            average_voltage_matrix[row][col] = average_voltage
            # disable the multiplexer output
            mux_en.off()
            
    # Process incoming HTTP requests

    print("average_voltage_matrix:")
    for row in average_voltage_matrix:
        print(row)  
    utime.sleep(2)
    #response = urequests.get('http://localhost:80/')
    


