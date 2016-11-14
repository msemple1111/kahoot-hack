import sys
from main import kahoot, error

def get_input():
  pin = input("Please Enter the kahoot pin: ")
  name = input("Please Enter your user name: ")
  try:
    return int(pin), str(name)
  except:
    print("Please input properly")
    error(0,"not proper input", True)

def esc():
  while send.end == False:
    if send.end == True:
      print("End!")

if __name__ == '__main__':
  try:
    name = sys.argv[1]
    pin = sys.argv[2]
  except:
      pin, name = get_input()
  print("connecting ...")
  send = kahoot(pin, name)
  send.connect()
  send.run_queue()
  esc()
