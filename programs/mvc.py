from libtbx.program_template import ProgramTemplate
from wxGUI2 import Preferences, utils
import wxGUI2
import wx
import math
import wx 
from iotbx.cli_parser import run_program
import sys

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
    b = (1-prop)*255
    return [r,0,b]


#----------------------------------------------------------------------------------------------------------------------
#threading

print(rainbow(.2))




#---------------------------------------------------------------------------------------------------------------------
#window stuff


#create a panel class and add it to the frame class
#for button color change
    #color want = self.colour, save, on paint will read it and change the background
    #create an event class w/ attrobute and pass it to on paint


class Mywin(wx.Frame): 
            
    def __init__(self, parent, title): 
    	super(Mywin, self).__init__(parent, title = title,size = (1024, 618))  
    	self.InitUI() 
          
    def InitUI(self): 
        self.up = True
        self.prop = 0
        self.bg_color = "pink"
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        text = wx.StaticText(self.panel, label = "wow, I am sooo good at text")
        text.SetBackgroundColour((0,255,0))
        self.sizer.Add(text, proportion = 1, flag = wx.RIGHT, border = 5)

        ID_NO = wx.NewId()
        button = wx.Button(self, ID_NO, 'DO NOT PRESS THIS BUTTON', pos=(20,40))
        button.Bind(wx.EVT_BUTTON, self.OnClicked, id=ID_NO)
        self.sizer.Add(button, 1, wx.ALL|wx.EXPAND, 0)

        self.panel.SetSizer(self.sizer)
        self.Centre()
        self.Show(True)

        self.Bind(wx.EVT_PAINT, self.OnPaint) 


    def OnClicked(self, event):
        text = wx.StaticText(self.panel, label = "WHY DID YOU DO THAT", size = (200, 300), pos = (100,100))
        self.sizer.Add(text, proportion = 10, flag = wx.Centre, border = 10)
        self.bg_color = rainbow(self.prop)
        if(self.up):
            self.prop += .05
            print(self.prop)
        else:
            self.prop -= .05
            print(self.prop)
        if(self.prop > 1):
            self.prop = 1
            self.up = False
        elif(self.prop < 0):
            self.prop = 0
            self.up = True
        self.Refresh()
        self.Centre()
        self.Show(True)


    def OnPaint(self, e): 
        print("on paint")
        dc = wx.PaintDC(self) 
        dc.SetBackground(wx.Brush(self.bg_color))  
        dc.Clear() 
        color = wx.Colour(255,0,0)
        b = wx.Brush(color) 
        dc.SetBrush(b) 
        
    def myWinRun(self):
        run_program(program_class=Program, args=[sys.argv[1]])
  
#-------------------------------------------------------------------------------------------------------------------		
#program stuff

class Program(ProgramTemplate):
    datatypes = ['model', 'phil']
  
    def validate(self): pass
  
    def run(self):
    	model = self.data_manager.get_model()
    	hierarchy = model.get_hierarchy()
    	print("residue groups \n")
    	for residue_group in hierarchy.residue_groups():
    		for atom in residue_group.atoms():
    			print(atom.quote())

    def results(self):
    	return self.results
  
    def drawResidueGroups(self, dc):
    	numDeg = (3*math.pi()/2)/len(hierarchy.residue_groups)
    	d = 1/6*numDeg
    	dc.AddArc(300, -45, 225)
#----------------------------------------------------------------------------------------------------------------------------
#running stuff


if __name__=='__main__':
	ex = wx.App() 
	w = Mywin(None,'Drawing demo')
	ex.MainLoop()


