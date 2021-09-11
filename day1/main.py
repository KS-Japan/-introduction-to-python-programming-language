## -*- coding: utf-8 -*-
import cv2
import random

def main():
	img = cv2.imread('tab.png')
	gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
	cv2.imwrite('gray.png',gray)
	edge = cv2.Canny(gray, 1, 100,apertureSize=7)
	cv2.imwrite('edge.png',edge)

	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (6,6))
	edge2 = cv2.dilate(edge,kernel)
	cv2.imwrite('edge2.png',edge2)
	contours, hierarchy = cv2.findContours(edge2, cv2.RETR_TREE,
		cv2.CHAIN_APPROX_SIMPLE)

	curves = []
	for contour, hierarchy in zip(contours, hierarchy[0]):
		curve = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour, True), True)
		if len(curve) == 4:
			curves.append(curve)
	curves = sorted(curves, key=lambda x:(x.ravel()[1], x.ravel()[0]))
	#print(curves)

	rect_img = img.copy()
	for i, curve in enumerate(curves):
		p1, p3 = curve[0][0], curve[2][0]
		x1, y1, x2, y2 = p1[0], p1[1], p3[0], p3[1]
		r, g, b = random.random()*255, random.random()*255, random.random()*255
		cv2.rectangle(rect_img, (x1, y1), (x2,y2),(r,g,b),thickness=2)
	cv2.imwrite('rect.png',rect_img)

if __name__ == "__main__":
	main()