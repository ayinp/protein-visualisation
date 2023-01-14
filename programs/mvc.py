from libtbx.program_template import ProgramTemplate
from wxGUI2 import Preferences, utils
import wxGUI2
import wx
import math
import wx 
from iotbx.cli_parser import run_program
import sys
import random

#-------------------------------------------------------------------------------------------------------------------
#tools

class MyError:
	def __init__(self, message):
		self.message = message

def linToPol(x,y):
	if(y == 0):
		e = MyError("y cannot be 0")
		print(e.message)
		return e
	point =  wx.Point(math.sqrt((x*x), (y*y)), math.atan(x/y))
	print(point)
	return point

def polToLin(r,theta):
	point = wx.Point(r*math.cos(theta), r*math.sin(theta))
	return point

def rainbow(prop):
    if(prop > 1 or prop < 0):
        return [0,0,0]
    r = 255*prop
    b = 255*(1-prop)
    return [r,0,b]

#----------------------------------------------------------------------------------------------------------------------
#threading

#---------------------------------------------------------------------------------------------------------------------
#window stuff

class Mywin(wx.Frame): 
            
    def __init__(self, parent, title): 
    	super(Mywin, self).__init__(parent, title = title,size = (1024, 618))  
    	self.InitUI() 
          
    def InitUI(self): 
        print("initUI")
        # self.up = True
        self.prop = 0
        self.numRects = 0
        self.rectColors = []

        self.bg_color = "pink"
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        ID_NO = wx.NewId()
        button = wx.Button(self, ID_NO, 'DO NOT PRESS THIS BUTTON', pos=(20,40))
        button.Bind(wx.EVT_BUTTON, self.OnClicked, id=ID_NO)
        self.sizer.Add(button, 1, wx.ALL|wx.EXPAND, 0)

        self.panel.SetSizer(self.sizer)
        self.Centre()
        self.Show(True)

        self.Bind(wx.EVT_PAINT, self.OnPaint) 

    def OnClicked(self, event):
        print("in on clicked rn")
        self.myWinRun()
        if(self.results is None):
            self.results = 0
        self.numRects = self.results
        print(self.numRects)
        for num in range(0, self.numRects, 1):
            self.prop = random.random()
            self.rectColors.append(rainbow(self.prop))
        # self.bg_color = rainbow(self.prop)
        # if(self.up):
        #     self.prop += .05
        #     print(self.prop)
        # else:
        #     self.prop -= .05
        #     print(self.prop)
        # if(self.prop > 1):
        #     self.prop = 1
        #     self.up = False
        # elif(self.prop < 0):
        #     self.prop = 0
        #     self.up = True
        self.Refresh()
        self.Centre()
        self.Show(True)

    def OnPaint(self, e): 
        print("on paint")
        dc = wx.PaintDC(self) 
        dc.SetBackground(wx.Brush(self.bg_color))  
        dc.Clear() 

        for i,col in enumerate (self.rectColors):
            color = wx.Colour(*tuple(col))
            b = wx.Brush(color)
            dc.SetBrush(b)
            dc.DrawRectangle(i*50, 100, 50,50)


    def myWinRun(self):
        print("myWinRun")
        self.results = run_program(program_class=Program, args=[sys.argv[1]])
        print("these are the results")
        print(self.results)
  
#-------------------------------------------------------------------------------------------------------------------		
#program stuff

class Program(ProgramTemplate):
    datatypes = ['model', 'phil']
  
    def validate(self): pass

    def run(self):
        print("i am running the program!")
    	model = self.data_manager.get_model()
    	hierarchy = model.get_hierarchy()
        #print(dir(hierarchy))
        #this is only the first chain which is an issue for later </3
        #dictionary with a key of a chain, and for each chain we put interests
        for chain in hierarchy.chains():
            numRects = chain.residue_groups_size()
        self.results = numRects
    	# for residue_group in hierarchy.residue_groups():
    	# 	for atom in residue_group.atoms():
    	# 		print(atom.quote())
        print('RESY')
        print(self.results)

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