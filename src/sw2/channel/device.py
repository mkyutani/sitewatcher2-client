from sw2.channel.interface_msteams import send_to_msteams
from sw2.channel.interface_slack import send_to_slack

def output_to_device(device_info, channel_resources, dry=False, skip=False):
    device_interface = device_info['interface'].lower()
    if device_interface == 'slack':
        return send_to_slack(device_info, channel_resources, dry=dry, skip=skip)
    elif device_interface == 'msteams':
        return send_to_msteams(device_info, channel_resources, dry=dry, skip=skip)
    else:
        return 1