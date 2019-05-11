"""
This module contains all the web handlers
"""
import json
import time

from datetime import timedelta
from twisted.web import server
from twisted.web.resource import Resource

class ClickHandler(Resource):
    """ Handles click events from the web application.
    Currently a click event will toggle the garage door.
    """
    isLeaf = True

    def __init__(self, controller):
        Resource.__init__(self)
        self.controller = controller

    def render(self, request):

        if request.args['type'] == 'door':
            cur_door = self.controller.get_door_byid(request.args['id'][0])
            if cur_door:
                self.controller.toggle(cur_door.id)
                return 'OK'
            else:
                return 'NOT FOUND'
        else:
            self.controller.toggle_zone(request.args['id'][0])
        

class StatusHandler(Resource):
    """ 
    Provides the state of the doors to the web front end
    """
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
    """ Provides information on the connecting IP address and displays 
    the version to the web front end.
    """
    isLeaf = True

    def __init__(self, controller):
        Resource.__init__(self)
        self.controller = controller
        self.is_remote_ip = False

    def render(self, request):
        version = self.controller.version
        connect_from = str(request.getClientIP())
        self.is_remote_ip = not connect_from.startswith("192")
        return str(version + " - connect from: " + connect_from)

class ConfigHandlerDoor(Resource):
    """ Sets up the web front end based on the config.json file
    Returns json to build the door web objects.
    """
    isLeaf = True
    def __init__(self, controller):
        Resource.__init__(self)
        self.controller = controller

    def render(self, request):
        request.setHeader('Content-Type', 'application/json')
        return json.dumps([(d.id, d.name, d.last_state, d.last_state_time, d.is_auto_door)
                           for d in self.controller.doors])

class ConfigHandlerZone(Resource):
    """ Sets up the web front end based on the config.json file
    Returns json to build the zone web objects.
    """
    isLeaf = True
    def __init__(self, controller):
        Resource.__init__(self)
        self.controller = controller

    def render(self, request):
        request.setHeader('Content-Type', 'application/json')
        return json.dumps([(z.id, z.name, z.last_run_time, z.state)
                           for z in self.controller.zones])                           

class UptimeHandler(Resource):
    """ 
    Provides server uptime data to the web front end
    """
    isLeaf = True
    def __init__(self, controller):
        Resource.__init__(self)

    def render(self, request):
        request.setHeader('Content-Type', 'application/json')

        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            uptime_string = str(timedelta(seconds=uptime_seconds))
        return json.dumps("Uptime: " + uptime_string)

class UpdateHandlerDoor(Resource):
    """
    Handles updates to the state of the doors
    """
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
            request.jsonpcallback = args['callback'][0]

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

        print 'delaying request'
        request.notifyFinish().addErrback(lambda x: self.delayed_requests.remove(request))
        self.delayed_requests.append(request)

        # tell the client we're not done yet
        return server.NOT_DONE_YET

class UpdateHandlerZone(Resource):