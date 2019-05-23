from Service import Service
from ServiceQueue import ServiceQueue
from WaitQueue import WaitQueue


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

    # 创建一个服务并添加队列信息
    def create_service(self, room_id,indoor_temp):
        service = Service(indoor_temp)
        # service_id暂时先设置为room_id，以后再更改
        service_id = self.max_service_id+1
        self.lists.append([room_id, service_id])

        # 执行策略 ......
        if(self.sq.get_service_num()<self.max_service):
            self.sq.append_service(service_id, service)
        else:
            lowest_id,lowest_speed=self.sq.get_lowest_speed_service()
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
                    longest_id=self.sq.get_longest_service_in_list(lowest_id)
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
    单位时间运行一次
    '''

    def run(self):


        return






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


if __name__ == "__main__":
    dis=Dispatcher()
    #测试create_service
    a=dis.create_service(1,26)
    a = dis.create_service(1, 26)
    a = dis.create_service(1, 26)
    a = dis.create_service(1, 26)
    print("service")
    for i in range (0,len(dis.sq.service_queue)):
        print(dis.sq.service_queue[i][0],end=" ")
        print(dis.sq.service_queue[i][1].start_time,dis.sq.service_queue[i][1].wait_time,)
    print("wait")
    for i in range(0, len(dis.wq.wait_queue)):
        print(dis.wq.wait_queue[i][0], end=" ")
        print(dis.wq.wait_queue[i][1].start_time, dis.wq.wait_queue[i][1].wait_time, )

