#!/usr/bin/python3
#note that this isn't representative of Riedler's average quality of code.
#this is literal shit code-wise.
print("Importing libraries...")
import os,sys
import pygame
import random,json
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
WORD=""
TRANSLATION=""
INDEX=0
PREVINDEX=0
SCORE=0
PREVSCORE=0
print("Initializing Fonts...")
normfont=pygame.font.SysFont("Arial",10)
bigfont=pygame.font.SysFont("Arial",13,bold=True)
print("Initializing Surfaces")
WORDSURF=bigfont.render("",True,BLACK)
TRANSSURF=bigfont.render("",True,WHITE)
SCORESURF=normfont.render("SCORE: 0",True,WHITE)
WORDHISTORY=pygame.Surface((WIDTH-10,HEIGHT-5-HEIGHT//20-SCORESURF.get_height()),pygame.SRCALPHA)
print("Loading vocabulary...")
with open("./test.json") as f:
	VOCABS=json.load(f)
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
	screen.blit(TRANSSURF,(WIDTH-TRANSSURF.get_width(),0))
	pygame.display.flip()

def mainloop():
	choose_word()
	while not STOP:
		event_handler()
		draw()
		for key in pygame_input():
			kn=chr(key)
			check_letter(kn)

print("\033[32meverything good\033[0m")
print("Vocabulary:")
for lang, data in VOCABS.items():
	print(" ",lang,end=":\n")
	for pair in data.items():
		print("    %s→%s"%pair)
mainloop()
