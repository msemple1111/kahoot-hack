from main import kahoot
import threading
import sys
import time

def kahoot_run(pin, x, name):
  send = kahoot(pin, name+str(x))
  send.connect()

def test_connection(pin):
  send = kahoot(pin, "Test Name")
  return send.reserve_session()

def start_kahoot_run():
  t = threading.Thread(target=kahoot_run, args=(pin,x,name,))
  t.daemon = True
  t.start()

def get_input():
  try:
    name = sys.argv[1]
    pin = sys.argv[2]
    exc = sys.argv[3]
    return int(pin), str(name), int(exc)
  except:
    pin = input("Please Enter the kahoot pin: ")
    name = input("Please Enter the base name: ")
    exc = input("Please Enter how many names to add: ")
  try:
    if (name == None) or (exc == None) or (pin == None):
      print("Please input properly")
      return None, None, None
    else:
      return int(pin), str(name), int(exc)
  except:
    print("Please input properly")
    error(0,"not proper input", True)

def esc():
  while True:
    esc = input("> ")
    if esc.lower() == 'e':
      break
    else:
      print("> invalid input")

if __name__ == '__main__':
  pin, name, exc = get_input()
  if test_connection(pin):
    print("connecting ...")
    for x in range(exc):
      time.sleep(0.1)
      start_kahoot_run()
    print("\nFinished\nLeave running to keep accounts connected\nPress E to Exit")
    esc()
  else:
    print("Game does not exists with that pin")
