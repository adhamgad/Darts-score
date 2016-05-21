import math
import numpy as np 
import cv2

#this is a list of all the radii in the image
radii = [14,33,80,127,174,220,267,314,361]

def calculate_distance(x0,y0,x1,y1):
	"""Takes two points as input and returns the distance between them"""

	return math.sqrt( (x1-x0)**2 + (y1-y0)**2 )

def calculate_score(dist):
	"""Calculates the score of each point based on it's distance from the center 
	by calculating in which circle it is enclosed in based on circles radii"""

	for i in range(len(radii)):
		if dist < radii[i]:
			return 9-i 

img = cv2.imread("input.jpg")
output = img.copy()

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #Gray scale version of the image
cv2.imwrite("Grayscale of Original image.jpg", gray)
gray = cv2.blur(gray,(9,9)) #Blurring the image before any operation to reduce noise and decrease the number of false positives
cv2.imwrite("Blurred Grayscale of Original image.jpg", gray)

#Extract bullets from the image by using hough transform
target_circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT, 1, 10 ,param1=45,param2=17 ,minRadius=10, maxRadius= 15 )
target_circles = np.round(target_circles[0, :]).astype("int") 

score = 0 # This value will be printed when finished

for (x, y, r) in target_circles:
	#Loop in all bullet points and calculate each bullet point distance from the center then it's score
	cv2.circle(output, (x, y), r, (0, 255, 0), 4)
	dist = calculate_distance(238, 246, x, y)
	score += calculate_score(dist)

print(score-9) # subtract from the score the false positive value of the smallest circle r9 which is about the same size of the other bullet points

cv2.imwrite("Output.jpg", output)

