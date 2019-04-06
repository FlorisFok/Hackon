
import pygame, sys
from PIL import Image
import pytesseract
import argparse
import cv2
import os
import sys
import re

def croppng2sum(pil_image, point=False, thershold=True):


    text = pytesseract.image_to_string(pil_image)

    numbers = [ re.findall('\\b\\d+\\b', i) for i in text.split('\n') if not i == '']

    total = 0
    if len(numbers) > 0:
        if point:
            for num in numbers:
                try:
                    total += float(num[0])+float(num[1])*0.1
                except:
                    total += float(num[0])
        else:
            for num in numbers:
                number = ''
                for s in num:
                    number += s
                total += int(number)
    else:
        message = 'One or less number found'

    return total
