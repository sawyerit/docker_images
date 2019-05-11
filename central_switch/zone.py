""" This module contains the irrigation zpne object and its methods """
import time

# import pigpio

class Zone(object):
    """ The Zone object created from the config.json file. A new instance of zone is
    created for each zone in the config.
    """
    last_action = None
    last_action_time = None
    msg_sent = False
    pb_iden = None

    def __init__(self, zoneId, config, glogger):
        self.logger = glogger
        self.id = zoneId
        self.zone_ip = config['pi_ip'] # remote pi that controls this zone relay
        self.name = config['name']
        self.relay_pin = config.get('relay_pin')        
        self.default_open_time = config.get('default_open_time')
        self.remote_connect_count = 0

        # setup irrigation remote pi
        self.connect_remote_pi()

        #  undo
        # if self.relay_pin:
        #     self.remote_pi.set_mode(self.relay_pin, pigpio.OUTPUT)
        #     self.remote_pi.write(self.relay_pin, 1)

    def toggle_relay(self):
        """ Toggle the relay. Set relay_pin low to trigger the
        zone via the relay.
        """
        state = self.get_state()
        if state == 'on':
            self.last_action = 'off'
            self.last_action_time = time.time()
        elif state == 'off':
            self.last_action = 'on'
            self.last_action_time = time.time()
        else:
            self.last_action = None
            self.last_action_time = None

        #
        print("turning zone on")
        time.sleep(5)
        print("turning zone off")
        # undo
        # self.remote_pi.write(self.relay_pin, 0)
        # time.sleep(self.default_open_time) # todo: make open time more dynamic, editable via the web app
        # self.remote_pi.write(self.relay_pin, 1)

    def get_state(self):
        """ Gets the current state of the door based on the state_pin
        and returns the state/status.
        """
        # undo and test this??
        # if self.remote_pi.read(self.relay_pin) == 1:
        # will always be off on the UI untl this is put back??
        if 0 == 0:
            return 'off'
        elif self.last_action == 'on':
            if time.time() - self.last_action_time >= self.default_open_time:
                return 'off'
        elif self.last_action == 'off':
            if time.time() - self.last_action_time >= self.default_open_time:
                return 'on' # This state indicates a problem
            else:
                return 'on'
        else:
            return 'on'

    def connect_remote_pi(self):
        """ Recursively try to connect to remote pi
        e.g. incase its not back up after a power failure
        """
        # undo
        # self.remote_pi = pigpio.pi(self.zone_ip)
        # if self.remote_pi.connected:
        #     self.logger.log(["Controller", "connected to pi for zone " + self.name])
        # else:
        #     if self.remote_connect_count < 8:
        #         self.remote_connect_count += 1
        #         time.sleep(2*self.remote_connect_count)
        #         self.connect_remote_pi()
        #     else:
        #         self.logger.log(["Controller", "could not connect to pi for zone " + self.name])
