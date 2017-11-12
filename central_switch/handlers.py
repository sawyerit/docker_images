"""
This module contains all the web handlers
"""
import json
import time

from datetime import timedelta
from twisted.web import server
from twisted.web.resource import Resource

class ClickHandler(Resource):
    isLeaf = True

    def __init__(self, controller):
        Resource.__init__(self)
        self.controller = controller

    def render(self, request):
        cur_door = self.controller.get_door_byid(request.args['id'][0])
        if cur_door:
            self.controller.toggle(cur_door.id)
            return 'OK'
        else:
            return 'NOT FOUND' # todo: return something valid here

class StatusHandler(Resource):
    isLeaf = True

    def __init__(self, controller):
        Resource.__init__(self)
        self.controller = controller

    def render(self, request):
        door = request.args['id'][0]
        for d in self.controller.doors:
            if d.id == door:
                return d.last_state
        return ''

class InfoHandler(Resource):
    isLeaf = True

    def __init__(self, controller): # TODO: is this even needed
        Resource.__init__(self)
        self.controller = controller

    def render(self, request):
        version = self.controller.version
        connect_from = request.getClientIP()
        return str(version + " - connect from: " + connect_from)

class ConfigHandler(Resource):
    isLeaf = True
    def __init__(self, controller): # TODO: does this even work
        Resource.__init__(self)
        self.controller = controller

    def render(self, request):
        request.setHeader('Content-Type', 'application/json')
        return json.dumps([(d.id, d.name, d.last_state, d.last_state_time, d.is_auto_door)
                           for d in self.controller.doors])

class UptimeHandler(Resource):
    isLeaf = True
    def __init__(self, controller):
        Resource.__init__(self)

    def render(self, request):
        request.setHeader('Content-Type', 'application/json')

        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            uptime_string = str(timedelta(seconds=uptime_seconds))
        return json.dumps("Uptime: " + uptime_string)

class UpdateHandler(Resource):
    isLeaf = True
    def __init__(self, controller):
        Resource.__init__(self)
        self.delayed_requests = []
        self.controller = controller

    def handle_updates(self):
        for request in self.delayed_requests:
            updates = self.controller.get_updates(request.lastupdate)
            if updates != []:
                self.send_updates(request, updates)
                self.delayed_requests.remove(request)

    def format_updates(self, request, update):
        response = json.dumps({'timestamp': int(time.time()), 'update':update})
        if hasattr(request, 'jsonpcallback'):
            return request.jsonpcallback +'('+response+')'
        else:
            return response

    def send_updates(self, request, updates):
        request.write(self.format_updates(request, updates))
        request.finish()

    def render(self, request):

        # set the request content type
        request.setHeader('Content-Type', 'application/json')

        # set args
        args = request.args

        # set jsonp callback handler name if it exists
        if 'callback' in args:
            request.jsonpcallback =  args['callback'][0]

        # set lastupdate if it exists
        if 'lastupdate' in args:
            request.lastupdate = float(args['lastupdate'][0])
        else:
            request.lastupdate = 0
            #print "request received " + str(request.lastupdate)

        # Can we accommodate this request now?
        updates = self.controller.get_updates(request.lastupdate)
        if updates != []:
            print('doing the update')
            return self.format_updates(request, updates)

        print('delaying request')
        request.notifyFinish().addErrback(lambda x: self.delayed_requests.remove(request))
        self.delayed_requests.append(request)

        # tell the client we're not done yet
        return server.NOT_DONE_YET