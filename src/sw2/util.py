import re

def is_uuid(id: str) -> bool:
    return re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', id) is not None

def to_printable(message: str) -> str:
    return ''.join([ch if ch >= ' ' else '.' for ch in message])

def analyze_rule(category, expression):
    contents = {}

    try:
        if category in ['include', 'exclude', 'start', 'stop']:
            src, value = expression.split(':', 1)
            contents['op'] = None
            contents['src'] = src
            contents['dst'] = None
            contents['value'] = value
        elif category == 'walk':
            items = expression.split(':', 2)
            if len(items) == 3:
                dst, src, value = items
                if len(value) == 0:
                    value = None
            elif len(items) == 2:
                dst, src = items
                value = None
            else:
                raise ValueError()
            contents['op'] = None
            contents['src'] = src.strip()
            contents['dst'] = dst.strip()
            contents['value'] = value
        elif category == 'property':
            op, expr = expression.split(':', 1)
            op = op.strip().lower()
            if op not in ['set', 'match', 'none']:
                raise ValueError()
            contents['op'] = op
            if op == 'set':
                dst, value = expr.split(':', 1)
                contents['src'] = None
                contents['dst'] = dst.strip()
                contents['value'] = value
            elif op == 'match':
                dst, src, value = expr.split(':', 2)
                contents['src'] = src.strip()
                contents['dst'] = dst.strip()
                contents['value'] = value
            else:
                raise ValueError()
        else:
            raise ValueError()
    except ValueError:
        if expression.lower() == 'none':
            contents['op'] = 'none'
            contents['src'] = None
            contents['dst'] = None
            contents['value'] = None
        else:
            return None

    return contents