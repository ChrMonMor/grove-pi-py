# libries installed
####
# this the OOP version of the python code in Grove+
# it needs $ python -m pip install requests : $ python -m pip install json : $ python -m pip install time
# timer list represent:  [0] = temp, [1] = humid, [2] = noise, [3] = Air
# sensorPorts list represent: [0] = temp & humid, [1] = noise, [2] = Air
####

import requests
import json
import time 
import math
import grovepiimport socket
 
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# connect() for UDP doesn't send packets
s.connect(('10.0.0.0', 0))  
ip = s.getsockname()[0])

class index:
    def __init__(self, sensorPorts) -> None:
        self.sensorPorts = sensorPorts
        temp = self.get_varibles()
        self.current_time = time.time()
        self.timer = [60 * temp[0]['temperature'] + self.current_time, 60 * temp[0]['humidity'] + self.current_time, 60 * temp[0]['noise'] + self.current_time, 60 * temp[0]['airquality'] + self.current_time]

    # fetches varibles from database, it tries 5 times incase the first failed.
    def get_varibles():
        url = 'http://192.168.1.149/post_api.php'
        tries = int(0)
        try:
            response = requests.get(url)
            while tries < 5:
                if response.status_code == 200:
                    posts = response.json()
                    return posts
                else:
                    tries += 1
        except requests.exceptions.RequestException as e:
            print('Error:', e)
            return None
    
    # gets varibles and sets the time for that one pin 
    def update_pin_timer(self, i) -> None:
        temp = self.get_varibles()
        if i == 0:
            self.timer[i] = 60 * temp[0]['temperature'] + self.current_time
        if i == 1:
            self.timer[i] = 60 * temp[0]['humidity'] + self.current_time
        if i == 2:
            self.timer[i] = 60 * temp[0]['noise'] + self.current_time
        if i == 3:
            self.timer[i] = 60 * temp[0]['airquality'] + self.current_time
    
    # send data off the chosen pin to the cloud database plus the promised time for the next one
    def send_data(self, i, readings) -> None:
        self.update_pin_timer(i)
        api_url = "http://192.168.1.147/sensordate.php"
        headers =  {"Content-Type":"application/json"}
        params = {"readings": readings, "promise": self.timer[i], "ip": ip}
        tries = int(0)
        while tries < 5:
            response = requests.post(api_url, data=json.dumps(params), headers=headers)
            if response.status_code == 200:
                return
            else:
                tries += 1
    



    def analogReadSensor(self, pin) -> float:
        return grovepi.analogRead(self.sensorPorts[pin])

    # t == 1 == temp == true
    # t == 0 == humid == false
    def dhtRead(self, t) -> float[]:
        [temp, humid] = grovepi.dht(self.sensorPorts[0])
        if t == 1:
            return temp
        else: 
            return humid

    
arr = [1,2,3]
main = index(arr)

while True:
    main.current_time = time.time()
    if main.current_time > main.timer[0]:
        main.send_data(0, main.dhtRead(1))
    if main.current_time > main.timer[1]:
        main.send_data(1, main.dhtRead(0))
    if main.current_time > main.timer[2]:
        main.send_data(2, main.analogReadSensor(1))
    if main.current_time > main.timer[3]:
        main.send_data(3, main.analogReadSensor(2))
