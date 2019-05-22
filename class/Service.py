import time


class Service:

    def __init__(self):
        self.start_time = time.localtime(time.time())
        self.end_time = time.localtime(time.time())
        self.temperature = 26
        self.fan_speed = 0

    def set_temperature(self, temp):
        self.temperature = temp

    def set_fan_speed(self, speed):
        self.fan_speed = speed

    def get_info(self):
        info = [self.start_time, self.end_time, self.temperature, self.fan_speed]
        return info
