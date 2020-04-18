#!/usr/bin/python3
import os,sys
import pygame
import random

pygame.init()
screen=pygame.display.set_mode((720,480),pygame.HWSURFACE)
HEIGHT=screen.get_height()
WIDTH=screen.get_width()
KEYS={}
STOP=False

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

def pygame_input():
	keys=[]
	for key,pressed in KEYS.items():
		if not pressed:
			keys.append(key)
	for key in keys:
		del KEYS[key]
	return keys

def draw():
	screen.fill((0,0,0))
	pygame.draw.rect(screen,(255,255,255),(5,HEIGHT-5,WIDTH-10,-HEIGHT//20))
	pygame.display.flip()

def mainloop():
	while not STOP:
		event_handler()
		draw()
		for key in pygame_input():
			kn=pygame.key.name(key)
			if len(kn)==1:
				print(kn)

mainloop()
