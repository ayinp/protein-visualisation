from libtbx.program_template import ProgramTemplate
from iotbx.pdb import common_residue_names_get_class as get_class
import math


# Translates Array of Carbon Alphas into Boolean Detection

def bool_Gaps(c_Alphas):
  my_linkage = linkages()
  false_Linkage = linkages()
  for i in range (len(c_Alphas)-1):
    key = (c_Alphas[i].parent().id_str(), c_Alphas[i + 1].parent().id_str())
    my_linkage.setdefault(key, False)
    d2 = dist_Squared(c_Alphas[i].xyz, c_Alphas[i +1].xyz)
    # Distance Squared
    if d2 < 20.25:
      my_linkage[key] = True
    else:
      false_Linkage[key] = True
  return my_linkage, false_Linkage


#--------------------------------------------------------------------------------

# Definition of Dictionary Class Linkage

class linkages(dict):
  def __repr__(self):
    outl = 'linkages\n'
    for key, item in self.items():
      outl += '  %s : %s\n' % (key, item)
    return outl

#--------------------------------------------------------------------------------

# Class Method that Returns a List of Residues in Respective Slots
  # def get_Gap(self, c_Alphas):
  #   rc = bool_Gaps(c_Alphas)
  #   print(rc)
  #   assert 0



#--------------------------------------------------------------------------------

# Distance Formula for Gap Detection

def dist_Squared(xyz1, xyz2):
  d2 = 0
  for i in range (3):
    d2 += (xyz1[i] - xyz2[i])**2
  return d2

#--------------------------------------------------------------------------------

# Start of Main Program

class Program(ProgramTemplate):
  description = '''
  molecular gaps need a model / pdb file '''
  datatypes = ['model', 'phil']

  c_Alphas = {}

  def validate(self):
    pass

  def run(self):
    self.data_Finder()
    # print(self.c_Alphas)
    self.results = {}
    for chain_id, c_Alphas in self.c_Alphas.items():
      tmp_linkage, tmp_false = bool_Gaps(c_Alphas)
      self.results[chain_id] = {}
      self.results[chain_id]['all connections'] = tmp_linkage
      self.results[chain_id]['all gaps'] = tmp_false

    # print out
    # print(self.results)
    print(self.get_chain_connections('A'))
    print(self.get_chain_connections('B'))
    print(self.get_chain_gaps('A'))
    print(self.get_chain_gaps('B'))

  def get_chain_connections(self, chain_id):
    print('get_chain_connections', chain_id)
    rc = self.results.get(chain_id, {})
    if not rc:
      return rc

    return rc['all connections']

  def get_chain_gaps(self, chain_id):
    print('get_chain_gaps', chain_id)
    rc = self.results.get(chain_id, {})
    if not rc:
      return rc

    return rc['all gaps']

  def get_linkage_info(self, chain_id, key):
    if key == 'all gaps':
      get_chain_gaps(self, chain_id)
    if key == 'all connections':
      get_chain_connections(self, chain_id)


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
        atom_Type = get_class(atom.parent().resname)
        if atom_Type != 'common_amino_acid':
          continue
        if atom.name.strip() == 'CA':
          self.c_Alphas.setdefault(chain.id, [])
          self.c_Alphas[chain.id].append(atom)
    

#--------------------------------------------------------------------------------