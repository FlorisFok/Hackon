import pygame, sys
from PIL import Image
import pytesseract
import argparse
import cv2
import os
import sys
import re

pygame.init()

def displayImage( screen, px, topleft):
     screen.blit(px, px.get_rect())
     if topleft:
         pygame.draw.rect( screen, (128,128,128), pygame.Rect(topleft[0], topleft[1], pygame.mouse.get_pos()[0] - topleft[0], pygame.mouse.get_pos()[1] - topleft[1]))
     pygame.display.flip()

def setup(path):
     px = pygame.image.load(path)
     screen = pygame.display.set_mode( px.get_rect()[2:] )
     screen.blit(px, px.get_rect())
     pygame.display.flip()
     return screen, px

def mainLoop(screen, px):
     topleft = None
     bottomright = None
     n=0
     while n!=1:
         for event in pygame.event.get():
             if event.type == pygame.MOUSEBUTTONUP:
                 if not topleft:
                     topleft = event.pos
                 else:
                     bottomright = event.pos
                     n=1
         displayImage(screen, px, topleft)
     return ( topleft + bottomright )

if __name__ == "__main__":
    file = sys.argv[1]

    for file in os.listdir(file):
        input_loc = "ABN_AMRO_Group_Annual-Report_2018_readable-012.png"
        input_loc = file

        screen, px = setup(input_loc)
        left, upper, right, lower = mainLoop(screen, px)
        im = Image.open(input_loc)
        im = im.crop(( left, upper, right, lower))
        pygame.display.quit()
        c = 0
        for i in range(2):
            try:
                file = f'image{c}.png'
                im.save( file, 'png')
                break
            except:
                c +=1

        gray = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
        # cv2.imshow('ImageWindow', gray)
        cv2.imwrite("gray2.png", gray)
        text = pytesseract.image_to_string(Image.open('gray2.png'))


        numbers = [ re.findall('\\b\\d+\\b', i) for i in text.split('\n') if not i == '']

        total = 0
        for num in numbers:
            try:
                total += float(num[0])+float(num[1])*0.1
            except:
                total += float(num[0])

        print(total)
