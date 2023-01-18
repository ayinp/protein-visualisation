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
class MyError:
	def __init__(self, message):
		self.message = message

def linToPol(x,y):
	if(y == 0):
        #returns an error if we divide by zero
		e = MyError("y cannot be 0")
		print(e.message)
		return e
	point =  wx.Point(math.sqrt((x*x), (y*y)), math.atan(x/y))
	print(point)
	return point

def polToLin(r,theta):
	point = wx.Point(r*math.cos(theta), r*math.sin(theta))
	return point

def toRad(degree):
    return degree*math.pi/180

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

# def rainbow(prop):
#     if(prop > 1 or prop < 0):
#         return [0,0,0]
#     r = 255*prop
#     b = 255*(1-prop)
#     return [r,0,b]

#---------------------------------------------------------------------------------------------------------------------
#window stuff
class Mywin(wx.Frame): 
            
    def __init__(self, parent, title): 
    	super(Mywin, self).__init__(parent, title = title,size = (1024, 618))  
    	self.InitUI() 
          
    def InitUI(self): 
        print("initUI")
        self.bFactorButton = False
        self.prop = 0
        self.numRects = 0
        self.rectColors = []

        self.bg_color = [240,240,240]
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        ID_NO = wx.NewId()
        button = wx.Button(self, ID_NO, 'run', pos=(20,40))
        button.Bind(wx.EVT_BUTTON, self.OnClicked, id=ID_NO)
        self.sizer.Add(button, 1, wx.ALL|wx.EXPAND, 0)

        ID_SWITCH = wx.NewId()
        self.newBut = wx.Button(self, ID_SWITCH, 'switch', pos = (100, 40))
        self.newBut.Bind(wx.EVT_BUTTON, self.switchButton, id=ID_SWITCH)
        self.sizer.Add(self.newBut, 1, wx.ALL|wx.EXPAND, 0)

        self.panel.SetSizer(self.sizer)
        self.Centre()
        self.Show(True)

        self.Bind(wx.EVT_PAINT, self.OnPaint) 

    def switchButton(self, event):
        print("HELLO I GOT HERE MOM< I AM SO COOL")
        self.rectColors = []
        if(self.bFactorButton):
            self.bFactorButton = False
            self.OnClicked(None)
        else:
            print("got here")
            self.bFactorButton = True
            self.OnClicked(None)
        self.Refresh()
        self.Centre()
        self.Show(True)

    def getColorsBFactor(self):
        returnList = []
        for key, item in self.bFactorData.items():
            for k2, i2 in item.items():
                if(k2 == "res"):
                    returnList.append(i2/100)
        return returnList

    def getColorsGaps(self):
        returnList = []
        for key, item in self.gaps.items():
            for k2, i2 in item.items():
                for k3, i3 in i2.items():
                    if(i3 == False):
                        returnList.append(1)
                        returnList.append(0)
                    else:
                        returnList.append(0)
        print(returnList)
        return returnList

    def OnClicked(self, event):
        print("in on clicked rn")
        self.myWinRun()
        if(self.bFactorButton):
            colors = self.getColorsBFactor()
        else:
            colors = self.getColorsGaps()
        if(self.results is None):
            self.results = 0
        self.numRects = self.results
        for num in range(0, self.numRects, 1):
            if(num >= len(colors)):
                return
            self.prop = colors[num]
            self.rectColors.append(rainbow(self.prop))
        self.Refresh()
        self.Centre()
        self.Show(True)

    def yuh(self):
        totalTheta = toRad(270)
        boxAngle = totalTheta/len(self.rectColors)
        pointList = []
        nextList = []
        returnList = []
        for i, j in enumerate(self.rectColors):
            pointList.append([300,boxAngle*i + toRad(135)])
        for i, thing in enumerate(pointList):
            nextList.append(polToLin(thing[0],thing[1]))
        print(nextList)
        for i, thing in enumerate(nextList):
            returnList.append([thing[0] + 500, thing[1] + 355])
        print(returnList)
        return returnList
            


    def OnPaint(self, e): 
        print("on paint")
        dc = wx.PaintDC(self) 
        dc.SetBackground(wx.Brush(self.bg_color))  
        dc.Clear() 
        points = self.yuh()
        for i,col in enumerate (self.rectColors):
            color = wx.Colour(*tuple(col))
            b = wx.Brush(color)
            dc.SetBrush(b)
            dc.DrawCircle(points[i][0], points[i][1], 10)
            # row = math.floor(i/20)+2
            # column = i%20
            # xPos = column*50
            # yPos = row*50
            # dc.DrawRectangle(xPos, yPos, 50,50)
        print("YUH")
        self.yuh()


    def myWinRun(self):
        print("myWinRun")
        pdbfile = sys.argv[1]
        self.results = run_program(program_class=Program, args=[pdbfile])
        self.bFactorData = run_program(program_class=BFactor.Program, args=[pdbfile])
        print("CONNOR")
        self.gaps = run_program(program_class=molecular_gaps.Program, args=[pdbfile])
  
#-------------------------------------------------------------------------------------------------------------------		
#program stuff
class Program(ProgramTemplate):
    datatypes = ['model', 'phil']
  
    def validate(self): pass

    def run(self):
        print("i am running the program!")
    	model = self.data_manager.get_model()
    	hierarchy = model.get_hierarchy()
        for chain in hierarchy.chains():
            numRects = chain.residue_groups_size()
        self.results = numRects

    def get_results(self):
        print("returing stuff", self.results)
    	return self.results
  
    def drawResidueGroups(self, dc):
        print("if this shows up somethign went wrong")
    	numDeg = (3*math.pi()/2)/len(hierarchy.residue_groups)
    	d = 1/6*numDeg
    	dc.AddArc(300, -45, 225)
# ----------------------------------------------------------------------------------------------------------------------------
# running stuff
if __name__=='__main__':
    ex = wx.App() 
    w = Mywin(None,'Drawing demo')
    ex.MainLoop()