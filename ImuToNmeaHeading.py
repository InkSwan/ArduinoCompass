import time
import board
import busio
import adafruit_bno055
import json
import serial

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)
port = serial.Serial ("/dev/ttyS0", 4800)

START_CALIBRATION_DATA = 0x55
MODE_CONFIG = 0x00
MODE_NDOF = 0x0C

def set_calibration():
    cal_data = None
    with open("bno055cal.json", "r") as cal_file:
        cal_data = json.load(cal_file)
        
    if(cal_data is None or len(cal_data) != 22):
       raise ValueError("Not 22 bytes")
    
    sensor.mode = MODE_CONFIG
    
    for i in range(22):
        sensor._write_register(START_CALIBRATION_DATA+i, cal_data[i])       
        
    sensor.mode = MODE_NDOF
    
    return cal_data

def checksum_from(payload):
    checksum = 0
    for byte in payload.encode('ascii'):
        checksum ^= byte

    return "{:02x}".format(checksum).upper()
    
set_calibration()
while True:
    heading, _, _ = sensor.euler

    payload = f"HCHDM,{heading:.0f},M"
    checksum = checksum_from(payload)

    packet = f"${payload}*{checksum}\r\n"

    port.write(packet.encode('ascii'))
    
    time.sleep(0.25)