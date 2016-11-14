import requests
import json
import time
import threading
import sys

def error(err_no, err_desc, end):
  import datetime
  print("Error")
  error_dec = "Time: "+str(datetime.datetime.now())+" Error no: " + str(err_no) + "  " + err_desc + "\n"
  with open('log.txt', 'a') as afile:
    afile.write(error_dec)
  if end:
    print('end')
    sys.exit()

class kahoot:
  def __init__(self, pin, name):
    self.pin = pin
    self.name = name
    self.s = requests.Session()
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
    self.subId = 12


  def ordinal(self, n):
    if 10 <= n % 100 < 20:
        return str(n) + 'th'
    else:
       return  str(n) + {1 : 'st', 2 : 'nd', 3 : 'rd'}.get(n % 10, "th")

  def make_first_payload(self):
    data = [{"advice": {"interval": 0, "timeout": 60000}, "channel": "/meta/handshake", "ext": {"ack": True, "timesync": {"l": 0, "o": 0, "tc": get_tc()}}, "id": "2", "minimumVersion" : "1.0", "supportedConnectionTypes": ["long-polling"], "version": "1.0"}]
    return str(json.dumps(data))

  def make_sub_payload(self, subId, chan, sub):
    chan = str(chan)
    subId = str(int(subId))
    sub = str(sub)
    data = [{"channel": "/meta/"+chan, "clientId": self.clientid, "ext": {"timesync": {"l": 5, "o": 0, "tc": get_tc()}}, "id": subId, "subscription": "/service/" + sub}]
    return str(json.dumps(data))

  def make_first_con_payload(self, subId):
    subId = str(int(subId))
    data = [{"advice": {"timeout": 0}, "channel": "/meta/connect", "clientId": self.clientid, "connectionType": "long-polling", "ext": {"ack": -1, "timesync": {"l": 5, "o": 15, "tc": get_tc()}}, "id": subId}]
    return str(json.dumps(data))

  def make_second_con_payload(self, ack):
    subId = str(int(self.subId))
    ack = int(ack)
    data = [{"channel": "/meta/connect", "clientId": self.clientid, "connectionType": "long-polling", "ext": {"ack": ack, "timesync": {"l": 12, "o": 133, "tc": get_tc()}}, "id": subId}]
    return str(json.dumps(data))

  def make_name_sub_payload(self, name):
    name = str(name)
    data = [{"channel": "/service/controller", "clientId": self.clientid, "data": {"gameid": self.pin, "host": "kahoot.it", "name": name, "type": "login"}, "id": "14"}]
    return str(json.dumps(data))

  def make_answer_payload(self, choice):
    subId = int(self.subId)
    choice = int(choice)
    innerdata = {"choice": choice, "meta": {"lag": 13, "device": {"userAgent": "bigup_jme", "screen": {"width": 1920, "height": 1080}}}}
    innerdata = json.dumps(innerdata)
    data = [{"channel": "/service/controller", "clientId": self.clientid, "data": {"content": innerdata, "gameid": self.pin, "host": "kahoot.it", "id": 6, "type": "message"}, "id": subId}]
    return str(json.dumps(data))

  def reserve_session(self):
    pin = str(self.pin)
    timecode = str(get_tc())
    url = "https://kahoot.it/reserve/session/"+pin+"/?"+timecode
    r = self.s.get(url)
    try:
        self.kahoot_session = r.headers['x-kahoot-session-token']
        return r.text == '{}'
    except:
        return False

  def ping_session(self):
    pin = str(self.pin)
    url = "https://kahoot.it/cometd/"+pin+"/"+self.kahoot_session
    try:
      r = self.s.get(url, headers=self.headers)
      if r.status_code != 400:
        error(100, str(r.status_code)+str(r.text),False)
    except requests.exceptions.ConnectionError:
      error(subId+200, "Conection error",False)
      print("Connection Refused")



  def handshake(self):
    pin = str(self.pin)
    url = "https://kahoot.it/cometd/"+pin+"/"+self.kahoot_session+"/handshake"
    data = self.make_first_payload()
    try:
      r = self.s.post(url, data=data, headers=self.headers)
      if r.status_code != 200:
        error(100, str(r.status_code)+str(r.text),False)
    except requests.exceptions.ConnectionError:
      error(107, "Conection error", True)
      print("Connection Refused")
    except:
      error(108, "handshake error", True)
    response = json.loads(r.text)
    return str(response[0]["clientId"])

  def send(self, func):
    pin = str(self.pin)
    data = func
    url = "https://kahoot.it/cometd/"+pin+"/"+self.kahoot_session+"/"
    try:
      r = self.s.post(url, data=data, headers=self.headers)
      if r.status_code != 200:
        error(subId+100, str(r.status_code)+str(r.text),False)
    except requests.exceptions.ConnectionError:
      error(subId+200, "Conection error",False)
      print("Connection Refused")
    response = json.loads(r.text)
    return response[0]["successful"] == True

  def connect_while(self):
    pin = str(self.pin)
    while True:
      self.subId = self.subId + 1
      data = self.make_second_con_payload(self.subId)
      url = "https://kahoot.it/cometd/"+pin+"/"+self.kahoot_session+"/connect"
      try:
        r = self.s.post(url, data=data, headers=self.headers)
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
        print(r)
        error(12, "self.connect_while error" + str(r.text), False)

  def ask_question(self, options, questionNo):
    options = list(options)
    questionNo = int(questionNo)
    print("List of options are:")
    for option in options:
      print(int(option)+1)
    while self.questionNo == questionNo:
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

  def do_id_7(self, dataContent):
    print(dataContent['primaryMessage'])

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

  def do_id_13(self, dataContent):
    print(dataContent['primaryMessage'], "\n"+ dataContent['secondaryMessage'])
    print("That is the end of this", dataContent['quizType']," well done!")
    self.end = True

  def do_id_14(self, dataContent):
    print("Connected\nYou joined this", dataContent['quizType'], "with the name", dataContent['playerName'])

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
    elif serviceID == 7:
      t = threading.Thread(target=self.do_id_7, args=(dataContent,))
    elif serviceID == 8:
      print("id-8")
      t = threading.Thread(target=self.do_id_8, args=(dataContent,))
    elif serviceID == 9:
      t = threading.Thread(target=self.do_id_9, args=(dataContent,))
    elif serviceID == 13:
      t = threading.Thread(target=self.do_id_13, args=(dataContent,))
    elif serviceID == 14:
      t = threading.Thread(target=self.do_id_14, args=(dataContent,))
    else:
      error(13, "serviceID out of range"+str(serviceID), True)
    t.start()

  def queue_wait(self):
    while True:
      while len(self.queue) > 0:
        for i, x in enumerate(self.queue):
          if x['channel'] == "/service/player":
            self.service_player(x['data'])
          self.queue.remove(x)
      time.sleep(0.5)


  def connect_first(self):
    pin = str(self.pin)
    data = self.make_first_con_payload(6)
    url = "https://kahoot.it/cometd/"+pin+"/"+self.kahoot_session+"/connect"
    try:
      r = self.s.post(url, data=data, headers=self.headers)
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
      print(r)
      error(12, "self.connect_first error" + str(r.text), False)

  def run_connect_while(self):
    t = threading.Thread(target=self.connect_while)
    t.daemon = True
    t.start()

  def run_connect_first(self):
    t = threading.Thread(target=self.connect_first)
    t.daemon = True
    t.start()

  def run_game(self):
    t = threading.Thread(target=self.queue_wait)
    t.daemon = True
    t.start()

  def connect(self):
    if self.reserve_session():
      self.ping_session()
      self.clientid = self.handshake()
      self.run_connect_first()
      subscribe_order = ["subscribe", "unsubscribe", "subscribe"]
      subscribe_text = ["controller", "player", "status"]
      for x in range(3):
        for y in range(3):
          self.send(self.make_sub_payload(x*3+(y+1), subscribe_text[y], subscribe_order[x]))
      self.run_connect_while()
      self.send(self.make_name_sub_payload(self.name))
    else:
      print("Error: no game with that pin")
      error(909,"no game with pin", True)

def get_tc():
  return int(time.time() * 1000)
