""" This module contains the door object and its methods """
import time

# import pigpio

class Door(object):
    """ The Door object created from the config.json file. A new instance of door is
    created for each door in the config.  Each door can have its own "remote pi"
    instance for handling its actions.
    """
    last_action = None
    last_action_time = None
    msg_sent = False
    pb_iden = None

    def __init__(self, doorId, config, glogger):
        self.logger = glogger
        self.id = doorId
        self.is_auto_door = config['auto_door'] == "True"
        self.door_ip = config['pi_ip'] # remote pi that controls this door sensor
        self.name = config['name']
        self.relay_pin = config.get('relay_pin')
        self.state_pin = config['state_pin']
        self.state_pin_closed_value = config.get('state_pin_closed_value', 0)
        self.time_to_close = config.get('time_to_close', 10)
        self.time_to_open = config.get('time_to_open', 10)
        self.openhab_name = config.get('openhab_name')
        self.open_time = time.time()
        self.remote_connect_count = 0

        # setup garage remote pi, one for each door
        self.connect_remote_pi()

        #  undo
        # if self.relay_pin:
        #     self.remote_pi.set_mode(self.relay_pin, pigpio.OUTPUT)
        #     self.remote_pi.write(self.relay_pin, 1)
        # self.remote_pi.set_mode(self.state_pin, pigpio.INPUT)
        # self.remote_pi.set_pull_up_down(self.state_pin, pigpio.PUD_UP)

    def get_state(self):
        """ Gets the current state of the door based on the state_pin
        and returns the state/status.
        """
        # undo
        # if self.remote_pi.read(self.state_pin) == self.state_pin_closed_value:
        if 0 == self.state_pin_closed_value:
            return 'closed'
        elif self.last_action == 'open':
            if time.time() - self.last_action_time >= self.time_to_open:
                return 'open'
            else:
                return 'opening'
        elif self.last_action == 'close':
            if time.time() - self.last_action_time >= self.time_to_close:
                return 'open' # This state indicates a problem
            else:
                return 'closing'
        else:
            return 'open'

    def toggle_relay(self):
        """ Toggle the relay. Set relay_pin low to trigger the
        garage door via the relay.
        """
        state = self.get_state()
        if state == 'open':
            self.last_action = 'close'
            self.last_action_time = time.time()
        elif state == 'closed':
            self.last_action = 'open'
            self.last_action_time = time.time()
        else:
            self.last_action = None
            self.last_action_time = None

        # undo
        # self.remote_pi.write(self.relay_pin, 0)
        # time.sleep(0.2)
        # self.remote_pi.write(self.relay_pin, 1)

    def connect_remote_pi(self):
        """ Recursively try to connect to remote pi
        e.g. incase its not back up after a power failure
        """
        # undo
        # self.remote_pi = pigpio.pi(self.door_ip)
        # if self.remote_pi.connected:
        #     self.logger.log(["Controller", "connected to pi for door " + self.name])
        # else:
        #     if self.remote_connect_count < 8:
        #         self.remote_connect_count += 1
        #         time.sleep(2*self.remote_connect_count)
        #         self.connect_remote_pi()
        #     else:
        #         self.logger.log(["Controller", "could not connect to pi for door " + self.name])
