#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.options
import sqldb
import sys
import threading
sys.path.append("../../class")


from tornado.options import define, options
import json
import Dispatcher
import Config
import time

define("port", default=3000, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/", MainHandler)]
        settings = dict(debug=True)
        tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.websocket.WebSocketHandler):
    dispatcher = Dispatcher.Dispatcher()
    #timer = threading.Timer(1.0,dispatcher.run())
    users=set()
    user2room_id={}
    def broadcast(self, state):
        for i in users:
            i.write_massage(state[user2room_id[i]])
    def get_reply(self,r_json):
        if "poweron" in r_json:
            user2room_id[self] = r_json["room_id"]
            r_json = r_json['poweron']
            dispatcher.create_service(r_json['room_id'],r_json['cur_temp'])
            para = {
                "setpara" : {
                    "mode" : Config.mode,
                    "target_temp" : Config.default_temp,
                    "highlimit_temp" : Config.max_temp,
                    "lowlimit_temp" : Config.min_temp,
                    "highfan_change_temp" : Config.FeeRate_H,
                    "lowfan_change_temp" : Config.FeeRate_L,
                    "medfan_change_temp": Config.FeeRate_M,
                    "fan" : Config.fan
                    }
                }
            return json.dumps(para)
        elif "poweroff" in r_json:
            r_json = r_json['poweroff']
            dispatcher.delete_sevice(r_json['room_id'])
            return '''ok or fail'''
        elif "config" in r_json:
            r_json = r_json['config']
            if r_json['mode']!=0:
                dispatcher.change_mode(r_json['room_id'],r_json['mode'])
            if r_json['target_temp']!=0:
                dispatcher.change_temperature(r_json['room_id'],r_json['target_temp'])
            if r_json['fan']!=0:
                dispatcher.change_fan(r_json['room_id'],r_json['fan'])
                dispatcher.show_state()
            return 'ok'
        elif "temp_update" in r_json:
            r_json = r_json['temp_update']
            dispatch.set_indoor_temp(r_json['room_id'],r_json['cur_temp'])
            dispatch.dispatch()
            state = dispatcher.show_state()
            return state
        elif "server_config" in r_json:
            r_json = r_json['server_config']
            dispatcher.SetPara(
                r_json['Temp_lowlimit'],
                r_json['Temp_highLimit'],
                r_json['min_speed'].
                r_json['max_speed'],
                r_json['FeeRate_H'],
                r_json['FeeRate_M'],
                r_json['FeeRate_L']
                )
            return 'ok'
        elif "CheckRoomState" in r_json:
                pass

    def check_origin(self, origin):
        return True

    def open(self):
        self.users.add(self)
        logging.info("A client connected.")
        self.write_message('server connected.')

    def on_close(self):
        self.users.remove(self)
        logging.info("A client disconnected")
        self.write_message('server disconnected.')

    def on_message(self, message):
        receive_json = json.loads(message)
        '''
        reply = {}
        reply['message'] = 'sucess:' + message
        reply['name'] = 'air condition'
        logging.info("message: {}".format(message))
        reply_json = json.dumps(reply)
        '''
        #reply_json = json.dumps(receive_json)
        reply_json = get_reply(receive_json)
        self.write_message(reply_json)


def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
