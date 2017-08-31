#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image,ImageEnhance,ImageFilter
from PIL import ImageOps
import urllib, cStringIO
import pytesseract

def binarizing(img,threshold): #input: gray image
    pixdata = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            if pixdata[x, y] < threshold:
                pixdata[x, y] = 0
            else:
                pixdata[x, y] = 255
    return img

def depoint(img):   #input: gray image
    pixdata = img.load()
    w,h = img.size
    for y in range(1,h-1):
        for x in range(1,w-1):
            count = 0
            if pixdata[x,y-1] > 245:
                count = count + 1
            if pixdata[x,y+1] > 245:
                count = count + 1
            if pixdata[x-1,y] > 245:
                count = count + 1
            if pixdata[x+1,y] > 245:
                count = count + 1
            if count > 2:
                pixdata[x,y] = 255
    return img


if __name__ == '__main__':

    # 開啟檔案
    img = Image.open("captcha_sample1.jpg")

    # 進行灰階轉換 ( RGB => Gray )
    img = img.convert('L')

    # 顏色反轉 ( 黑底白字 => 白底黑字 )
    img = ImageOps.invert(img)

    # 二值化
    img = binarizing(img,45)

    # 去噪
    img = depoint(img)

    # 辨識 (由於這個範例中辨識碼只有數字，因此指定輸出字元為 0~9 )
    out = pytesseract.image_to_string( img,config='-psm 7 -c tessedit_char_whitelist=0123456789')

    # 輸出結果
    print out
