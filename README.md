##What is it?
####tl;dr
It "hacks" [kahoot.it](https://kahoot.it) quiz platform

##Story
Basically during one boring quiz on kahoot, I came up with another funny name before it was instantly banned.
I went on google looking for a tool to flood the game with names like 1000 times so the teacher cannot ban them all. I found one tool on github but it was broken with the developer having no intent of fixing it.
So I thought why not build my own suite of tools for script kiddies to troll their teacher. And here we are.

If your not very technical, I am going to create a website version of these tools soon, so stay tuned!

#Tools
Here are the tools:

flood.py - Spam the game lobby with many names (e.g. 1000)

play.py - play kahoot normally

Soon to come - crash.py - crashing the game of kahoot so it cannot be played


#Installing

This short guide is designed for either for python installed with IDLE or unix style command line (mac / linux or windows with cygwin installed).

##Prerequisites

- python 3  [Install Python 3](https://www.python.org/downloads/)

1. 
Download latest repo [here](https://github.com/msemple1111/kahoot-hack/archive/master.zip)

or clone the repo
```
git clone https://github.com/msemple1111/kahoot-hack.git
```

2. 
Get onto the correct folder. Either click into it or use the terminal command below.
```
cd kahoot-hack
```

##Usage

Either run using IDLE or run the command below to play or flood.

```
python play.py name pin
```
```
python flood.py name pin bot-count
```

### Restricted Network
If the network that you want to run this software from uses https mitm filtering, please add a false to the end of the command line.
```
python play.py name pin false
```
```
python flood.py name pin bot-count false
```

Or if your using IDLE, please change the setting at the top of flood.py of play.py
```
####################################################
#  Settings:                                       #
####################################################

_verify = True  
```
Change the "_verify" varible to equal "False".

#Faq

###Q. 
 My name is _insert-name_ and I want to use this tool to hack my teacher, Yeah!! 
 Can I do this?
 
#### A.
NO!! This suite of tools is intended to be used in test purposes only and no Liability to the owner or any of the contributors for anything done as the result of this program.


###Q. 
Can I use naughty names?
 
#### A.
Again, No! This suite of tools is NOT for putting in naughty names into the game.

###Q. 
Can I use this for test purposes only?
 
#### A.
Finally, a sensible question. Yes of course you can use this for test purposes only.





Boiiiiii shoudl make a kahoot lobby searcher tooooo
