"""Software to monitor and control your home via a raspberry pi."""

import time
import smtplib
import syslog

import json
import httplib
import urllib

# undo
#import pigpio

from door import Door
from zone import Zone
from handlers import ClickHandler, ConfigHandlerDoor, ConfigHandlerZone, InfoHandler
from handlers import StatusHandler, UpdateHandlerDoor, UpdateHandlerZone, UptimeHandler
from logger import CSLogger

from twisted.internet import task
from twisted.internet import reactor
from twisted.web import server
from twisted.web.static import File
from twisted.web.resource import IResource
from twisted.cred import checkers, portal
from twisted.web.guard import HTTPAuthSessionWrapper, BasicCredentialFactory
from zope.interface import implements

class HttpPasswordRealm(object):
    implements(portal.IRealm)

    def __init__(self, myresource):
        self.myresource = myresource

    def requestAvatar(self, user, mind, *interfaces):
        if IResource in interfaces:
            return (IResource, self.myresource, lambda: None)
        raise NotImplementedError()

class Controller(object):
    """ The controller object sets up the webserver, handles events from the UI,
    handles event notification, logging etc. It is the main execution of the
    application.
    """
    def __init__(self, config):
        # Setup loggers for writing to google drive
        self.version = config['config']['version']
        self.use_gdrive = config['config']['use_gdrive']
        self.server_logger = CSLogger(self.use_gdrive, "Logging", "CentralSwitch")
        self.garage_logger = CSLogger(self.use_gdrive, "Logging", "GarageDoors")

        # write initialization to the spreadsheet
        self.server_logger.log(["CentralStation", "server controller started"])
        # setup the configuration
        self.config = config
        self.updateHandlerDoor = UpdateHandlerDoor(self)
        self.updateHandlerZone = UpdateHandlerZone(self)

        self.doors = [Door(n, c, self.garage_logger) for (n, c) in config['doors'].items()]
        for door in self.doors:
            door.last_state = 'unknown'
            door.last_state_time = time.time()

        self.zones = [Zone(n, c, self.garage_logger) for (n, c) in config['irrigation']['zones'].items()]
        print(len(self.zones))
        for zone in self.zones:
            zone.last_run_time = time.time()
            zone.last_state = 'unknown'

        self.use_alerts = config['config']['use_alerts']
        self.alert_type = config['alerts']['alert_type']
        self.ttw = config['alerts']['time_to_wait']
        if self.alert_type == 'smtp':
            self.use_smtp = False
            smtp_params = ("smtphost", "smtpport", "smtp_tls", "username", "password", "to_email")
            self.use_smtp = ('smtp' in config['alerts']) and set(smtp_params) <= set(config['alerts']['smtp'])
            syslog.syslog("we are using SMTP")
        elif self.alert_type == 'pushbullet':
            self.pushbullet_access_token = config['alerts']['pushbullet']['access_token']
            syslog.syslog("we are using Pushbullet")
        else:
            self.alert_type = None
            syslog.syslog("No alerts configured")


    def status_check(self):
        for door in self.doors:
            new_state = door.get_state()
            if door.last_state != new_state:
                door.logger.log([door.id, door.name, door.last_state + '=>' + new_state])
                door.last_state = new_state
                door.last_state_time = time.time()
                self.updateHandlerDoor.handle_updates()

            if new_state == 'open' and not door.msg_sent and time.time() - door.open_time >= self.ttw:
                if self.use_alerts:
                    title = "%s's garage door open" % door.name
                    etime = elapsed_time(int(time.time() - door.open_time))
                    message = "%s's garage door has been open for %s" % (door.name, etime)
                    if self.alert_type == 'smtp':
                        self.send_email(title, message)
                    elif self.alert_type == 'pushbullet':
                        self.send_pushbullet(door, title, message)
                    door.msg_sent = True

            if new_state == 'closed':
                if self.use_alerts:
                    if door.msg_sent:
                        title = "%s's garage doors closed" % door.name
                        etime = elapsed_time(int(time.time() - door.open_time))
                        message = "%s's garage door is now closed after %s "% (door.name, etime)
                        if self.alert_type == 'smtp':
                            self.send_email(title, message)
                        elif self.alert_type == 'pushbullet':
                            self.send_pushbullet(door, title, message)
                door.open_time = time.time()
                door.msg_sent = False

        for zone in self.zones:
            new_state = zone.get_state()
            if zone.last_state != new_state:
                zone.last_state = new_state
                zone.last_run_time = time.time()
                self.updateHandlerZone.handle_updates()

    def send_email(self, title, message):
        if self.use_smtp:
            syslog.syslog("Sending email message")
            config = self.config['alerts']['smtp']
            server = smtplib.SMTP(config["smtphost"], config["smtpport"])
            if config["smtp_tls"] == "True":
                server.starttls()
            server.login(config["username"], config["password"])
            server.sendmail(config["username"], config["to_email"], message)
            server.close()

    def send_pushbullet(self, door, title, message):
        syslog.syslog("Sending pushbutton message")
        config = self.config['alerts']['pushbullet']

        if door.pb_iden != None:
            conn = httplib.HTTPSConnection("api.pushbullet.com:443")
            conn.request("DELETE", '/v2/pushes/' + door.pb_iden, "",
                         {'Authorization': 'Bearer ' + config['access_token'], 'Content-Type': 'application/json'})
            conn.getresponse()
            door.pb_iden = None

        conn = httplib.HTTPSConnection("api.pushbullet.com:443")
        conn.request("POST", "/v2/pushes",
             json.dumps({
                 "type": "note",
                 "title": title,
                 "body": message,
             }), {'Authorization': 'Bearer ' + config['access_token'], 'Content-Type': 'application/json'})
        response = conn.getresponse().read()
        print(response)
        door.pb_iden = json.loads(response)['iden']

    def toggle(self, doorId):
        """ Click Handler invokes this controller action to toggle the selected door """
        door = self.get_door_byid(doorId)
        if door and door.is_auto_door:
            door.toggle_relay()
            return

    def toggle_zone(self, zId):
        """ Click Handler invokes this controller action to toggle the selected zone """        
        zone = next((x for x in self.zones if x.id == zId), None)
        if zone:
            zone.toggle_relay()
            return            

    def get_updates(self, lastupdate):
        updates = []
        for d in self.doors:
            # only fire an update ('upd') if there was a status update since the last check
            if d.last_state_time >= lastupdate:
                updates.append((d.id, d.last_state, d.last_state_time))
        return updates

    def get_zone_updates(self, lastupdate):
        updates = []
        for z in self.zones:
            # only fire an update ('upd') if there was a status update since the last check
            if z.last_run_time >= lastupdate:
                updates.append((z.id, z.last_state, z.last_run_time))
        return updates

    def get_door_byid(self, doorid):
        return next((x for x in self.doors if x.id == doorid), None)

    def run(self):
        info_handler = InfoHandler(self)
        task.LoopingCall(self.status_check).start(0.5)
        root = File('www')
        root.putChild('st', StatusHandler(self))
        root.putChild('upd-door', self.updateHandlerDoor)
        root.putChild('upd-zone', self.updateHandlerZone)
        root.putChild('cfg-door', ConfigHandlerDoor(self))
        root.putChild('cfg-zone', ConfigHandlerZone(self))
        root.putChild('upt', UptimeHandler(self))
        root.putChild('inf', info_handler)

        if self.config['config']['use_auth'] and info_handler.is_remote_ip:
            clk = ClickHandler(self)
            args = {self.config['site']['username']:self.config['site']['password']}
            checker = checkers.InMemoryUsernamePasswordDatabaseDontUse(**args)
            realm = HttpPasswordRealm(clk)
            p = portal.Portal(realm, [checker])
            credentialFactory = BasicCredentialFactory("Garage Door Controller")
            protected_resource = HTTPAuthSessionWrapper(p, [credentialFactory])
            root.putChild('clk', protected_resource)
        else:
            root.putChild('clk', ClickHandler(self))

        site = server.Site(root)
        reactor.listenTCP(self.config['site']['port'], site)  # @UndefinedVariable
        reactor.run()  # @UndefinedVariable

