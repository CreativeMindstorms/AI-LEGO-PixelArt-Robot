import cv2
from time import sleep

def moveXmotor(Xmotor, location, safeDistance, brakee=True, keepDistance=False):
  Xmotor.start_move_to(location+safeDistance, speed=100, brake=brakee)
  while Xmotor.busy: pass
  if not keepDistance:
    Xmotor.start_move_to(location, speed=5, brake=brakee)
    while Xmotor.busy: pass

def moveYmotor(Ymotor, location, Ydistance, useYdistance=False, brakee=True):
  if useYdistance:
    Ymotor.start_move_to(location+Ydistance, speed=100, brake=brakee)
    while Ymotor.busy: pass
    Ymotor.start_move_to(location, speed=5, brake=brakee)
    while Ymotor.busy: pass
  else:
    Ymotor.start_move_to(location, speed=100, brake=brakee)
    while Ymotor.busy: pass

def pickPixel(Zmotor, Zbottom, Ztop, Zdistance, brakee = True):
  retry = True
  while retry:
    retry = False
    Zmotor.start_move_to(Zdistance, speed=75, brake=brakee)
    while Zmotor.busy: pass
    Zmotor.start_move_to(Zbottom, speed=25, brake=brakee)
    while Zmotor.busy:
      if cv2.waitKey(1) == ord('s'):
        retry = True
        Zmotor.start_move_to(Ztop, speed=100, brake=brakee)
        while cv2.waitKey(1) != ord('c'): pass
    sleep(0.5)
    Zmotor.start_move_to(Ztop, speed=100, brake=brakee)
    while Zmotor.busy: pass

def placePixel(Zmotor, Xmotor, Ymotor, Zbottom, Ztop, Zdistance, Xposition, Yposition, safeDistance, brakee = True):
  if Yposition < 0: Ymotor.start_move_to(Yposition-safeDistance, speed=20, brake=brakee)
  while Ymotor.busy: pass
  Zmotor.start_move_to(Zdistance, speed=50, brake=brakee)
  while Zmotor.busy: pass
  Xmotor.start_move_to(Xposition, speed=5, brake=brakee)
  if Yposition < 0: Ymotor.start_move_to(Yposition, speed=10, brake=brakee)
  while Xmotor.busy: pass
  while Ymotor.busy: pass
  Zmotor.start_move_to(Zbottom, speed=25, brake=brakee)
  while Zmotor.busy: pass
  sleep(0.5)
  Zmotor.start_move_to(Ztop, speed=100, brake=brakee)
  while Zmotor.busy: pass

def resetZAxis(Zmotor):
  Zmotor.start_move(speed=10)
  sleep(3)
  Zmotor.position = 0
  Zmotor.start_move_to(position=-90, speed=25, brake=True)
  while Zmotor.busy: pass
  Zmotor.position = 0

def resetXAxis(Xmotor, XTouch, Xstart, Xdistance):
  if not XTouch.touched:
    Xmotor.start_move(speed=75)
    while not XTouch.touched: pass
    Xmotor.stop()
  Xmotor.start_move_by(-175, speed=25, brake=True)
  while Xmotor.busy: pass
  Xmotor.start_move(speed=5)
  while not XTouch.touched: pass
  Xmotor.stop(brake=True)
  sleep(0.25)
  Xmotor.position = 0
  moveXmotor(Xmotor, Xstart, Xdistance)
  sleep(0.25)
  Xmotor.position = 0

def resetYAxis(Ymotor, YTouch, Ystart, Ydistance):
  if not YTouch.touched:
    Ymotor.start_move(speed=100)
    while not YTouch.touched: pass
    Ymotor.stop(brake=True)
  Ymotor.start_move_by(-250, speed=100, brake=True)
  while Ymotor.busy: pass
  Ymotor.start_move(speed=10)
  while not YTouch.touched: pass
  Ymotor.stop(brake=True)
  sleep(0.25)
  Ymotor.position = 0
  moveYmotor(Ymotor, Ystart, -Ydistance, useYdistance=True)
  sleep(0.25)
  Ymotor.position = 0