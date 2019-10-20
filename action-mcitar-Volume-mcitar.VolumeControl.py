#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
from hermes_python.hermes import Hermes
from hermes_python.ffi.utils import MqttOptions
from hermes_python.ontology import *
import io

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

class SnipsConfigParser(configparser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, configparser.Error) as e:
        return dict()

def subscribe_intent_callback(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    action_wrapper(hermes, intentMessage, conf)


def action_wrapper(hermes, intentMessage, conf):
    #!/usr/bin/env python3
    
    from hermes_python.hermes import Hermes, MqttOptions
    import datetime
    import random
    import toml
    import alsaaudio
    
    USERNAME_INTENTS = "mcitar"
    MQTT_BROKER_ADDRESS = "localhost:1883"
    MQTT_USERNAME = None
    MQTT_PASSWORD = None
    
    m = alsaaudio.Mixer('PCM_PLAYBACK')
    vol = m.getvolume()[0]
    
    m.setmute(0)
    m.setvolume(100)
    
    def user_intent(intentname):
        return USERNAME_INTENTS + ":" + intentname
    
    
    def subscribe_intent_callback(hermes, intent_message):
        intentname = intent_message.intent.intent_name
    
        if intentname == user_intent("lauter"):
            vol = min(100,m.getvolume()[0] + 10)
            m.setvolume(vol)
            result_sentence = "Lautstärke auf {} gesetzt".format(vol)
    
        elif intentname == user_intent("leiser"):
            vol = max(0,m.getvolume()[0] - 10)
            m.setvolume(vol)
            result_sentence = "Lautstärke auf {} gesetzt".format(vol)
    
        elif intentname == user_intent("Volume"):
            vol = intentMessage.slots.volume.first().value
            m.setvolume(vol)
            result_sentence = "Lautstärke auf {} gesetzt".format(vol)
    
        current_session_id = intentMessage.session_id
        hermes.publish_end_session(current_session_id, result_sentence)
    
    if __name__ == "__main__":
        snips_config = toml.load('/etc/snips.toml')
        if 'mqtt' in snips_config['snips-common'].keys():
            MQTT_BROKER_ADDRESS = snips_config['snips-common']['mqtt']
        if 'mqtt_username' in snips_config['snips-common'].keys():
            MQTT_USERNAME = snips_config['snips-common']['mqtt_username']
        if 'mqtt_password' in snips_config['snips-common'].keys():
            MQTT_PASSWORD = snips_config['snips-common']['mqtt_password']
    
        mqtt_opts = MqttOptions(username=MQTT_USERNAME, password=MQTT_PASSWORD, broker_address=MQTT_BROKER_ADDRESS)
        with Hermes(mqtt_options=mqtt_opts) as h:
            h.subscribe_intents(subscribe_intent_callback).start()
    


if __name__ == "__main__":
    mqtt_opts = MqttOptions()
    with Hermes(mqtt_options=mqtt_opts) as h:
        h.subscribe_intent("mcitar:Volume", subscribe_intent_callback) \
         .start()
