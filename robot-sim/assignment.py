from __future__ import print_function

import time
from sr.robot import *

a_th = 2.0
""" float: Threshold for the control of the linear distance"""

d_th = 0.4
""" float: Threshold for the control of the orientation"""

grabbed_token = []
tokens = []
i = 0
end = 10


R = Robot()
""" instance of the class Robot"""


def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
    
def find_all_token():
    dist = 100
    global tokens
    global grabbed_token
    while 1:
    	for token in R.see():
    	  print(token.info.code)
    	  grabbato = False
    	  for t in grabbed_token:
    	    print("grabbe")
    	    if t.info.code == token.info.code:
    	      grabbato = True
    	      break
    	  if grabbato == True:
    	  	print("pass")
    	        pass
    	  else:
    		trovato = False

    		if token.dist < dist:
    			dist = token.dist
    			tokenf = token
    		if tokens == []:#se la lista tokens e' vuota  not tokens
    			tokens.append(token) #aggiungi il primo token visto
    			print("primo")
    			
    		#se il token trovato e' uguale al primo hai completato il giro 
    		elif token.info.code == tokens[0].info.code and len(tokens) > 1: 
    			print("escii")

    			for toke in tokens:
    				if toke.info.code == tokenf.info.code:
    					tokens.remove(toke)
    					tokens.insert(0,toke)
    			print("piu vicino:")
    			print(tokenf.info.code)
    			return tokenf #ritorna il token piu' vicino
    		
    		else:
    			for tokenz in tokens:
    				if tokenz.info.code == token.info.code:
    					trovato = True
    					break
    			if trovato == True:
    				pass
    		        else:	
    				print("ciao")
    				tokens.append(token)   		
				
    	turn(10,1)

  
def reach_and_grab(token):
    	 grabbed = False
    	 global tokens
    	 global grabbed_token
    	 global end
    	 global i 
         dist = token.dist
         rot_y = token.rot_y
         if dist==-1:
         	print("I don't see any token!!")
         	exit()  # if no markers are detected, the program ends
         elif dist < d_th: 
        	print("Found it!")
        	grabbed = R.grab() # if we are close to the token, we grab it.
        	grabbed = True
        	i = i+1
        	grabbed_token.append(token)
        	print("Gotcha!")
		if i == 1:
			print("sonoo QUIIII")
			print(len(tokens))
			end = len(tokens)
    		tokens = []
    		d = 100

        	while d > d_th:
        	      if len(grabbed_token) == 1:
        		print("len 1")
        		tokenn = find_all_token()
        	      else:
        	      	print("len magg 1")
        	      	#print(grabbed_token[1])
        	      	tokenn = token_target()
        	      d = tokenn.dist - d_th
        	      rot_yn = tokenn.rot_y 
		      take_to_center(d, rot_yn)
		#if i >= 1:
		grabbed_token.append(tokenn)

    		tokens=[]		
    		for to in tokens:
    			print(to.info.code)	
        	return grabbed 

         elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
         	print("Ah, here we are!.")
         	drive(10, 0.5)
         elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
         	print("Left a bit...")
         	turn(-2, 0.5)
         elif rot_y > a_th:
         	print("Right a bit...")
         	turn(+10, 0.3)  

def take_to_center(dist, rot_y):
         if dist < d_th: 
        	print("releasing")
        	release = R.release() # if we are close to the token, we grab it.
        	drive(-10,2)
        	#exit()
         elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
         	print("Ah, here we are!.")
         	drive(10, 0.5)
         elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
         	print("Left a bit...")
         	turn(-2, 0.5)
         elif rot_y > a_th:
         	print("Right a bit... center")
         	turn(+2, 0.5)


def token_target():
	while 1:
		for token in R.see():
			if token.info.code == grabbed_token[1].info.code:
				return token
			else: pass
		turn(10,0.5)
		

while 1: #len(grabbed_token) < end

	token = find_all_token()
	
	grabbed = reach_and_grab(token)
	
		

	
	
