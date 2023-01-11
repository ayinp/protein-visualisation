from libtbx.program_template import ProgramTemplate
from wxGUI2 import Preferences, utils
import wxGUI2
import wx

import wx 
 
class Mywin(wx.Frame): 
            
   def __init__(self, parent, title): 
      super(Mywin, self).__init__(parent, title = title,size = (500,300))  
      self.InitUI() 
         
   def InitUI(self): 
      self.Bind(wx.EVT_PAINT, self.OnPaint) 
      self.Centre() 
      self.Show(True)
		
   def OnPaint(self, e): 
      dc = wx.PaintDC(self) 
      # brush = wx.Brush("pink")  
      dc.SetBackground(wx.Brush("pink"))  
      dc.Clear() 
        
      color = wx.Colour(255,0,0)
      b = wx.Brush(color) 
      dc.SetBrush(b) 
      dc.DrawCircle(300,100,50) 
      # dc.SetBrush(wx.Brush(wx.Colour(255,255,255))) 
      # dc.DrawCircle(300,125,30) 
		
      # font = wx.Font(18, wx.ROMAN, wx.ITALIC, wx.NORMAL) 
      # dc.SetFont(font) 
      # dc.DrawText("Hello wxPython",200,10) 
		
      # pen = wx.Pen(wx.Colour(0,0,255)) 
      # dc.SetPen(pen) 
      # dc.DrawLine(200,50,350,50) 
      # dc.SetBrush(wx.Brush(wx.Colour(0,255,0), wx.CROSS_HATCH)) 
      # dc.DrawRectangle(380, 15, 90, 60) 
		




class Program(ProgramTemplate):
  datatypes = ['model', 'phil']

  def validate(self): pass

  def run(self):
  	model = self.data_manager.get_model()
  	print('model \n',dir(model))
  	hierarchy = model.get_hierarchy()
  	print('hierarchy \n', dir(hierarchy))
  	print("residue groups \n")
  	for residue_group in hierarchy.residue_groups():
  		for atom in residue_group.atoms():
  			print(atom.quote())



  def results(self):
  	return self.results

ex = wx.App() 
Mywin(None,'Drawing demo') 
ex.MainLoop()