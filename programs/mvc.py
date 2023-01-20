from libtbx.program_template import ProgramTemplate
from wxGUI2 import Preferences, utils
import wxGUI2
import wx
import math
import wx 
from iotbx.cli_parser import run_program
import sys
import random
import BFactor
import ligand
import molecular_gaps

#-------------------------------------------------------------------------------------------------------------------
#tools
#throws errors when someone wants to
class MyError:
	def __init__(self, message):
		self.message = message

#converts from linear coordinates to polar coordinates
def linToPol(x,y):
	if(y == 0):
        #returns an error if we divide by zero
		e = MyError("y cannot be 0")
		print(e.message)
		return e
	point =  wx.Point(math.sqrt((x*x), (y*y)), math.atan(x/y))
	return point

#converts from polar to linear coordinates
def polToLin(r,theta):
	point = wx.Point(r*math.cos(theta), r*math.sin(theta))
	return point

#converts from degrees to radians
def toRad(degree):
    return degree*math.pi/180

#switches between colors based on a property
def rainbow(prop):
    r = 0
    g = 0
    b = 0
    if(prop>=0 and prop<=.4):
        x = (prop)/(.4)
        r = 255*(x)
        g = 255
        print('a')
    elif(prop>=.4 and prop<=1):
        x = (prop-.4)/(.6)
        r = 255
        g = 255*(x)
        print('b')
    print(prop)
    print([r,g,b])
    return [r,g,b]

#different color option
# def rainbow(prop):
#     r = 0
#     g = 0
#     b = 0
#     if(prop >= 0 and prop <=.25):
#         r = 0
#         g = 255*(prop)
#         b = 255
#         print('a')
#     elif(prop >= .25 and prop <=.5):
#         r = 0
#         g = 255
#         b = 255*(prop)
#         print('b')
#     elif(prop >= .5 and prop <=.75):
#         r = 255*(prop)
#         g = 255
#         b = 0
#         print('c')
#     elif(prop >= .75 and prop <=1):
#         r = 255
#         g = 255*(prop)
#         b = 0
#         print('d')
#     print(prop)
#     print([r,g,b])
#     return [r,g,b]

#different color option 
# def rainbow(prop):
#     if(prop > 1 or prop < 0):
#         return [0,0,0]
#     r = 255*prop
#     b = 255*(1-prop)
#     return [r,0,b]

