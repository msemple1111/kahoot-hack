import os, sys, inspect
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"lib")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
import requests
import json
import time
import threading
import base64
import array
import urllib.parse

def error(err_no, err_desc, end, printErr=True):
  import datetime
  if printErr:
    print("Error:  "+str(err_no)+'  - ',err_desc)
  error_dec = "Time: "+str(datetime.datetime.now())+" Error no: " + str(err_no) + "  " + err_desc + "\n"
  with open('log.txt', 'a') as afile:
    afile.write(error_dec)
  if end:
    print('end')
    sys.exit()

def get_tc():
  return int(time.time() * 1000)

def get_o():
  return int(-14)

def get_l():
  return int(0)


class kahoot:
  def __init__(self, pin, name):
    self.pin = pin
    self.name = name
    self.s = requests.Session()
    self.verify = True
    #self.cookie = {'no.mobitroll.session': str(self.pin)}
    self.requests = {}
    self.headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:43.0) Gecko/20100101 Firefox/43.0',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Referer':'https://kahoot.it/'
        }

    self.queue = []
    self.questionNo = 0
    self.end = False
    self.kahoot_session = ''
    self.kahoot_raw_session = ''
    self.subId = 12
    self.ackId = 1
    self.challenge = 0
    self.twoFactor = ''
    self.twoFactorPromptShown = False
    self.twoFactorSolved = False
    self.twoFactorStarted = False
    self.twoFactorCount = 0

  def ordinal(self, n):
    if 10 <= n % 100 < 20:
        return str(n) + 'th'
    else:
       return  str(n) + {1 : 'st', 2 : 'nd', 3 : 'rd'}.get(n % 10, "th")

  def get_ackID(self):
      self.ackId = self.ackId + 1
      return self.ackId

  def make_first_payload(self):
    data = [{"advice": {"interval": 0, "timeout": 60000}, "channel": "/meta/handshake", "ext": {"ack": self.get_ackID(), "timesync": {"l": get_l(), "o": get_o(), "tc": get_tc()}}, "id": "2", "minimumVersion" : "1.0", "supportedConnectionTypes": ["long-polling"], "version": "1.0"}]
    return str(json.dumps(data))

  def make_sub_payload(self, chan, sub):
    self.subId = self.subId + 1
    subId = str(int(self.subId))
    chan = str(chan)
    sub = str(sub)
    data = [{"channel": "/meta/"+chan, "clientId": self.clientid, "ext": {"timesync": {"l": get_l(), "o": get_o(), "tc": get_tc()}}, "id": subId, "subscription": "/service/" + sub}]
    return str(json.dumps(data))

  def make_first_con_payload(self, subId):
    subId = str(int(subId))
    data = [{"advice": {"timeout": 0}, "channel": "/meta/connect", "clientId": self.clientid, "connectionType": "long-polling", "ext": {"ack": self.get_ackID(), "timesync": {"l": get_l(), "o": get_o(), "tc": get_tc()}}, "id": subId}]
    return str(json.dumps(data))

  def make_second_con_payload(self, ack):
    subId = str(int(self.subId))
    data = [{"channel": "/meta/connect", "clientId": self.clientid, "connectionType": "long-polling", "ext": {"ack": self.get_ackID(), "timesync": {"l": get_l(), "o": get_o(), "tc": get_tc()}}, "id": subId}]
    return str(json.dumps(data))

  def make_name_sub_payload(self, name):
    name = str(name)
    data = [{"channel": "/service/controller", "clientId": self.clientid, "data": {"gameid": self.pin, "host": "kahoot.it", "name": name, "type": "login"}, "id": "14"}]
    return str(json.dumps(data))

  def make_answer_payload(self, choice):
    subId = int(self.subId)
    choice = int(choice)
    innerdata = {"choice": choice, "meta": {"lag": 13, "device": {"userAgent": "bigup_UK_grime", "screen": {"width": 1920, "height": 1080}}}}
    innerdata = json.dumps(innerdata)
    data = [{"channel": "/service/controller", "clientId": self.clientid, "data": {"content": innerdata, "gameid": self.pin, "host": "kahoot.it", "id": 6, "type": "message"}, "id": subId}]
    return str(json.dumps(data))

  def make_two_factor_payload(self, choice):
    subId = int(self.subId)
    choice = str(choice)
    innerdata = {"sequence" : choice}
    innerdata = json.dumps(innerdata)
    data = [{"channel": "/service/controller", "clientId": self.clientid, "data": {"content": innerdata, "gameid": self.pin, "host": "kahoot.it", "id": 50, "type": "message"}, "id": subId}]
    return str(json.dumps(data))

  def testSession(self):
    pin = str(self.pin)
    timecode = str(get_tc())
    url = "https://kahoot.it/reserve/session/"+pin+"/?"+timecode
    r = self.s.get(url, verify=self.verify)
    try:
      data = json.loads(r.text)
      self.kahoot_raw_session = r.headers['x-kahoot-session-token']
      self.challenge = self.solve_kahoot_challenge(data['challenge'])
      self.kahoot_session = self.kahoot_session_shift()
      return True
    except:
      error(909, 'No kahoot Game with that pin', False, False)
      return False

  def solve_kahoot_challenge(self, challenge):
    s1 = challenge.find('this,')+7
    s2 = challenge.find("');")
    message = challenge[s1:s2]
    s1 = challenge.find('var offset')+13
    s2 = challenge.find('; if')
    offset = str("".join(challenge[s1:s2].split()))
    offset = eval(offset)
    def repl(char, position):
        return chr((((ord(char)*position) + offset)% 77)+ 48)
    res = ""
    for i in range(0,len(message)):
        res+=repl(message[i],i)
    return res

  def kahoot_session_shift(self):
    kahoot_session_bytes = base64.b64decode(self.kahoot_raw_session)
    challenge_bytes = str(self.challenge).encode("ASCII")
    bytes_list = []
    for i in range(len(kahoot_session_bytes)):
        bytes_list.append(kahoot_session_bytes[i] ^ challenge_bytes[i%len(challenge_bytes)])
    return array.array('B',bytes_list).tostring().decode("ASCII")

  def startSession(self):
    pin = str(self.pin)
    url = "https://kahoot.it/cometd/"+pin+"/"+self.kahoot_session
    try:
      r = self.s.get(url, headers=self.headers, verify=self.verify)
      if r.status_code != 400:
        error(1001, str(r.status_code)+str(r.text),False)
    except requests.exceptions.ConnectionError:
      error(self.subId+200, "Conection error",False)
      print("Connection Refused")

  def handshake(self):
    pin = str(self.pin)
    url = "https://kahoot.it/cometd/"+pin+"/"+self.kahoot_session+"/handshake"
    data = self.make_first_payload()
    try:
      r = self.s.post(url, data=data, headers=self.headers, verify=self.verify)
      if r.status_code != 200:
        error(1002, str(r.status_code)+str(r.text),False)
    except requests.exceptions.ConnectionError:
      error(107, "Conection error", True)
      print("Connection Refused")
    except:
      error(108, "handshake error", True)
    response = json.loads(r.text)
    return str(response[0]["clientId"])

  def send(self, dataIn, urlIn=None):
    pin = str(self.pin)
    data = str(dataIn)
    if urlIn is None:
      url = "https://kahoot.it/cometd/"+pin+"/"+self.kahoot_session+"/"
    else:
      url = urlIn
    try:
      r = self.s.post(url, data=data, headers=self.headers, verify=self.verify)
      if r.status_code != 200:
        error(self.subId+100, str(r.status_code)+str(r.text),False)
    except requests.exceptions.ConnectionError:
      error(self.subId+200, "Conection error",False)
      print("Connection Refused")
    try:
      response = json.loads(r.text)
    except:
      error(self.subId, "response cannot be processed",False)
    for x in range(len(response)):
      if "successful" in response[x]:
        if response[x]["successful"] != True:
          return None
    else:
        return response
    error(918, str(r.status_code)+" "+str(response),True)
    return None

  def connect_while(self):
    pin = str(self.pin)
    while True:
      self.subId = self.subId + 1
      data = self.make_second_con_payload(self.subId)
      url = "https://kahoot.it/cometd/"+pin+"/"+self.kahoot_session+"/connect"
      try:
        r = self.s.post(url, data=data, headers=self.headers, verify=self.verify)
        if r.status_code != 200:
          error(self.subId+100, str(r.status_code)+str(r.text),False)
      except requests.exceptions.ConnectionError:
        error(self.subId+200, "Conection error",False)
        print("Connection Refused")
      try:
        response = json.loads(r.text)
        if len(response) > 0:
          for i,x in enumerate(response):
            if x['channel'] != "/meta/connect":
              self.queue.append(x)
      except:
        error(12, "self.connect_while error" + str(r.text), False)

  def ask_question(self, options, questionNo):
    options = list(options)
    questionNo = int(questionNo)
    print("List of options are:")
    for option in options:
      print(int(option)+1)
    while self.questionNo == questionNo:
      answer = -1
      try:
        answer = int(input("Enter your answer: "))
        questionNo = questionNo - 1
        answer = answer - 1
      except:
        print("your answer is not is the list of options1")
      if str(answer) in options:
        return int(answer)
      else:
        print("your answer is not is the list of options2")

  def do_id_1(self, dataContent):
    questionNo = int(dataContent['questionIndex'])
    print("Question number: ", questionNo+1)
    self.questionNo = questionNo

  def do_id_2(self, dataContent):
    options = []
    questionNo = int(dataContent['questionIndex'])
    for i,x in enumerate(dataContent['answerMap']):
      options.append(x)
    answer = self.ask_question(sorted(options), questionNo)
    self.send(self.make_answer_payload(answer))


  def do_id_3(self, dataContent):
    print("End of quiz! \nYou came", self.ordinal(dataContent['rank']), "out of", dataContent['playerCount'],"players")
    print("You got", dataContent['totalScore'], "points")
    print("You got", dataContent['correctCount'], "Questions correct and", dataContent['incorrectCount'], "Questions incorect and had", dataContent['unansweredCount'], "Questions unanswered")

  def do_id_4(self, dataContent):
    print("End of question", dataContent['questionNumber'])
    self.questionNo = dataContent['questionNumber'] - 1

  def do_id_5(self, dataContent):
    print('end')

  def do_id_7(self, dataContent):
    print('\n'+dataContent['primaryMessage'])

  def do_id_8(self, dataContent):
    print("id-8")
    if dataContent['isCorrect']:
      print("Well Done, You got that question Correct!")
    else:
      print("Bad luck, You got that question incorrect!")
      if len(dataContent['correctAnswers']) > 1:
        print("The correct answers are:")
      else:
        print("The correct answer is:")
      for x in dataContent['correctAnswers']:
        print(x)
    print("You got",dataContent['points'], "points\nand current score is", dataContent['totalScore'])
    print("You are", self.ordinal(dataContent['rank']))
    if dataContent['nemesis'] == None:
      print("Well done!")
    elif dataContent['totalScore'] == dataContent['nemesis']['totalScore']:
      print("Your tied with", dataContent['nemesis']['name'])
    elif dataContent['totalScore'] < dataContent['nemesis']['totalScore']:
      print("Your behind", dataContent['nemesis']['name'], "by", (dataContent['nemesis']['totalScore']- dataContent['totalScore']), "points")

  def do_id_9(self, dataContent):
    print("The name of this", dataContent['quizType'], "is", dataContent['quizName'], ". It has", len(dataContent['quizQuestionAnswers']), "Questions")

  def do_id_10(self, dataContent):
    print("end")
    self.end == True

  def do_id_12(self, dataContent):
    print("finish")

  def do_id_13(self, dataContent):
    print(dataContent['primaryMessage'], "\n"+ dataContent['secondaryMessage'])
    print("That is the end of this", dataContent['quizType']," well done!")
    self.end = True

  def do_id_14(self, dataContent):
    print("Connected\nYou joined this", dataContent['quizType'], "with the name", dataContent['playerName'])

  def do_id_51(self, dataContent):
    print("Wrong Two factor code")
    self.twoFactorStarted = False

  def do_id_52(self, dataContent):
    print("Two factor code correct")
    self.twoFactorSolved = True

  def get_two_factor(self):
    if self.twoFactorPromptShown != True:
      print("Quiz needs a two factor code")
      print("Enter the first letter of the shape\n\n[t] for triangle\n[d] for Diamond\n[c] for circle\n[s] for square")
      print("Enetr it as one string,if it was a Triangle, Diamond, Circle and then Square")
      print("you would enter [tdcs]")
      self.twoFactorPromptShown = True
    else:
      print("enter two factor code again:")
    stringTwoFactor = str(input())
    if stringTwoFactor.isalpha():
      listTwoFactor = list(stringTwoFactor)
      if len(listTwoFactor) == 4:
        for i in range(len(listTwoFactor)):
          choices = {'t': '0', 'd': '1', 'c': '2', 's': '3'}
          listTwoFactor[i] = choices.get(listTwoFactor[i].lower(), '9')
        self.twoFactor = ''.join(listTwoFactor)
      else:
        print("Please enter a 4 letter code like [tdcs] excluding the brackets")
    else:
      print("Enter leters only please")

  def do_id_53(self, dataContent):
    while not self.twoFactorSolved:
      if not self.twoFactorStarted:
        self.twoFactorStarted = True
        self.get_two_factor()
        self.send(self.make_two_factor_payload(self.twoFactor))

  def service_player(self, data):
    serviceID = data['id']
    dataContent = json.loads(data['content'])
    if serviceID == 1:
      t = threading.Thread(target=self.do_id_1, args=(dataContent,))
    elif serviceID == 2:
      t = threading.Thread(target=self.do_id_2, args=(dataContent,))
    elif serviceID == 3:
      t = threading.Thread(target=self.do_id_3, args=(dataContent,))
    elif serviceID == 4:
      t = threading.Thread(target=self.do_id_4, args=(dataContent,))
    elif serviceID == 5:
      t = threading.Thread(target=self.do_id_5, args=(dataContent,))
    elif serviceID == 7:
      t = threading.Thread(target=self.do_id_7, args=(dataContent,))
    elif serviceID == 8:
      t = threading.Thread(target=self.do_id_8, args=(dataContent,))
    elif serviceID == 9:
      t = threading.Thread(target=self.do_id_9, args=(dataContent,))
    elif serviceID == 10:
      t = threading.Thread(target=self.do_id_10, args=(dataContent,))
    elif serviceID == 12:
      t = threading.Thread(target=self.do_id_12, args=(dataContent,))
    elif serviceID == 13:
      t = threading.Thread(target=self.do_id_13, args=(dataContent,))
    elif serviceID == 14:
      t = threading.Thread(target=self.do_id_14, args=(dataContent,))
    elif serviceID == 51:
      t = threading.Thread(target=self.do_id_51, args=(dataContent,))
    elif serviceID == 52:
      t = threading.Thread(target=self.do_id_52, args=(dataContent,))
    elif serviceID == 53:
      t = threading.Thread(target=self.do_id_53, args=(dataContent,))
    else:
      error(13, "serviceID out of range"+str(serviceID), True)
    t.start()

  def twoFactorSolver(self):
    combinations = ['0123', '0132', '0213', '0231', '0321', '0312', '1023', '1032', '1203', '1230', '1302', '1320', '2013', '2031', '2103', '2130', '2301', '2310', '3012', '3021', '3102', '3120', '3201', '3210']
    # self.send_two_factor_code('0123')
    for combo in combinations:
      if not self.twoFactorSolved:
        t = threading.Thread(target=self.send_two_factor_code, args=(combo,))
        #t.daemon = True
        t.start()

  def send_two_factor_code(self, combo):
    pin = str(self.pin)
    url = "https://kahoot.it/cometd/"+pin+"/"+self.kahoot_session+"/connect"
    response = self.send(self.make_two_factor_payload(combo),url)
    print(response)
    try:
      for x in range(len(response)):
        self.queue.add(x)
    except:
        print('its fucked m8\n\n')
    self.twoFactorCount = self.twoFactorCount + 1

  def queue_wait(self):
    while True:
      while len(self.queue) > 0:
        for i, x in enumerate(self.queue):
          if x['channel'] == "/service/player":
            self.service_player(x['data'])
          self.queue.remove(x)
      else:
        time.sleep(0.05)

  def queue_wait_flood(self):
    while True:
      while len(self.queue) > 0:
        for x in range(len(self.queue)):
          if response[x]['data']['id'] == 52:
            self.twoFactor = combo
            self.twoFactorSolved = True
        self.queue.remove(x)
      else:
        time.sleep(0.05)

  def connect_first(self):
    pin = str(self.pin)
    data = self.make_first_con_payload(6)
    url = "https://kahoot.it/cometd/"+pin+"/"+self.kahoot_session+"/connect"
    try:
      r = self.s.post(url, data=data, headers=self.headers, verify=self.verify)
      if r.status_code != 200:
        error(self.subId+100, str(r.status_code)+str(r.text),False)
    except requests.exceptions.ConnectionError:
      error(self.subId+200, "Conection error",False)
      print("Connection Refused")
    try:
      response = json.loads(r.text)
      if len(response) > 1:
        for i,x in enumerate(response):
          if x['channel'] != "/meta/connect":
            self.queue.append(x)
    except:
      error(12, "self.connect_first error" + str(r.text), False)

  def startQueue(self):
    t = threading.Thread(target=self.connect_while)
    t.daemon = True
    t.start()

  def setName(self, name):
    self.send(self.make_name_sub_payload(name))

  def enterSession(self):
    t = threading.Thread(target=self.connect_first)
    t.daemon = True
    t.start()
    subscribe_order = ["subscribe", "unsubscribe", "subscribe"]
    subscribe_text = ["controller", "player", "status"]
    for x in range(3):
      for y in range(3):
        self.send(self.make_sub_payload(subscribe_text[y], subscribe_order[x]))

  def run_game(self):
    t = threading.Thread(target=self.queue_wait)
    t.daemon = True
    t.start()

  def run_a_game(self):
    t = threading.Thread(target=self.queue_wait_flood)
    t.daemon = True
    t.start()

  def connect(self):
    if self.testSession():
      self.startSession()
      self.clientid = self.handshake()
      self.enterSession()
      self.startQueue()
      self.setName(self.name)
    else:
      error(909, "no game with pin", True)
