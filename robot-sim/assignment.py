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
    
def find_nearest_token():
    dist = 100
    global tokens
    global grabbed_token
    while 1:
    	for token in R.see(): # for all tokens that the robot is seeing
    	  grabbato = False
    	  for t in grabbed_token:
    	    if t.info.code == token.info.code: #check if the tokens was already grabbed
    	      grabbato = True
    	      break
    	  if grabbato == True:
    	        pass #if the token was already grabbed pass to the next token
    	  else:
    		trovato = False

    		if token.dist < dist: #find the nearest token
    			dist = token.dist
    			tokenf = token
    		if tokens == []:#if the list tokens is empty
    			tokens.append(token) #add the first token
    			
    		#if the token is equal to the first one, you completed a turn 
    		elif token.info.code == tokens[0].info.code:

    			for toke in tokens:
    				if toke.info.code == tokenf.info.code:
    					tokens.remove(toke)
    					tokens.insert(0,toke) #move the nearest token in the first position
    			return tokenf #return the nearest token
    		
    		else:
    			for tokenz in tokens:
    				if tokenz.info.code == token.info.code: #check if the token was already in the list
    					trovato = True
    					break
    			if trovato == True:
    				pass
    		        else:
    				tokens.append(token) #add the token to the list		
				
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
        	grabbed_token.append(token) #add the grabbe dtoken to the grabbed_token list
        	print("Gotcha!")
		if i == 1:
			end = len(tokens)
    		tokens = [] #empty the list
    		
    		d = 100
        	while d > d_th:
        	      if len(grabbed_token) == 1: #the first time
        		print("len 1")
        		tokenn = find_nearest_token() #find the nearest token
        	      else:                       #the other time
        	      	print("len magg 1")
        	      	#print(grabbed_token[1])
        	      	tokenn = token_target()   #find the token target
        	      d = tokenn.dist - d_th	  #compute the distance from the target
        	      rot_yn = tokenn.rot_y 	  #compute the angle
		      take_to_target(d, rot_yn)  #take the token to the target

		if len(grabbed_token) == 1:
			grabbed_token.append(tokenn) #add the token in the target position to the grabbe_token list

    		tokens=[] 			
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

def take_to_target(dist, rot_y):
         if dist < d_th: 
        	print("releasing")
        	release = R.release() # if we are close to the token, we grab it.
        	drive(-15,2.5)
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
		

while len(grabbed_token) < end:

	token = find_nearest_token()
	
	grabbed = reach_and_grab(token)
	
	print("len grabed token:")
	print(len(grabbed_token))	

	
	
