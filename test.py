import sys
from main import kahoot, error
def esc():
  while send.end == False:
    if send.end == True:
      print("End!")

if __name__ == '__main__':
  pin = sys.argv[2]
  name = sys.argv[1]
  print("connecting ...")
  send = kahoot(pin, name)
  send.reserve_session()
  print(send.find_kahoot_session())
  print(send.kahoot_session)
  #esc()

  # if send.reserve_session():
  #   send.ping_session()
  #   print( send.handshake())
