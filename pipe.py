#!/usr/bin/python3
import re
import sys
import colorama
from jinja2 import Environment, FileSystemLoader, select_autoescape

# read avahi-browse -p (--parsable) from stdin and create fancy output
# helpful functions:
def parse_txt(txt):
    """Parse DNS-SD TXT records from `avahi-browse -p` into a dictionary.
    txt: string formatted like '"key=value" "key2=value2"' """
    # match records. returns [('key', 'value'), ...]
    # \S will need to be changed if spaces are allowed in values. probably yes...
    matches = re.findall(r'"(\w+)=(\S+)"',txt)
    records = { item[0]: item[1] for item in matches }
    return records

def colour(s): # could be a lambda but i find this clearer
    return colorama.Fore.GREEN + s + colorama.Fore.RESET

# parse everything
devices = []
for line in sys.stdin.readlines():
    parts = line.split(';')
    if parts[0] != '=': # = means 'resolved'
        continue
    device = {
        "hostname": parts[6],
        "ip": parts[7],
        "service": parts[4],
        "name": parts[3],
        "txt": parse_txt(parts[9])
    }
    devices.append(device)

# decide type of output, the default is text
mode = 'text'
if len(sys.argv) > 1:
    mode = sys.argv[1]

if mode == 'text':
    for d in devices:
        print(f"{d['name']} @ {d['hostname']} / {d['ip']}")
        print(f"{colour('service')}: {d['service']}")
        for key in d['txt']:
            print(f"{colour(key)}: {d['txt'][key]}")
        print("-"*10)

elif mode == 'html':
    env = Environment(
    	loader = FileSystemLoader("html"),
    	autoescape = select_autoescape()
    )
    template = env.get_template("devices.html")
    print(template.render(devices=devices, length=len))
