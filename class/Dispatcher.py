from Service import Service
from ServiceQueue import ServiceQueue
from WaitQueue import WaitQueue
from Config import Config
import time

class Dispatcher:

    '''
    初始化
    service_num:服务对象数量上限
    '''

    request_num = 0
    def __init__(self):
        # room_id 和 service_id 的映射
        self.lists = []
        self.sq = ServiceQueue()
        self.wq = WaitQueue()
        self.max_service_id=0 #当前最大的service_id
        self.max_service=3 #允许同时服务最大数量
        self.wait_time=120000 #默认等待服务时长 120000ms
        self.max_wait_time = 999999999999  # 最大等待服务时长，若等待时长为此值，等待时长不减少，服务队列空的时候才加入服务队列
        self.unit=60000 #时间片长度60000ms，每次运行一次run
        self.per_var=[0,1,2,3] #单位时间，各档风速对应的温度改变

    # 创建一个服务并添加队列信息
    def create_service(self, room_id,indoor_temp):
        service = Service(indoor_temp)
        # service_id记录每一次服务
        service_id = self.max_service_id+1
        self.max_service_id += 1
        self.lists.append([room_id, service_id])

        # 执行策略 ......
        if(self.sq.get_service_num()<self.max_service):
            self.sq.append_service(service_id, service)
        else:
            lowest_id,lowest_speed=self.sq.get_lowest_speed_service()
            #print(lowest_id)
            if service.fan_speed>lowest_speed :
                if(len(lowest_id)==1):
                    move_id,move_service=self.sq.move_service(lowest_id[0])
                    #分配等待服务时间
                    move_service.set_wait_time(self.wait_time)

                    #移入等待队列
                    self.wq.append_service(move_id,move_service)
                    #移入服务队列
                    self.sq.append_service(service_id, service)
                else:
                    #print(lowest_id)
                    longest_id=self.sq.get_longest_service_in_list(lowest_id)
                    #print(longest_id)
                    move_id, move_service = self.sq.move_service(longest_id[0])
                    # 分配等待服务时间
                    move_service.set_wait_time(self.wait_time)

                    # 移入等待队列
                    self.wq.append_service(move_id, move_service)
                    # 移入服务队列
                    self.sq.append_service(service_id, service)
            elif service.fan_speed==lowest_speed:
                # 分配等待服务时间
                service.set_wait_time(self.wait_time)
                # 移入等待队列
                self.wq.append_service(service_id, service)

            elif service.fan_speed<lowest_speed:
                # 分配等待服务时间
                service.set_wait_time(self.max_wait_time)
                # 移入等待队列
                self.wq.append_service(service_id, service)



        return self.sq.service_queue


    '''
    单位时间运行一次，遍历等待队列，服务队列
    返回结束的room_id的list
    '''

    def run(self):

        finish_id=[] #记录达到目标温度的room_id

        #遍历服务队列。若服务完成，则移出队列
        for service_map in self.sq.service_queue:
            service_map[1].add_service_time(self.unit)
            is_finished=service_map[1].change_indoor_temp(self.per_var[service_map[1].fan_speed])
            if is_finished:
                move_id, move_service = self.sq.move_service(service_map[0])
                finish_id.append(self.service_id2room_id(move_id))

        #遍历等待队列。若等待时间降为0，移入服务队列。
        for service_map in self.wq.wait_queue:
            service_map[1].reduce_wait_time(self.unit)

            if service_map[1].wait_time<=0:
                longest=self.sq.get_longest_service()

                #从服务队列移除服务时间最长的服务
                move_id, move_service = self.sq.move_service(longest[0])
                # 分配等待服务时间
                move_service.set_wait_time(self.wait_time)
                # 移入等待队列
                self.wq.append_service(move_id, move_service)

                # 从等待队列移除等待时间=0的服务
                service_id, service = self.wq.move_service(service_map[0])
                # 移入服务队列
                self.sq.append_service(service_id, service)


        #若服务队列空闲，移入等待时间最小的。
        while (self.sq.get_service_num()<self.max_service and self.wq.get_wait_num()>0):
            lowest_id=self.wq.get_lowest_wait_service()
            # 从等待队列移除等待时间最短的服务
            service_id, service = self.wq.move_service(lowest_id[0])
            # 移入服务队列
            self.sq.append_service(service_id, service)


        return finish_id #返回结束服务的room_id

    '''
    通过service_id 转成对应的room_id
    '''

    def service_id2room_id(self,service_id):
        room_id = -1
        # 根据room_id找到对应的service_id
        for room_service in self.lists:
            if room_service[1] == service_id:
                room_id = room_service[0]

        return room_id



    # 删除某一服务对象并删除队列信息
    def delete_service(self, room_id):
        service_id, service = self.find_service(room_id)
        # 删除服务对象
        if service is not None:
            del service

        i = 0
        exist = 0
        for room_service in self.lists:
            if room_service[0] == service_id:
                exist = 1
                break
            i += 1
        # 删除队列信息
        if exist:
            del self.lists[i]

        # 删除服务队列或等待队列信息
        service = self.sq.get_service(service_id)
        if service is not None:
            self.sq.move_service(service_id)
        else:
            service = self.wq.get_service(service_id)
            if service is not None:
                self.wq.move_service(service_id)

    # 根据room_id找到ServiceQueue或WaitQueue里边的Service对象
    def find_service(self, room_id):
        service_id = -1
        # 根据room_id找到对应的service_id
        for room_service in self.lists:
            if room_service[0] == room_id:
                service_id = room_service[1]
        # 查找ServiceQueue和WaitQueue
        service = self.sq.get_service(service_id)
        if service is None:
            service = self.wq.get_service(service_id)
            if service is None:
                return service_id, None
        return service_id, service

    # 调节温度
    def change_temperature(self, room_id, temp):
        service_id, service = self.find_service(room_id)
        service.set_temperature(temp)

    # 调节风速
    def change_fan_speed(self, room_id, speed):
        service_id, service = self.find_service(room_id)
        service.set_fan_speed(speed)


    # 初始化
    def PowerON(self):
        self.SettingMode = True
        return True


    # 设置config
    def SetPara(self, Mode, Temp_lowLimit, Temp_highLimit, default_TargetTemp, min_speed, max_speed, default_speed,
                FeeRate_H, FeeRate_M, FeeRate_L):
        if self.SettingMode:
            Config.set_para(Mode, Temp_lowLimit, Temp_highLimit, default_TargetTemp, min_speed, max_speed,
                            default_speed, FeeRate_H, FeeRate_M, FeeRate_L)
            return True
        else:
            return False


    # 返回各房间的状态信息：状态信息：（是否开机，是否正在服务，是否被挂起），当前室温，目标温度，风速，费率，费用，服务时长
    def GetRoomState(self, room_id):
        for room_service in self.lists:
            if room_service[0] == room_id:
                service_id = room_service[1]
                service = self.sq.get_service(service_id)
                return service.get_info()


    # 展示每个房间的开关次数，使用空调的时长，总费用，被调度的次数、详单数、调温次数、调风次数
    def QueryReport(self, list_room_id, report_type, date):
        report = get_report(list_room_id, report_type, date)
        return report


    # 打印报表
    def PrintReport(self, list_room_id, report_type, date):
        report = get_report(list_room_id, report_type, date)
        return report


    def print_queue(self):

        print("=========================================")

        print("service_queue")
        for i in range(0, len(self.sq.service_queue)):

            print("service_id: ",self.sq.service_queue[i][0],"||", end=" ")
            print("start_time: ",self.sq.service_queue[i][1].start_time,"|",
                  "current_time: ",self.sq.service_queue[i][1].current_time,"|",
                  "service_time: ",self.sq.service_queue[i][1].service_time,"|",
                  "wait_time: ",self.sq.service_queue[i][1].wait_time,"|",
                  "indoor_temp: ", self.sq.service_queue[i][1].indoor_temp,"|",
                  "temperature: ", self.sq.service_queue[i][1].temperature,"|",
                  "fan_speed: ", self.sq.service_queue[i][1].fan_speed)

        print("---------------------------------------")
        print("wait_queue")
        for i in range(0, len(self.wq.wait_queue)):
            print("service_id: ", self.wq.wait_queue[i][0],"||", end=" ")
            print("start_time: ", self.wq.wait_queue[i][1].start_time,"|",
                  "current_time: ", self.wq.wait_queue[i][1].current_time,"|",
                  "service_time: ", self.wq.wait_queue[i][1].service_time,"|",
                  "wait_time: ", self.wq.wait_queue[i][1].wait_time,"|",
                  "indoor_temp: ", self.wq.wait_queue[i][1].indoor_temp,"|",
                  "temperature: ", self.wq.wait_queue[i][1].temperature,"|",
                  "fan_speed: ", self.wq.wait_queue[i][1].fan_speed)



if __name__ == "__main__":
    dis=Dispatcher()
    #测试create_service
    a=dis.create_service(1,16)
    a = dis.create_service(1, 16)
    #time.sleep(10)
    a = dis.create_service(1, 16)
    a = dis.create_service(1, 16)

    dis.print_queue()

    for j in range(0,6):
        print("unit",j)
        a=dis.run()
        dis.print_queue()

