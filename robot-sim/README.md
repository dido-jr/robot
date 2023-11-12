Assignment 1 Research Track
================================

### Objective ###
Write a python node that controls the robot to put all the golden boxes togheter

### Possible solutions ###
In order to put all the boxes togheter I decide to:
* find, reach and grab the nearest token
* take this token to nearest one and release it there (this will be the collection point)
* find, reach an grab the nearest token (ignoring the token already in the collection point)
* take this token to the collection point
* come back to the third point

Another possible solution would have been to bring all the tokens to the center, with the assumption that the tokens are in circle, to minimize the distances, but the code would have lost generality.

### Implementation ###
Before all I declared the following global variables:
```
grabbed_token = [] #this list will contain the token grabbed
tokens = [] #this list will contain the token seen, not already grabbed
i = 0 #this variable will count the number of iterations
end = 1 #this variable will contain the number of  tokens 
a_th = 2.0 #is the threshold for the control of the orientation
d_th = 0.4 #is the threshold for the control of the linear distance
```

I decided to save in a list the tokens seen by the robot, while it turns around, until it sees the first token inserted in the list again, at which point all the tokens will have been seen and we will know which one is the closest one. Once this latter has been identify, the robot will have to reach it directly without stopping to calculate the nearest token. For this reason it is necessary to move the nearest token to the first place in the list. In the subsequent iterations it will also be necessary to check that the closest token has not already been grabbed.
These steps are implemented in the function called `find_nearest_token`

```plaintext
set dist to 100

While true:
	For each token in R.see():
		Set grabbato to false
		if token is in grabbed_token
			Set grabbato to true
			exit loop
		If grabbato:
			continue
		Else:
			Set trovato to false
			
			If token.dist is less than dist
				Set dist to token.dist
				Set nearest_token to token
			
			If tokens is empty:
				Append token to tokens
			
			Elif token is equal to first token in tokens
				Remove token from tokens
				Insert token at index 0 in tokens
				return nearest_token
				
			Else:
				if token is already in tokens
					Set trovato = true
				If trovato:
					Continue
				Else:
					Append token to tokens
					
		Turn(10,1)
```

Once the previous function returned the nearest token, the robot have to reach and grab it. For this reason I create the function `reach_and_grab` that take as parameter the token that must be reached. Once the token has been reached it must be taken to the collection point


```plaintext
set grabbed to false
set dist to token.dist
set rot_y to token.rot_y

If dist less then threshold:
	#grab the token
	print("Found it")
	set grabbed = R.grab()
	set i to i+1
	append token to grabbed_token
	print("Gotcha")
	
	if i equal to 1: 	       #at the first iteration the list contain all the tokens
		set end to len(tokens) #so end is equal the number of all tokens in the arena
	
	set tokens to empty list #because we will need to re-compute the nearest token
	
	#take the grabbed token to the collection point
	set d to 100
	while d greater then threshold:
		if grabbed_token contains 1 element: 
			tokenn = find_nearest_token() #fisrt time find the nearest token
		else:
			set tokenn to token_target() #other times find the collection point
		set d to tokenn.dist - threshold
		set rot_yn to tokenn.rot_y
		take_to_target(d, rot_y)
	
	if grabbed_token contains 1 element:
		append tokenn to grabbed_token #the token in the collection point must not be grabbed
		
	set tokens to empty list
	return grabbed

#drive the robot towards the nearest token	
elif -a_th <= rot_y <= a_th:
	print("Ah, here we are!")
	drive(10, 0.5)
	
elif rot_y less then -a_th:
	print("left a bit...)
	turn(-2, 0.5)
	
elif rot_y greater then a_th:
	print("Right a bit...")
	turn(+10, 0.3)

```

The function `token_target` called in the reach_and grab function return the token that is in the collection point

```plaintext
while 1:
	for each token in R.see()
		if token is equal to grabbed_token[1]:
			return token
		else: continue
	turn(10, 0.5)

```

While the function `take_to_target` take as parameter a distance and an angle, then take the robot to that position and release there the token that it was grabbing:
```plaintext
if dist less then threshold
	release the token
	move back
	
elif rot_y<= rot_y <= a_th #the robot is aligned with the target
	drive(10,0.5)

elif rot_y < -a_th: # if the robot is not well aligned with the token
         print("Left a bit...")
         turn(-2, 0.5)
 elif rot_y > a_th:
         print("Right a bit...")
         turn(+2, 0.5)
```

The `main function` call the find_nearest_token function and pass the token returned by it to the reach_and_grab function until the lenght of the grabbed_token list will be same of the list tokens at the first iteration, when it contains all the tokens.

```plaintext
while len(grabbed_token) < end :
	
	token = find_nearest_token()
	
	grabbed = reach_and_grab(token)
```

###Possible improvements###

The robot could turn less to find the nearest token by controlling the size of the list tokens. In fact, knowing the number of total tokens and the number of tokens taken, we can make the robot stop turning when the size of the list tokens, added to the size of the grabbed_token list, is equal to the number of total tokens


