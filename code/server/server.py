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
import time

define("port", default=3000, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/", MainHandler)]
        settings = dict(debug=True)
        tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.websocket.WebSocketHandler):
    dispatcher = Dispatcher.Dispatcher()
    timer = threading.Timer(1.0,dispatcher.run())
    def get_reply(r_json):
        if "poweron" in r_json:
            timer.start()
            dispatcher.PowerOn()
            return '''ok or fail'''
        elif "poweroff" in r_json:
            pass
            dispatcher.delete_sevice(r_json['poweroff']['room_id'])
            timer.cancel()
            return '''ok or fail'''
        elif "config" in r_json:
            return '''ok or fail'''
        elif "temp_update" in r_json:

            return '''finish or null'''
        else:
            return "format error"

    def check_origin(self, origin):
        return True

    def open(self):
        logging.info("A client connected.")
        self.write_message('server connected.')

    def on_close(self):
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
