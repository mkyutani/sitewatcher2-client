from sw2.channel.interface_msteams import send_to_msteams
from sw2.channel.interface_slack import send_to_slack

def output_to_device(device_info, channel_resources, sending=False):
    device_interface = device_info['interface'].lower()
    if device_interface == 'slack':
        return send_to_slack(device_info, channel_resources, sending=sending)
    elif device_interface == 'msteams':
        return send_to_msteams(device_info, channel_resources, sending=sending)
    else:
        return 1