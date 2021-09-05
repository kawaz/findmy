import jsonpickle
import json
from pygments import highlight, lexers, formatters
def printjc(value):
    vj = jsonpickle.encode(value)
    vjj = json.dumps(json.loads(vj), sort_keys=True)
    vjc = highlight(vjj, lexers.JsonLexer(), formatters.TerminalFormatter())
    print(vjc)
def printj(value, max_depth=None, indent=None, sort_keys=True, **params):
    print(json.dumps(json.loads(jsonpickle.encode(value, max_depth=max_depth, **params)), sort_keys=sort_keys, indent=indent, **params))

import sys
orig_displayhook = sys.displayhook
def myhook(value):
    if value != None:
        __builtins__._ = value
        printjc(value)
if __builtins__:
    __builtins__.pprint_on = lambda: setattr(sys, 'displayhook', myhook)
    __builtins__.pprint_off = lambda: setattr(sys, 'displayhook', orig_displayhook)
    __builtins__.pprint_on()



from pyicloud import PyiCloudService
import os
api = PyiCloudService(os.environ['FINDMY_ACCOUNT_ID'])


if __name__ == '__main__':
    args = sys.argv
    if len(args) == 1:
        print("Usage:")
        print("  {0} device list".format(args[0]))
        sys.exit(1)
    if args[1] == "device":
        if args[2] == "list":
            for d in api.devices:
                data = d.data
                del data['features']
                # del data['msg']
                # del data['snd']
                # del data['location']
                printj(data, max_depth=2)
        elif args[2] == "play_sound":
            dev = api.devices[args[3]]
            if dev != None:
                printj(dev.play_sound())
                sys.exit(0)


