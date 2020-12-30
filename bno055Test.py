import time
import board
import busio
import adafruit_bno055
import json

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)

START_CALIBRATION_DATA = 0x55
MODE_CONFIG = 0x00
MODE_NDOF = 0x0C

def get_calibration():
    sensor.mode = MODE_CONFIG
    
    data = []
    for i in range(22):
        data.append(sensor._read_register(START_CALIBRATION_DATA+i))
        
    print(type(data))
    print(data)
    with open("bno055cal2.json", "w") as cal_file:
        json.dump(data, cal_file)
    
    sensor.mode = MODE_NDOF
    
    return data

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
    
set_calibration()
while True:
    for i in range(200):
        try:
            print("Euler angle: {}".format(sensor.euler))
            print("Temperature: {}".format(sensor.temperature))
            print("Gravity: {}".format(sensor.gravity))
            print("Calibration: {}".format(sensor.calibration_status))
        except Exception as e:
            print (e)
        #cal_data = sensor.get_calibration()
        #with open("bnocal.json", w) as cal_file:
        #    json.dump(cal_data, cal_file)
        time.sleep(0.1)
    
    get_calibration()
    time.sleep(5)
    