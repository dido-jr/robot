Python Robotics Simulator
================================

This is a simple, portable robot simulator developed by [Student Robotics](https://studentrobotics.org).
Some of the arenas and the exercises have been modified for the Research Track I course

Installing and running
----------------------

The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

Once the dependencies are installed, simply run the `test.py` script to test out the simulator.

To run my code:
go into the rigth folder then run
```bash
$ python2 run.py assignment.py
```

Robot API
---------

The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].

### Motors ###

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

### The Grabber ###

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.

### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

For example, the following code lists all of the markers the robot can see:

```python
markers = R.see()
print "I can see", len(markers), "markers:"

for m in markers:
    if m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER):
        print " - Token {0} is {1} metres away".format( m.info.offset, m.dist )
    elif m.info.marker_type == MARKER_ARENA:
        print " - Arena marker {0} is {1} metres away".format( m.info.offset, m.dist )
```

[sr-api]: https://studentrobotics.org/docs/programming/sr/

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
			
			Elif token.info.code is equal to tokens[0].info.code:
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

The function `token_target called` in the reach_and grab function return the token that is in the collection point

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


