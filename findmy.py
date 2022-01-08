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
from pyicloud.exceptions import PyiCloudNoStoredPasswordAvailableException
from pyicloud.utils import store_password_in_keyring
from getpass import getpass

import os

try:
    api = PyiCloudService(os.environ['FINDMY_ACCOUNT_ID'], cookie_directory=os.environ['FINDMY_COOKIE_DIR'])
except PyiCloudNoStoredPasswordAvailableException:
    print("No stored password available")
    password = getpass("Enter the password: ")
    api = PyiCloudService(os.environ['FINDMY_ACCOUNT_ID'], password, cookie_directory=os.environ['FINDMY_COOKIE_DIR'])
    store_password_in_keyring(os.environ['FINDMY_ACCOUNT_ID'], password)

if api.requires_2fa:
    print("Two-factor authentication required.")
    code = input("Enter the code you received of one of your approved devices: ")
    result = api.validate_2fa_code(code)
    print("Code validation result: {}".format(result))
    if not result:
        print("Failed to verify security code")
        sys.exit(1)
    if not api.is_trusted_session:
        print("Session is not trusted. Requesting trust...")
        result = api.trust_session()
        print("Session trust result {}".format(result))
        if not result:
            print("Failed to request trust. You will likely be prompted for the code again in the coming weeks")
elif api.requires_2sa:
    import click
    print("Two-step authentication required. Your trusted devices are:")
    devices = api.trusted_devices
    for i, device in enumerate(devices):
        print("  {}: {}".format(i, device.get("deviceName", "SMS to %s".format(device.get("phoneNumber")))))
    device = click.prompt("Which device would you like to use?", default=0)
    device = devices[device]
    if not api.send_verification_code(device):
        print("Failed to send verification code")
        sys.exit(1)
    code = click.prompt("Please enter validation code")
    if not api.validate_verification_code(device, code):
        print("Failed to verify verification code")
        sys.exit(1)


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

