import datetime
from random import randint
import math

from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF, QObject
#elif PYQT_VER == 'PYQT4':
#	from PyQt4.QtCore import QLineF, QPointF, QObject
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

import time

# Some global color constants that might be useful
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

# Global variable that controls the speed of the recursion automation, in seconds
#
PAUSE = 0.25

#
# This is the class you have to complete.
#


class ConvexHullSolver(QObject):

	# Using Master theorem T(n) = 2T(n/2) + O(1)
	# a/b^d = 2/2^1 = 1 which means that O(n^dlogn) = O(nlogn)
	def DivideAndConquer(self, list):
		half = int(len(list) / 2)
		List1 = list[0:half]
		List2 = list[half: len(list)]
		if len(list) < 4 and len(list) > 0:
			if len(list) == 1:
				return list
			else:
				return self.ConvexMerger(List1, List2)
		else:
			return self.ConvexMerger(self.DivideAndConquer(List1), self.DivideAndConquer(List2))

	# this function includes 4 O(n) sections(loops) which means the function is O(n).
	def ConvexMerger(self, list1, list2):
		LIST1_SIZE = int(len(list1))
		LIST2_SIZE = int(len(list2))
		LPlace = 0
		RPlace = 0
		Lindex = 0
		Rindex = 0
		Rx = math.inf
		Lx = -math.inf

		# this is O(n)
		#List 1 find Left lists most right point
		for i in range(int(LIST1_SIZE)):
			if(list1[i].x() >= Lx):
				Lx = list1[i].x()
				LPlace = list1[i]
				Lindex = i

		#this is O(n)
		#List 2 find Right's most left point
		for i in range(int(LIST2_SIZE)):
			if (list2[i].x() <= Rx):
				RPlace = list2[i]
				Rx = list2[i].x()
				Rindex = i

		#edge case for two points
		if LIST1_SIZE == 1 and LIST2_SIZE == 1:
			return list1 + list2


		oldSlope = 0
		newSlope = self.SlopeCalculator(LPlace, RPlace)
		TLindex = Lindex #top left index
		TRindex = Rindex #top right index
		TLPlace = LPlace #top left point
		TRPlace = RPlace #top right point

		# this is O(n)
		#while loop to find the top connecting points for the convex hull
		while oldSlope != newSlope:
			oldSlope = newSlope

			#this process pivots around the Right point and finds the next counter clockwise
			#Left point and finds the slope to check with current/new slope
			changeIndex = (TLindex - 1) % LIST1_SIZE
			changeL = list1[changeIndex]
			RSlope = self.SlopeCalculator(changeL, TRPlace)

			#this if checks the previously found slope and changes it if the Right Slope is less then the current slope
			if(RSlope <= newSlope):
				newSlope = RSlope
				TLindex = (TLindex - 1) % LIST1_SIZE
				TLPlace = list1[TLindex]

			# this process pivots around the Left point and finds the next clockwise
			# Right point and finds the slope to check with current/new slope
			changeIndex = (TRindex + 1) % LIST2_SIZE
			changeR = list2[changeIndex]
			LSlope = self.SlopeCalculator(TLPlace, changeR)

			# this if checks the previously found slope and changes it if the Left Slope is greater then the current slope
			if LSlope >= newSlope:
				newSlope = LSlope
				TRindex = (TRindex + 1) % LIST2_SIZE
				TRPlace = list2[TRindex]


		oldSlope = 0
		newSlope = self.SlopeCalculator(LPlace, RPlace)
		BLindex = Lindex  # bottom left index
		BRindex = Rindex  # bottom right index
		BLPlace = LPlace  # bottom left point
		BRPlace = RPlace  # bottom right point

		# this is O(n)
		# while loop to find the bottom connecting points for the convex hull
		while oldSlope != newSlope:
			oldSlope = newSlope

			# this process pivots around the Right point and finds the next counter clockwise
			# Left point and finds the slope to check with current/new slope
			changeIndex = (BLindex + 1) % LIST1_SIZE
			changeL = list1[changeIndex]
			RSlope = self.SlopeCalculator(changeL, BRPlace)

			# this if checks the previously found slope and changes it if the Right Slope is greater then the current slope
			if RSlope > newSlope:
				newSlope = RSlope
				BLindex = changeIndex
				BLPlace = list1[BLindex]

			# this process pivots around the Left point and finds the next clockwise
			# Right point and finds the slope to check with current/new slope
			changeIndex = (BRindex - 1) % LIST2_SIZE
			changeR = list2[changeIndex]
			LSlope = self.SlopeCalculator(BLPlace, changeR)

			# this if checks the previously found slope and changes it if the Left Slope is less then the current slope
			if LSlope < newSlope:
				newSlope = LSlope
				BRindex = changeIndex
				BRPlace = list2[BRindex]

		#print("list1: " + str(list1) + "\nlist2: " + str(TRindex) + " BRIndex: " + str(BRindex))
		#This section creates a combined list from the two shapes making the convex Hull of them
		tempList = list1[:TLindex+1]
		if BRindex > TRindex: tempList = tempList + list2[TRindex:BRindex+1]
		if BRindex < TRindex: tempList = tempList + list2[TRindex:] + list2[:BRindex+1]
		if TLindex < BLindex: tempList = tempList + list1[BLindex:]
		FinalList = []
		[FinalList.append(p) for p in tempList if p not in FinalList]
		return FinalList


	def SlopeCalculator(self, LPlace, RPlace):
		#this calculates the slope from two given points
		if LPlace.y() != RPlace.y() or LPlace.x() != RPlace.x():
			slope = float((RPlace.y() - LPlace.y()) / (RPlace.x() - LPlace.x()))
		return slope

