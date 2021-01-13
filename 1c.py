import collections
import re
import math
 
class coord:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        
    def __eq__(self, other):
        return (abs(self.x - other.x) <= 0.00001) and (abs(self.y - other.y) <= 0.00001)
    
    def length(self, other):
        return round((((self.x - other.x)**2 + (self.y - other.y)**2)**0.5), 6)
 
class polygon:
    def __init__(self):
        self.center = coord(0.0, 0.0)
        self.c = []
        self.Radius = 0
        self.Area = 0
    
    def addCoord(self, coord):
        self.c.append(coord)
        if len(self.c) == 1:
            pt1 = coord
        elif len(self.c) == 2:
            pt2 = coord
        elif len(self.c) == 3:
            pt3 = coord
            self.Radius =-1		# error checking 
            
            if (not self.IsPerpendicular(1, 2, 3)):				
                self.CalcCircle(1, 2, 3)
            elif (not self.IsPerpendicular(1, 3, 2)):
                self.CalcCircle(1, 3, 2)
            elif (not self.IsPerpendicular(2, 1, 3) ):
                self.CalcCircle(2, 1, 3)
            elif (not self.IsPerpendicular(2, 3, 1) ):
                self.CalcCircle(2, 3, 1)
            elif (not self.IsPerpendicular(3, 2, 1) ):
                self.CalcCircle(3, 2, 1)
            elif (not self.IsPerpendicular(3, 1, 2) ):
                self.CalcCircle(3, 1, 2)
            else: 
        #       The three pts are perpendicular to axis
        #		pt1->trace();			pt2->trace();			pt3->trace();
                self.Radius =-1
    
    def IsPerpendicular(self, n1, n2, n3):
    # Check the given point are perpendicular to x or y axis 
        pt1 = self.c[n1-1]
        pt2 = self.c[n2-1]
        pt3 = self.c[n3-1]
        yDelta_a = pt2.y - pt1.y
        xDelta_a = pt2.x - pt1.x
        yDelta_b = pt3.y - pt2.y
        xDelta_b = pt3.x - pt2.x
    # checking whether the line of the two pts are vertical
        if (abs(xDelta_a) == 0 and abs(yDelta_b) == 0):
            return False
        if (abs(yDelta_a) == 0):
            return True
        elif (abs(yDelta_b) == 0):
            return True
        elif (abs(xDelta_a) == 0):
            return True
        elif (abs(xDelta_b) == 0):
            return True
        else:
            return False
    
    def CalcCircle(self, n1, n2, n3):
        if len(self.c) >= 3:
            
            pt1 = self.c[n1-1]
            pt2 = self.c[n2-1]
            pt3 = self.c[n3-1]
            
            yDelta_a= pt2.y - pt1.y
            xDelta_a= pt2.x - pt1.x
            yDelta_b= pt3.y - pt2.y
            xDelta_b= pt3.x - pt2.x
            
            if (abs(xDelta_a) == 0 and abs(yDelta_b) == 0):
                self.center = coord(0.5*(pt2.x + pt3.x), 0.5*(pt1.y + pt2.y))
                self.Radius = self.center.length(pt1)		# calc. radius
                return self.Radius
            aSlope=yDelta_a/xDelta_a 
            bSlope=yDelta_b/xDelta_b
            if (abs(aSlope-bSlope) == 0):	# checking whether the given points are colinear. 	
                return -1
 
            self.center.x= (aSlope*bSlope*(pt1.y - pt3.y) + bSlope*(pt1.x + pt2.x)
                - aSlope*(pt2.x+pt3.x) )/(2* (bSlope-aSlope) )
            self.center.y = -1*(self.center.x - (pt1.x+pt2.x)/2)/aSlope +  (pt1.y+pt2.y)/2
            
            self.Radius = self.center.length(pt1)		# calc. radius
            return self.Radius
    
    def coord_range(self, bordCount):
        #point = coord()
        for bordNumber in range(1, bordCount+1, 1):
            sin0 = (self.c[0].y - self.center.y)/self.Radius;
            cos0 = (self.c[0].x - self.center.x)/self.Radius;
            x = self.center.x + (cos0*math.cos(math.pi*2*(bordNumber-1)/bordCount)-sin0*math.sin(math.pi*2*(bordNumber-1)/bordCount))*self.Radius#- self.Radius + self.c[0].x
            y = self.center.y + (sin0*math.cos(math.pi*2*(bordNumber-1)/bordCount)+cos0*math.sin(math.pi*2*(bordNumber-1)/bordCount))*self.Radius#+ self.c[0].y
            point = coord(x, y)
            #print ('coord ', bordNumber, ' angle ', 360*(bordNumber-1)/bordCount, 'calc coords: ', 'x ', x, ' y', y)
            yield point
    
    def calcCent(self):
        if len(self.c) >= 3:
            
            for bordNumber in range(3, 101, 1):
                nRes = 0
                for coordFullIndex in self.coord_range(bordNumber):
                    for coordIndex in self.c:
                        #print ('real coords: ', 'x ', coordIndex.x, 'y ', coordIndex.y) 
                        if coordIndex == coordFullIndex:
                            nRes = nRes + 1
                #print ('possible area: ', (self.Radius**2*bordNumber/2)*math.sin(math.pi*2/bordNumber))
                if nRes >= 3:
                    self.Area = (self.Radius**2*bordNumber/2)*math.sin(math.pi*2/bordNumber)
                    break
    
coordinates = []
 
sstorage_path = 'params'
plg = polygon()
#with open(sstorage_path) as f:
for line in range(1,4,1):
    line = input()
    match = re.findall(r'(\S+)', line)
    rate1 = float(match[0])
    rate2 = float(match[1])
    coordinates.append(coord(match[0], match[1]))
    plg.addCoord(coord(match[0], match[1]))
 
plg.calcCent()              
#print(plg.center.x, ' ', plg.center.y, ' ', plg.Radius, ' ', plg.Area)
print(plg.Area)
#for coord in coordinates:
    #print(coord.x, ' ', coord.y)
 
#f.close()