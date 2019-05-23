from Service import Service

class WaitQueue:

    '''
    初始化，新建wait_queue,用来保存service_id和service
    wait_queue为记录了service_id和service的list
    '''
    def __init__(self):
        self.wait_queue=[]

    '''
    添加一个service_id和service到wait_queue，返回是否成功
    '''
    def append_service(self,service_id,service,wait_time):

        self.wait_queue.append([service_id,service,wait_time])
        return True;

    '''
    从wait_queue中移除service_id和对应的service,返回service_id和对应的service
    '''
    def move_service(self,service_id):

        for i in range(0,len(self.wait_queue)):
            if self.wait_queue[i][0]==service_id:
                service=self.wait_queue[i][1]
                del self.wait_queue[i]

        return service_id,service

    '''
    根据调度策略选择下一个执行的service，返回service_id service
    '''
    def get_ready_service(self):


        return service_id,service

    '''
    返回等待队列
    '''
    def get_wait_queue(self):

        return self.wait_queue

