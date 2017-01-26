import sys
import time
from main import kahoot, error
def esc():
  while send.end == False:
    if send.end == True:
      print("End!")

def find_two_factor_code(pin):
  send.twoFactorSolver()
  while send.twoFactorCount < 24:
    time.sleep(0.05)
  print('fin')
  if send.twoFactorSolved:
    print('true')
    print(send.twoFactor)
  else:
    print('false')

pin = sys.argv[1]
send = kahoot(pin, "TestName3")
if __name__ == '__main__':
  #name = sys.argv[2]
  send.testSession()
  #send.startSession()
  send.clientid = send.handshake()
  # send.enterSession()
  # print(send.clientid)
  send.run_a_game()
  print("connecting ...")
  #send.connect()
  print('connected')
  #send.run_game()
  time.sleep(1)
  print('start')
  find_two_factor_code(pin)
  #find_two_factor_code(pin)
  print(send.twoFactor)
  #send = kahoot(pin, name)
  #send.reserve_session()
  #print(send.find_kahoot_session())
  #print(send.kahoot_session)
  #esc()

  # if send.reserve_session():
  #   send.ping_session()
  #   print( send.handshake())
