#!/usr/bin/python3
#note that this isn't representative of Riedler's average quality of code.
#this is literal shit code-wise.
import sys
argv=sys.argv
if "-h" in argv or "--help" in argv:
	print("Usage: python3 speedtranslate.py file\nThis game uses the CommonCodes 1.0.0 Standard for error messages.\nFor further information see here: https://mfederczuk.github.io/commoncodes/v2.html")
	exit(0)
print("Importing libraries...")
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import random,json
from time import time
from commoncodes import CommonCode
print("handling arguments...")
if len(argv)<2:
	raise CommonCode(3,"speedtranslate","file")
elif len(argv)>2:
	raise CommonCode(4,"speedtranslate",str(len(argv)-2))
print("Initializing pygame...")
pygame.init()
screen=pygame.display.set_mode((720,480),pygame.HWSURFACE)
print("Setting variables...")
HEIGHT=screen.get_height()
WIDTH=screen.get_width()
WHITE=(255,255,255)
BLACK=(0,0,0)
KEYS={}
STOP=False
END=False
WORD=""
TRANSLATION=""
INDEX=0
PREVINDEX=0
SCORE=0
PREVSCORE=0
endt=time()+30
print("Initializing Fonts...")
normfont=pygame.font.SysFont("Arial",10)
bigfont=pygame.font.SysFont("Arial",13,bold=True)
hugefont=pygame.font.SysFont("Arial",42,bold=True)
print("Initializing Surfaces")
WORDSURF=bigfont.render("",True,BLACK)
TRANSSURF=bigfont.render("",True,WHITE)
ENDMSG=hugefont.render("END",True,WHITE)
SCORESURF=normfont.render("SCORE: 0",True,WHITE)
TIMESURF=normfont.render("TIME: 30",True,WHITE)
WORDHISTORY=pygame.Surface((WIDTH-10,HEIGHT-5-HEIGHT//20-SCORESURF.get_height()),pygame.SRCALPHA)
print("Loading vocabulary...")
if os.path.exists(argv[1]):
	if os.path.isfile(argv[1]):
		with open(argv[1],"r") as f:
			VOCABS=json.load(f)
	else:
		raise CommonCode(25,argv[1],"file")
else:
	raise CommonCode(24,argv[1],"file or directory")
print("Defining functions...")
def event_handler():
	global STOP, KEYS
	for event in pygame.event.get():
		if event.type==pygame.KEYDOWN:
			KEYS[event.key]=True
		elif event.type==pygame.KEYUP:
			KEYS[event.key]=False
		elif event.type==pygame.QUIT:
			STOP=True

def timer():
	global TIMESURF,END
	curtime=endt-time()
	if curtime<=0:
		END=True
	else:
		TIMESURF=normfont.render("TIME: %02i"%curtime,True,WHITE)

def check_key(key):
	if key in KEYS.keys():
		return KEYS[key]
	else:
		return None

def choose_word():
	global INDEX,WORD,TRANSLATION,TRANSSURF
	INDEX=0
	lang=tuple(VOCABS.values())[random.randrange(len(VOCABS))]
	i=random.randrange(len(lang))
	WORD,TRANSLATION=tuple(lang.items())[i]
	TRANSSURF=bigfont.render(TRANSLATION,True,WHITE)

def check_letter(l):
	global INDEX,WORD,SCORE
	if l.lower()==WORD[INDEX].lower():
		INDEX+=1
	if INDEX==len(WORD):
		SCORE+=1
		WORDHISTORY.fill((0,0,0,random.randint(10,16)),special_flags=pygame.BLEND_RGBA_SUB)
		WS=bigfont.render(WORD,True,WHITE)
		WORDHISTORY.scroll(0,-(WS.get_height()+2))
		WORDHISTORY.fill((0,0,0),(0,WORDHISTORY.get_height()-WS.get_height(),WIDTH-10,WS.get_height()))
		WORDHISTORY.blit(WS,(0,WORDHISTORY.get_height()-WS.get_height()))
		choose_word()

def pygame_input():
	keys=[]
	for key,pressed in KEYS.items():
		if not pressed:
			keys.append(key)
	for key in keys:
		del KEYS[key]
	return keys

def draw():
	global SCORE,PREVSCORE,SCORESURF,PREVINDEX,WORDSURF
	screen.fill((0,0,0))
	pygame.draw.rect(screen,(255,255,255),(5,HEIGHT-5,WIDTH-10,-HEIGHT//20))
	if SCORE!=PREVSCORE:
		PREVSCORE=SCORE
		SCORESURF=normfont.render("SCORE: %i"%SCORE,True,WHITE)
	if INDEX!=PREVINDEX:
		PREVINDEX=INDEX
		WORDSURF=bigfont.render(WORD[:INDEX],True,BLACK)
	screen.blit(WORDHISTORY,(5,normfont.get_height()))
	screen.blit(WORDSURF,(10,HEIGHT-5-HEIGHT//40-WORDSURF.get_height()//2))
	screen.blit(SCORESURF,(0,0))
	screen.blit(TIMESURF,(0,SCORESURF.get_height()))
	screen.blit(TRANSSURF,(WIDTH-TRANSSURF.get_width(),0))
	if END:
		screen.blit(ENDMSG,(WIDTH//2-ENDMSG.get_width()//2,HEIGHT//2-ENDMSG.get_height()//2))
	pygame.display.flip()

def mainloop():
	choose_word()
	while not STOP:
		event_handler()
		timer()
		draw()
		if not END:
			for key in pygame_input():
				check_letter(chr(key))

print("\033[32meverything good\033[0m")
print("Vocabulary:")
for lang, data in VOCABS.items():
	print(" ",lang,end=":\n")
	for pair in data.items():
		print("    %s→%s"%pair)
mainloop()
