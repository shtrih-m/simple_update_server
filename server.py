#!/bin/python3
import sys
import datetime
import tornado.escape
import tornado.ioloop
import tornado.web
from config import *

___VERSION___ = "0.1"


def build_to_int(build):
    return int(datetime.datetime.strptime(build, "%d.%m.%Y").strftime("%Y%m%d"))


def make_download_url(request, firmware):
    return '/'.join(["http://"+request.host, "firmware", str(firmware["version"]), "upd_app.bin"])


def make_download_url_old_frs(request, firmware):
    return '/'.join(["http://"+request.host, "firmware", str(firmware["version"]), "upd_app_for_old_frs.bin"])


class VersionHandler(tornado.web.RequestHandler):
    def get(self):
        response = {'susv': '0.1',
                    'python': sys.version.split(" ")[0],
                    'tornado': tornado.version,
                    'server': '1.0'}
        self.write(response)


class CheckStableFirmware(tornado.web.RequestHandler):
    def post(self):
        if self.request.body:
            try:
                data = tornado.escape.json_decode(self.request.body)
                build = build_to_int(data['build_date'])
                response = {'update_available': build < CURRENT_FIRMWARE["version"],
                            'critical': build < CRITICAL_VERSION,
                            'version': CURRENT_FIRMWARE["version"],
                            'description': CURRENT_FIRMWARE["description"],
                            "url": make_download_url(self.request, CURRENT_FIRMWARE),
                            "url_old_frs": make_download_url_old_frs(self.request, CURRENT_FIRMWARE)}
                self.write(response)
                return
            except ValueError:
                self.send_error(400, message='Unable to parse JSON.')  # Bad Request
        else:
            self.send_error(400, message='Empty request body.')  # Bad Request


application = tornado.web.Application([
    (r"/check_firmware", CheckStableFirmware),
    (r"/version", VersionHandler),
    (r'/firmware/(.*)', tornado.web.StaticFileHandler, {'path': FIRMWARE_PATH})
])


def main():
    application.listen(PORT)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
