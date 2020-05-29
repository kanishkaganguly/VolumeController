#!/usr/bin/env python3

import pulsectl
import notify2
from sys import argv


def notify(vol):
    notify2.init("Volume Controller")
    n = notify2.Notification("Setting volume: {}".format(vol))
    n.set_urgency(notify2.URGENCY_NORMAL)
    n.set_timeout(1000)
    n.show()


def get_sink_by_name(sink_name, pulse):
    for sink in pulse.sink_list():
        if sink_name == sink.name:
            return sink


def get_card_by_name(card_name, pulse):
    for card in pulse.card_list():
        if card_name == card.name:
            return card


sink_list = {
    'headphones':
    'alsa_output.usb-GeneralPlus_USB_Audio_Device-00.analog-stereo',
    'speakers': 'alsa_output.pci-0000_0c_00.3.analog-stereo'
}

card_list = {
    'headphones': 'alsa_card.usb-GeneralPlus_USB_Audio_Device-00',
    'speakers': 'alsa_card.pci-0000_0c_00.3'
}

output_profile_list = {
    'headphones': 'output:analog-stereo+input:analog-mono',
    'speakers': 'output:analog-stereo'
}

pulse = pulsectl.Pulse('VolumeController')
try:
    if len(argv) > 1 and len(argv) == 2:
        # Target sink name
        target_sink_name = str(argv[1])
        print("Switching to {}".format(target_sink_name))
        # Get target sink
        target_sink = get_sink_by_name(sink_list[target_sink_name], pulse)
        # Switch default sink to target sink
        pulse.sink_default_set(target_sink)
        # Get available input sinks
        input_sink = pulse.sink_input_list()[0]
        # Switch sinks now
        pulse.sink_input_move(input_sink.index, target_sink.index)
    elif len(argv) > 2:
        print("Usage: python3 vol_test.py [speakers|headphones]")
except pulsectl.PulseOperationFailed as e:
    print("Error")

# try:
#     if len(argv) > 1 and len(argv) == 2:
#         source_name = str(argv[1])
#         print("Switching to {}".format(source_name))
#         card = get_card_by_name(card_list[source_name], pulse)
#         print("{} {}".format(card.index, output_profile_list[source_name]))
#         pulse.card_profile_set_by_index(card.index,
#                                         output_profile_list[source_name])
#     elif len(argv) > 2:
#         print("Usage: python3 vol_test.py [speakers|headphones]")
# except pulsectl.PulseOperationFailed as e:
#     print("Error")

# set_vol = 1.0
# volume = sink.volume
# volume.value_flat = set_vol
# pulse.volume_set(sink, volume)
# notify(set_vol * 100)

pulse.close()