def elapsed_time(seconds, suffixes=['y', 'w', 'd', 'h', 'm', 's'], add_s=False, separator=' '):
    """
    Takes an amount of seconds and turns it into a human-readable amount of time.
    """
    # the formatted time string to be returned
    time_str = []

    # the pieces of time to iterate over (days, hours, minutes, etc)
    # - the first piece in each tuple is the suffix (d, h, w)
    # - the second piece is the length in seconds (a day is 60s * 60m * 24h)
    parts = [(suffixes[0], 60 * 60 * 24 * 7 * 52),
             (suffixes[1], 60 * 60 * 24 * 7),
             (suffixes[2], 60 * 60 * 24),
             (suffixes[3], 60 * 60),
             (suffixes[4], 60),
             (suffixes[5], 1)]

    # for each time piece, grab the value and remaining seconds, and add it to
    # the time string
    for suffix, length in parts:
        value = seconds / length
        if value > 0:
            seconds = seconds % length
            time_str.append('%s%s' % (str(value),
                                      (suffix, (suffix, suffix + 's')[value > 1])[add_s]))
        if seconds < 1:
            break

    return separator.join(time_str)

if __name__ == '__main__':
    # configure and run the site
    CONFIG_FILE = open('config.json')
    CONTROLLER = Controller(json.load(CONFIG_FILE))
    CONFIG_FILE.close()

    CONTROLLER.run()
