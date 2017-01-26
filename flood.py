####################################################
#  Settings:                                       #
####################################################

_verify = True   #if the network filters https traffic
                 #set to false to turn off verification



####################################################
from main import kahoot
import threading
import sys
import time

def kahoot_run(pin, x, name, verify):
  send = kahoot(pin, name+str(x+1))
  send.verify = verify
  send.connect()

def test_connection(pin):
  send = kahoot(pin, "Test Name")
  return send.testSession()

def find_two_factor_code(pin):
  send = kahoot(pin, "Test Name")
  send.reserve_session()
  while self.twoFactorCount < 24:
    time.sleep(0.05)
  if self.twoFactorSolved:
    print('true')
    print(self.twoFactor)
  else:
    print('false')

def start_kahoot_run():
  t = threading.Thread(target=kahoot_run, args=(pin,x,name,verify ))
  t.daemon = True
  t.start()

def get_input():
  try:
    name = sys.argv[1]
    pin = sys.argv[2]
    exc = sys.argv[3]
    if (len(sys.argv) > 4):
      if (sys.argv[4].lower() =='false'):
        verify = False
    else:
      verify = True
  except:
    pin = input("Please Enter the kahoot pin: ")
    name = input("Please Enter the base name: ")
    exc = input("Please Enter how many names to add: ")
    verify = _verify
  try:
    if (name == None) or (exc == None) or (pin == None):
      print("Please input properly")
      return get_input()
    else:
      return int(pin), str(name), int(exc), bool(verify)
  except:
    print("\nPlease input properly:")
    return get_input()

def esc():
  while True:
    esc = input("> ")
    if esc.lower() == 'e':
      break
    else:
      print("> invalid input")

if __name__ == '__main__':
  pin, name, exc, verify = get_input()
  if test_connection(pin):
    print("connecting ...")
    for x in range(exc):
      time.sleep(0.1)
      start_kahoot_run()
    print("\nFinished\nLeave running to keep accounts connected\nPress E to Exit")
    esc()
  else:
    print("Game does not exists with that pin")