# Class constructor
	def __init__( self):
		super().__init__()
		self.pause = False
		
# Some helper methods that make calls to the GUI, allowing us to send updates
# to be displayed.

	def showTangent(self, line, color):
		self.view.addLines(line,color)
		if self.pause:
			time.sleep(PAUSE)

	def eraseTangent(self, line):
		self.view.clearLines(line)

	def blinkTangent(self,line,color):
		self.showTangent(line,color)
		self.eraseTangent(line)

	def showHull(self, polygon, color):
		self.view.addLines(polygon,color)
		if self.pause:
			time.sleep(PAUSE)
		
	def eraseHull(self,polygon):
		self.view.clearLines(polygon)
		
	def showText(self,text):
		self.view.displayStatusText(text)
	

# This is the method that gets called by the GUI and actually executes
# the finding of the hull
	def compute_hull( self, points, pause, view):
		self.pause = pause
		self.view = view
		assert( type(points) == list and type(points[0]) == QPointF )

		t1 = time.time()
		#according to python this is O(nlogn)
		sortedPoints = sorted(points, key=lambda k: k.x())
		#sortedPoints = self.QuickSort(points)
		t2 = time.time()

		t3 = time.time()
		# this is a dummy polygon of the first 3 unsorted points
		hull = self.DivideAndConquer(sortedPoints)
		polygon = [QLineF(hull[i], hull[(i+1) % len(hull)]) for i in range(len(hull))]
		t4 = time.time()
		print("T1: "+ str(t1) + " T2: " + str(t2) + " T3: "+ str(t3) + " T4: " + str(t4))
		print("TOTAL time: " + str((t4-t1)))
		# when passing lines to the display, pass a list of QLineF objects.  Each QLineF
		# object can be created with two QPointF objects corresponding to the endpoints
		self.showHull(polygon,RED)
		self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))

	#NO LONGER USING THIS PIECE OF CODE, USING PYTHONS IN CODE SORT
	def QuickSort(self, points):
		LIST_SIZE = len(points)
		ChangePoints = points
		pivot = int(LIST_SIZE / 2)


		while(True):
			LPointer = points[0]
			RPointer = points[LIST_SIZE-1]
			LPlace = 0
			RPlace = int(LIST_SIZE-1)

			while(LPointer.x() < points[pivot].x()) and LPlace < pivot:
				LPlace += 1
				LPointer = points[LPlace]

			while(RPointer.x() > points[pivot].x()) and RPlace > pivot:
				RPlace -= 1
				RPointer = points[RPlace]

			if LPlace == pivot and RPlace == pivot:
				break

			points[LPlace] = RPointer
			points[RPlace] = LPointer

		if(int(LIST_SIZE) >= 3):
			points1 = self.QuickSort(points[:int(LIST_SIZE / 2)])
			points2 = self.QuickSort(points[int(LIST_SIZE / 2):])
			return points1 + points2

		if(int(LIST_SIZE) < 3):
			return points



