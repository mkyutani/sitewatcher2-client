from sw2.env import Environment

def sw2_parser_config(subparser):
    parser = subparser.add_parser('config', help='Configure sitewatcher2 client')
    parser.add_argument('name', nargs='?', default=None, help='Name to configure')
    parser.add_argument('value', nargs='?', default=None, help='Value to set')
    return []

def sw2_config(args):
    name = args['name']
    value = args['value']
    if name is None:
        kv = Environment.get()
        for key in kv.keys():
            if kv[key] is not None:
                print(f'{key}={kv[key]}')
    elif value is None:
        value = Environment.get(name)
        if value is not None:
            print(f'{name}={value}')
    else:
        Environment.set(name, value)
        print(f'{name}={value}')

    return 0