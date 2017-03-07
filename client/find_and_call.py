# Copyright 2017 Antillion Ltd
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#!/usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import requests
import socket
import sys
from time import sleep
from datetime import datetime, timedelta

from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf

found_services = []


def is_our_api(service_name):
    return 'simpleapi' in service_name


def on_service_state_change(zeroconf, service_type, name, state_change):
    print("Service %s of type %s state changed: %s" % (name, service_type, state_change))
    global api_service # yeuch, globals

    info = zeroconf.get_service_info(service_type, name)
    if not info:
        print('[{}] Found no info'.format(name))
        return

    if state_change is ServiceStateChange.Added and is_our_api(name):
        api_service = {
            'address': socket.inet_ntoa(info.address),
            'port': info.port,
            'path': ''
        }
        paths = [value for key,value in info.properties.items()
                       if key == 'path']
        if len(paths) > 0:
            if len(paths) > 1:
                print('WARN: service {} provides more than one path ' +
                      ' will use first only'.format(name))

            api_service['path'] = paths[0]

        print('Discovered a service: {}'.format(api_service))
        found_services.append(api_service)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('requests').setLevel(logging.INFO)
    if len(sys.argv) > 1:
        assert sys.argv[1:] == ['--debug']
        logging.getLogger('zeroconf').setLevel(logging.DEBUG)

    zeroconf = Zeroconf()
    print("\nWaiting 10s for services to become available (Ctrl+C to cancel search early)\n")
    browser = ServiceBrowser(zeroconf, "_http._tcp.local.", handlers=[on_service_state_change])
    start = datetime.now()
    try:
        while datetime.now() < start + timedelta(seconds=10) :
            sleep(0.1)

    except KeyboardInterrupt:
        pass
    finally:
        zeroconf.close()

    if len(found_services) is 0:
        print('Found no services')
        sys.exit(2)

    print('\nQuerying {} services found'.format(len(found_services)))
    for service in found_services:
        result = requests.get('http://{address}:{port}{path}/hello'.format(**service))
        print('Service @ {} responded with {}:{}'.format(service['address'],
                                                         result.status_code,
                                                         result.content))
