#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hermes_python.hermes import Hermes, MqttOptions
import datetime
import random
import toml
import alsaaudio

USERNAME_INTENTS = "mcitar"
MQTT_BROKER_ADDRESS = "localhost:1883"
MQTT_USERNAME = None
MQTT_PASSWORD = None

m = alsaaudio.Mixer('Master')
vol = m.getvolume()[0]

def user_intent(intentname):
    return USERNAME_INTENTS + ":" + intentname


def subscribe_intent_callback(hermes, intent_message):
    intentname = intent_message.intent.intent_name

    if intentname == user_intent("lauter"):
        vol = min(100,m.getvolume()[0] + 10)
        m.setvolume(vol)
        result_sentence = u"Lautstärke auf {} gesetzt".format(vol)

    elif intentname == user_intent("leiser"):
        vol = max(0,m.getvolume()[0] - 10)
        m.setvolume(vol)
        result_sentence = u"Lautstärke auf {} gesetzt".format(vol)

    elif intentname == user_intent("Volume"):
        if intentMessage.slots.volume:
            vol = intentMessage.slots.volume.first()
            m.setvolume(int(vol))
            result_sentence = u"Lautstärke auf {} gesetzt".format(vol)
        else:
            result_sentence = u"hab's leider nicht verstanden"

    hermes.publish_end_session(intentMessage.session_id, result_sentence)

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
        h.subscribe_intent("mcitar:lauter", subscribe_intent_callback)\
            .subscribe_intent("mcitar:leiser", subscribe_intent_callback) \
            .subscribe_intent("mcitar:Volume", subscribe_intent_callback) \
            .start()
