def beautify(string):
    return string.replace('_', ' ').replace('-', ' ').title()

def unbeautify(string):
    return string.replace(' ', '-').lower()

MAX_LEN = 40
def generate_short_title(title):
    short_title = title or 'Untitled'
    if len(title) >= MAX_LEN:
        short_title = title[:MAX_LEN - len(' ... ')] + ' ... '
    short_title = short_title.replace('$', '')
    return short_title

