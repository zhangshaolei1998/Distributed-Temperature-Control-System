import Service

class ServiceQueue:
    '''
        初始化，新建service_queue,用来保存service_id和service
        service_queue为记录了service_id和service的list
        '''

    def __init__(self):
        self.service_queue = []

    '''
    添加一个service_id和service到service_queue，返回是否成功
    '''

    def append_service(self, service_id, service):
        self.service_queue.append([service_id, service])

        return

    '''
    从service_queue中移除service_id和对应的service,返回service_id和对应的service
    '''

    def move_service(self, service_id):
        return service_id, service

    '''
    返回服务队列中的数量
    '''
    def get_service_num(self):

        return service_num

    '''
    根据调度策略选出即将被移到等待队列的服务
    返回service_id和service
    '''
    def get_wait_service(self):


        return service_id,service

    '''
    返回服务队列
    '''
    def get_service_queue(self):

        return self.service_queue
