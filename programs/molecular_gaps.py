from libtbx.program_template import ProgramTemplate
from iotbx.pdb import common_residue_names_get_class as get_class
import math

#--------------------------------------------------------------------------------

# Definition of Dictionary Class Linkage

class linkages(dict):
  def __repr__(self):
    outl = 'linkages\n'
    for key, item in self.items():
      outl += '  %s : %s\n' % (key, item)
    return outl

#--------------------------------------------------------------------------------

# Distance Formula for Gap Detection

def dist_Squared(xyz1, xyz2):
  d2 = 0
  for i in range (3):
    d2 += (xyz1[i] - xyz2[i])**2
  return d2

#--------------------------------------------------------------------------------

# Translates Array of Carbon Alphas into Boolean Detection

def bool_Gaps(c_Alphas):
  binary_C_Alphas = []
  my_linkage = linkages()
  for i in range (len(c_Alphas)-1):
    key = (c_Alphas[i].parent().id_str(), c_Alphas[i + 1].parent().id_str())
    my_linkage.setdefault(key, False)
    d2 = dist_Squared(c_Alphas[i].xyz, c_Alphas[i +1].xyz)
    if d2 < 20.25:
      my_linkage[key] = True
  print(my_linkage)
  
#--------------------------------------------------------------------------------

# Start of Main Program

class Program(ProgramTemplate):
  description = '''
  molecular gaps need a model / pdb file '''
  datatypes = ['model', 'phil']

  c_Alphas = []

  def validate(self):
    pass

  def run(self):
    self.gap_Finder()

  def results(self):
     return self.results

#--------------------------------------------------------------------------------

# Data Retriever and Interpreter for .pdb Files. Also Main function

  def data_Finder(self):
    model = self.data_manager.get_model()
    hierarchy = model.get_hierarchy()
    for chain in hierarchy.chains():
      for residue_group in chain.residue_groups():
        atom_group = residue_group.atom_groups()[0]
        atom = atom_group.get_atom('CA')
        if atom is None:
          continue
        print(atom.quote())
        atom_Type = get_class(atom.parent().resname)
        if atom_Type != 'common_amino_acid':
          continue
        if atom.name.strip() == 'CA':
          self.c_Alphas.append(atom)

    binary_Gaps(self.c_Alphas)

#--------------------------------------------------------------------------------