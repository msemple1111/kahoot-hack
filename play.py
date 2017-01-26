import sys
from main import kahoot, error
import time

def get_input():
  try:
    name = sys.argv[1]
    pin = sys.argv[2]
    if (len(sys.argv) > 3):
      if (sys.argv[3].lower() =='false'):
        verify = False
    else:
        verify = True
  except:
    pin = input("Please Enter the kahoot pin: ")
    name = input("Please Enter your user name: ")
    verify = True
  try:
    return int(pin), str(name), bool(verify)
  except:
    print("Please input properly")
    error(0,"not proper input", True)

def esc():
  while send.end == False:
    if send.end == True:
      print("End!")
    else:
      time.sleep(0.1)

if __name__ == '__main__':
  pin, name, verify = get_input()
  print("connecting ...")
  send = kahoot(pin, name)
  send.verify = verify
  send.connect()
  send.run_game()
  esc()
