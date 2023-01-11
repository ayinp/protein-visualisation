from libtbx.program_template import ProgramTemplate
from iotbx.pdb import common_residue_names_get_class as get_class
import math

def dist_Squared(xyz1, xyz2):
  d2 = 0
  for i in range (3):
    d2 += (xyz1[i] - xyz2[i])**2
  return d2

def dist_Check(c_Alphas):
  for i in range (len(c_Alphas)-2):
    d2 = dist_Squared(c_Alphas[i].xyz, c_Alphas[i + 2].xyz)



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
# Gap Finder

  def gap_Finder(self):
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
        # else:
        #   continue
        print(residue_group.id_str())
        print(get_class(atom.parent().resname))
        print(atom.quote(), atom.xyz)
        print(atom.parent().resname)

    print(self.c_Alphas)

    dist_Check(self.c_Alphas)


