#!/bin/python3
import sys
import datetime
import tornado.escape
import tornado.ioloop
import tornado.web
import re
from config import *

___VERSION___ = "0.2"


def build_to_int(build):
    return int(datetime.datetime.strptime(build, "%d.%m.%Y").strftime("%Y%m%d"))


def make_download_url(request, firmware):
    return '/'.join(["http://" + request.host, "firmware", str(firmware["version"]), "upd_app.bin"])


def make_download_url_old_frs(request, firmware):
    return '/'.join(["http://" + request.host, "firmware", str(firmware["version"]), "upd_app_for_old_frs.bin"])


class VersionHandler(tornado.web.RequestHandler):
    def get(self):
        response = {'susv': ___VERSION___,
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


def cached_feature_licenses():
    if not cached_feature_licenses.map:
        tmp_map = {}
        with open(FEATURE_LICENSES_PATH) as f:
            license_line_re = re.compile("^(\d{16})\t([A-F0-9a-f]{128})\t([A-F0-9a-f]{128})$")
            for line in f:
                matched = license_line_re.match(line)
                if not matched:
                    raise ValueError("invalid feature license string {}" % line)
                tmp_map[matched.group(1)] = (matched.group(2), matched.group(3))
            if tmp_map:
                cached_feature_licenses.map = tmp_map
            else:
                raise ValueError("No licenses in file {}" % FEATURE_LICENSES_PATH)
    return cached_feature_licenses.map


cached_feature_licenses.map = None


def licenses_for_serial(serial):
    return cached_feature_licenses()[serial]


class DeployFeatureLicenses(tornado.web.RequestHandler):
    def post(self):
        if self.request.body:
            try:
                data = tornado.escape.json_decode(self.request.body)
                kkt_serial = str(data['serial'])
                license_signature = licenses_for_serial(kkt_serial)
                response = {'licenses': license_signature[0],
                            'signature': license_signature[1]
                            }
                self.write(response)
                return
            except KeyError:
                self.send_error(400, message='Unable to parse JSON.')  # Bad Request
            except FileNotFoundError:
                self.send_error(400, message='Invalid license file.')
        else:
            self.send_error(400, message='Empty request body.')  # Bad Request


application = tornado.web.Application([
    (r"/check_firmware", CheckStableFirmware),
    (r"/feature_licenses", DeployFeatureLicenses),
    (r"/version", VersionHandler),
    (r'/firmware/(.*)', tornado.web.StaticFileHandler, {'path': FIRMWARE_PATH})
])


def main():
    application.listen(PORT)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
