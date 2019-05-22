class Dispatcher:

    '''
    初始化
    service_num:服务对象数量上限
    '''

    request_num = 0

    def __init__(self,service_num):
        self.service_num=service_num

    '''
    room_id房间申请服务，
    分配一个service_id根据调度策略将service_id放到等待队列或者服务队列
    '''
    def add_service(self,room_id):


        return service_id
