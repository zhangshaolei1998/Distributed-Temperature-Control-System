import time


class Service:

    # 初始化对象
    def __init__(self):
        self.start_time = time.localtime(time.time())
        self.current_time = time.localtime(time.time())
        self.end_time = time.localtime(time.time())
        self.temperature = 26
        self.fan_speed = 0

    # 设置温度
    def set_temperature(self, temp):
        if 16 <= temp <= 30:
            self.temperature = temp
            return True
        else:
            return False

    # 设置风速
    def set_fan_speed(self, speed):
        if 0 <= speed <= 5:
            self.fan_speed = speed
            return True
        else:
            return False

    # 返回开始时间、当前时间、温度、风速
    def get_info(self):
        self.current_time = time.localtime(time.time())
        info = [self.start_time, self.current_time, self.temperature, self.fan_speed]
        return info

    # 销毁对象，返回开始时间、结束时间
    def __del__(self):
        self.end_time = time.localtime(time.time())
        return [self.start_time, self.end_time]
