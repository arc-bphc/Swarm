import numpy as np
import cv2
import cv2.aruco as aruco
import math
import serial
import paho.mqtt.client as paho
#import time

#reference_time = time.time()

broker = "192.168.225.56"
port = 1883

def on_publish(client, userdata, result):
	print("data published \n")
	pass

client1 = paho.Client("control2")
client1.on_publish=on_publish
client1.connect(broker,port)

#dat= serial.Serial('/dev/cu.SLAB_USBtoUART',9600)
#dat= serial.Serial('/dev/cu.SLAB_USBtoUART',115200)

cap = cv2.VideoCapture(1)
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('output.mp4',fourcc, 20.0, (640,480))

cap.set(3,620)
cap.set(4,480)
height = int (cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


#------------------------------------------------------------------#------------------------------------------------------------------#
# Make all the modifications here to give the id number and coordinates that bot has to reach										

s = 0 

bot_data = np.zeros((20,6)) # contains id number, final x, final y, current x, current y, and theta 

# Made a switch like function here to either add details for a bot or to start the program so feel free to remove this
def switch(s): 

	choice = float(input("1: Add details for a new id \n2: Start the camera \n"))

	if choice == 1:
		new_bot(s)
	elif choice == 2:
		s = 0
	else :
		print("Invalid choice choose again")
		switch(s)

# This is the function where the id number, final x and final y is take from the user (or Swarm algorithm)
def new_bot(c):
	
	bot_data[c][0] = float(input("Enter the id for this bot: ")) # Id no
	bot_data[c][1] = float(input("Enter the final X for this bot: ")) # Final X
	bot_data[c][2] = float(input("Enter the final Y for this bot: ")) # FInal Y
	c = c + 1
	print("\n")
	switch(c)

bot_data = np.zeros((20,6))
switch(s) #passing cause apparently i dunno how to use global variables
print(bot_data) 
#------------------------------------------------------------------#------------------------------------------------------------------#

while(True):
	# Capture frame-by-frame
	ret, frame = cap.read()
	#frame = image
	#print(frame.shape) #480x640
	# Our operations on the frame come here
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_250)
	parameters =  aruco.DetectorParameters_create()
	#cv2.line(frame, (190, 0), (190, height), (0, 0, 0), 2)
	#print(parameters)
 
	'''    detectMarkers(...)
		detectMarkers(image, dictionary[, corners[, ids[, parameters[, rejectedI
		mgPoints]]]]) -> corners, ids, rejectedImgPoints
		'''
		#lists of ids and the corners beloning to each id
	corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
	#print(ids)
	
	if len(corners)!=0:

		for i in range(len(ids)):

			for j in range(4):
				#print(ids[i][0])
				x = corners[i][0][j][0]
				y = corners[i][0][j][1]
				#print(x,y) 
				centroid_x = (int)(abs(corners[i][0][0][0] + corners[i][0][2][0]) / 2.0)
				centroid_y = (int)(abs(corners[i][0][0][1] + corners[i][0][2][1]) / 2.0)
				id_loc = 0
				for k in range(20):
					if bot_data[k][0] == ids[i][0]:
						id_loc = k
						break
					elif bot_data[k][0] == 0:
						bot_data[k][0] = ids[i][0]
						bot_data[k][1] = -1
						id_loc = k
						break

				#bot_data[k][0] = ids[i][0]
				bot_data[id_loc][3] = centroid_x
				bot_data[id_loc][4] = centroid_y
				xfin = bot_data[id_loc][1]
				yfin = bot_data[id_loc][2]

				x1 = (int)(abs(corners[i][0][2][0] + corners[i][0][3][0]) / 2.0)
				y1 = (int)(abs(corners[i][0][2][1] + corners[i][0][3][1]) / 2.0)

				x2 = (int)(abs(corners[i][0][0][0] + corners[i][0][3][0]) / 2.0)
				y2 = (int)(abs(corners[i][0][0][1] + corners[i][0][3][1]) / 2.0)

				den = float(math.sqrt( (x1-centroid_x)*(x1-centroid_x) + (centroid_y-y1)*(centroid_y-y1) ) * math.sqrt( (xfin-centroid_x)*(xfin-centroid_x) + (centroid_y-yfin)*(centroid_y-yfin) ))
				den2 = float(math.sqrt( (x2-centroid_x)*(x2-centroid_x) + (centroid_y-y2)*(centroid_y-y2) ) * math.sqrt( (xfin-centroid_x)*(xfin-centroid_x) + (centroid_y-yfin)*(centroid_y-yfin) ))

				if den != 0:
					costheta = ( (x1-centroid_x)*(xfin-centroid_x) + (centroid_y-y1)*(centroid_y-yfin) )/ den
				else:
					costheta = 1
				if den2 != 0:
					costheta2 = ( (x2-centroid_x)*(xfin-centroid_x) + (centroid_y-y2)*(centroid_y-yfin) )/ den2
				else:
					costheta2 = 1

				if costheta > 1: #temporary fix for runtime errors 
					costheta = 1 
				elif costheta < -1:
					costheta = -1

				if costheta2 > 1:
					costheta2 = 1 
				elif costheta2 < -1:
					costheta2 = -1

				theta = (math.acos(costheta) * 360) / (2 *3.1415) 
				theta2 = (math.acos(costheta2) * 360) / (2 *3.1415) 

				if theta2 < 90:
					theta = -theta
				cv2.putText(frame, "Angle: " + str(theta), (0, 15), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 0), 1)

				bot_data[id_loc][5] = theta

				cv2.line(frame, (centroid_x, centroid_y), (x1, y1), (0, 0, 255), 2)
				cv2.line(frame, (centroid_x, centroid_y), (x2, y2), (0, 255, 0), 2)
				if bot_data[k][1] != -1:
					cv2.line(frame, (centroid_x, centroid_y), (int(xfin), int(yfin)), (255, 255, 0), 2)

				#cv2.drawMarker(frame, (x,y), (0, 255, 0), cv2.MARKER_STAR, markerSize=4, thickness=4, line_type=cv2.LINE_AA)
				#cv2.drawMarker(frame, (centroid_x,centroid_y), (200, 0, 255), cv2.MARKER_STAR, markerSize=4, thickness=4, line_type=cv2.LINE_AA)

	aruco.drawDetectedMarkers(frame, corners, ids)

	#print(rejectedImgPoints)
	# Display the resulting frame
	#cv2.imshow('frame',gray)
	
	cv2.imshow('frame1',frame)
	#client1 = paho.Client("control2")
	
	#------------------------------------------------------------------#------------------------------------------------------------------#

	# The part where I publish the data for each row (bot) registered by the user (Swarm algo) 

	for i in range(20):
		if bot_data[i][1] != -1 and bot_data[i][0] != 0 and bot_data[i][3] != 0: # checks to remove the data of bots that were registered but not present and unwanted arucos that were detected 
			ret=client1.publish("inTopic","Sent") # use this as a check for each bot to see if data is being lost
			ret=client1.publish("inTopic",bot_data[i][0]) # Id number
			ret=client1.publish("inTopic",bot_data[i][1]) # Final X
			ret=client1.publish("inTopic",bot_data[i][2]) # Final Y
			ret=client1.publish("inTopic",bot_data[i][3]) # Centroid X
			ret=client1.publish("inTopic",bot_data[i][4]) # Centroid Y
			ret=client1.publish("inTopic",bot_data[i][5]) # theta in degrees
	#------------------------------------------------------------------#------------------------------------------------------------------#
	#print(bot_data)

	for i in range(20):
		#if bot_data[i][0] != 0:
		#	ret=client1.publish("inTopic",bot_data[i][0])
		if bot_data[i][1] == -1:
			bot_data[i] = 0
		else:
			bot_data[i][3] = 0

	#out.write(frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
 
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()