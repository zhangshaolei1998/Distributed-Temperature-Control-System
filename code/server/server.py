#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.options
import sqldb
import sys
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
    dispatcher = Dispatcher()
    def get_reply(receive_json):
        if "poweron" in receive_json:
            pass
            while(1):
                dispatcher.PowerOn()
                time.sleep(1)
            return '''ok or fail'''
        elif "poweroff" in receive_json:
            pass

            return '''ok or fail'''
        elif "config" in receive_json:
            pass
            return '''ok or fail'''
        elif "temp_update" in receive_json:
            pass
            return '''finish or null'''

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
