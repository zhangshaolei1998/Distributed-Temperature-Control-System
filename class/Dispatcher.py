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

    # 创建一个服务并添加队列信息
    def create_service(self, room_id):
        service = Service(room_id)
        # service_id暂时先设置为room_id，以后再更改
        service_id = room_id
        self.lists.append([room_id, service_id])

        # 执行策略 ......

        self.sq.append_service(service_id, service)
        return self.sq.service_queue

    # 删除某一服务并删除队列信息
    def delete_service(self, room_id):
        i = 0
        for room_service in self.lists:
            if room_service[0] == room_id:
                service_id = room_service[1]
                service_id, service = self.sq.move_service(service_id)
                del service
                break
            i += 1
        del self.lists[i]

    '''
    room_id房间申请服务，
    分配一个service_id根据调度策略将service_id放到等待队列或者服务队列
    
    def add_service(self,room_id):


        return service_id
    '''

if __name__ == "__main__":
    dis=Dispatcher()
    #测试create_service
    a=dis.create_service(1)
    print(a)