#---------------------------------------------------------------------------------------------------------------------
#window stuff
class Mywin(wx.Frame): 
    #constructor       
    def __init__(self, parent, title): 
    	super(Mywin, self).__init__(parent, title = title,size = (1024, 618))  
    	self.InitUI() 
          
    #sets everything up 
    def InitUI(self): 
        #sets some fields up to be used later
        self.bFactorButton = False
        self.prop = 0
        self.numRects = 0
        self.rectColors = []
        self.bg_color = [240,240,240]
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        #makes the run button
        ID_NO = wx.NewId()
        button = wx.Button(self, ID_NO, 'run', pos=(20,40))
        button.Bind(wx.EVT_BUTTON, self.OnClicked, id=ID_NO)
        self.sizer.Add(button, 1, wx.ALL|wx.EXPAND, 0)

        #makes the switch button
        ID_SWITCH = wx.NewId()
        self.newBut = wx.Button(self, ID_SWITCH, 'switch', pos = (100, 40))
        self.newBut.Bind(wx.EVT_BUTTON, self.switchButton, id=ID_SWITCH)
        self.sizer.Add(self.newBut, 1, wx.ALL|wx.EXPAND, 0)

        #finishes the set up
        self.panel.SetSizer(self.sizer)
        self.Centre()
        self.Show(True)
        self.Bind(wx.EVT_PAINT, self.OnPaint) 

    #returns the list of colors for the bfactor set
    def getColorsBFactor(self):
        #makes an empty list
        returnList = []
        #loops over the dictionary
        for key, item in self.bFactorData.items():
            for k2, i2 in item.items():
                #if it is the average residue bfactor
                if(k2 == "res"):
                    #add it to the list, but on a scale from 0-1 (if its over 1 thats okay, it will just displau as black)
                    returnList.append(i2/100)
        #return the list
        return returnList

    #returns the list of colors for the gaps
    def getColorsGaps(self):
        #makes an empty list
        returnList = []
        #loops over the dictionaries
        for key, item in self.gaps.items():
            for k2, i2 in item.items():
                for k3, i3 in i2.items():
                    #if gap is there
                    if(i3 == False):
                        #append a gap and a non gap (because of the way the return works)
                        returnList.append(1)
                        returnList.append(0)
                    else:
                        #just append a normal one
                        returnList.append(0)
        #return the list
        return returnList

    #switches between the two options
    def switchButton(self, event):
        #resets the list of colors to empty so that we dont double draw the boxes
        self.rectColors = []
        #if were looking at the bfactor
        if(self.bFactorButton):
            #say were no longer looking at the bfactor and go back to on-clicked
            self.bFactorButton = False
            self.OnClicked(None)
        #if not looking at the bfacors
        else:
            #set it to bfactors and go back to on-clicked
            self.bFactorButton = True
            self.OnClicked(None)
        self.Refresh()
        self.Show(True)

    #runs the initial program
    def OnClicked(self, event):
        #calls the method to run the phenix program
        self.myWinRun()
        #if currently looking at bfactor
        if(self.bFactorButton):
            #set the colors to the bfactor colors
            #in the future I should probably store this!
            colors = self.getColorsBFactor()
        else:
            #if looking at gaps, set the color to the gap colors
            #I should also definately store this
            colors = self.getColorsGaps()
        #if results are "none" then set results to 0 so it doesnt break!
        if(self.results is None):
            self.results = 0
        #make the number of rectangles equaal to results
        #results is the number of residue groups atm
        self.numRects = self.results
        #loop over the rectangles!
        for num in range(0, self.numRects, 1):
            #if there are more residue groups than colors, exit (if gaps, related to b-factor)
            #will improve this in the future
            if(num >= len(colors)):
                return
            #set the current property to the indicie in the list we are and make it into an rgb value
            self.prop = colors[num]
            self.rectColors.append(rainbow(self.prop))
        #redrawthe screen!
        self.Refresh()
        self.Centre()
        self.Show(True)

    #thsi method gets locations to draw in an arc!
    def yuh(self):
        #setting some local variables
        totalTheta = toRad(270)
        boxAngle = totalTheta/len(self.rectColors)
        pointList = []
        nextList = []
        returnList = []
        #loop over the colors(just to get the number of points)
        for i, j in enumerate(self.rectColors):
            #this calculates the points in polar and adds them to the list
            pointList.append([300,boxAngle*i + toRad(135)])
        #loop over them again
        for i, thing in enumerate(pointList):
            #but this time convert them to linear
            nextList.append(polToLin(thing[0],thing[1]))
        #loop for a third time
        for i, thing in enumerate(nextList):
            #this time offset each point by an ammount (preferably to center them)
            #I just hardcoded it for now </3
            returnList.append([thing[0] + 500, thing[1] + 355])
        #return the list of points!
        return returnList
        #this method is incredibly inefficient so I will be fixing it
            
    #this method actually draws stuff to the screen
    def OnPaint(self, e): 
        #wx python set up
        dc = wx.PaintDC(self) 
        dc.SetBackground(wx.Brush(self.bg_color))  
        dc.Clear() 
        #setting the points to be drawn 
        points = self.yuh()
        #looping over each residue group being drawn
        for i,col in enumerate (self.rectColors):
            #setting the color
            color = wx.Colour(*tuple(col))
            b = wx.Brush(color)
            dc.SetBrush(b)
            #drawing the residue groups :)
            dc.DrawCircle(points[i][0], points[i][1], 10)

    #this method runs the program to get information about the protein!
    def myWinRun(self):
        #setting the pdb file to be passed in 
        pdbfile = sys.argv[1]
        #running the programs
        self.results = run_program(program_class=Program, args=[pdbfile])
        self.bFactorData = run_program(program_class=BFactor.Program, args=[pdbfile])
        self.gaps = run_program(program_class=molecular_gaps.Program, args=[pdbfile])
  
#-------------------------------------------------------------------------------------------------------------------		
#program stuff
class Program(ProgramTemplate):
    datatypes = ['model', 'phil']
    def validate(self): pass

    #this actively runs my program, which basically just gets a podel
    def run(self):
    	model = self.data_manager.get_model()
    	hierarchy = model.get_hierarchy()
        #loop over the chains and stores the residue group size
        for chain in hierarchy.chains():
            numRects = chain.residue_groups_size()
        #sets it up to be returned
        self.results = numRects

    def get_results(self):
        #returns the results
    	return self.results
# ----------------------------------------------------------------------------------------------------------------------------
# running stuff
if __name__=='__main__':
    #starts the wxpython app
    ex = wx.App() 
    #draws it
    w = Mywin(None,'Drawing demo')
    #ends it
    ex.MainLoop()

#things Id like to add in the future:
#-make a class for the widgets on the screen, which will store their info (points, color, what they represent, etc)
#-make it clickable and more interactive!!!
#-make the code more optimal and sensical lmao