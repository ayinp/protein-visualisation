#Imports

from libtbx.program_template import ProgramTemplate
import sys
from iotbx.pdb import common_residue_names_get_class as get_class

#Ligand class

class ligandConnections(dict):

#Making the print neater

  def __repr__(self):
    outl = 'ligand connection'
    for other, item in self.items():
      outl += 'other\n'
      for an1 in item:
        outl += '  %s\n' % an1
    return outl

#Finding hBonds

  def find_h_bonds(self):
    hBonds = []
    for other, item in self.items():
      for an1 in item:
        #print('an1',an1)
        val = an1.values()[0]
        #print('val',val)
        #Checking if something is hBond
        if val["dist"]<=3 and val["isHydrogen"]==True:
          if val["LA element"] == "O" or val["NLA element"] == "O":
            val["isHbond"] = True
            val["bondedWith"] = 'Oxygen'
            hBonds.append(val)
          elif val["LA element"] == "N" or val["NLA element"] == "N":
            val["isHbond"] = True
            val["bondedWith"] = 'Nitrogen'
            hBonds.append(val)
          elif val["LA element"] == "F" or val["NLA element"] == "F":
            val["isHbond"] = True
            val["bondedWith"] = 'Flourine'
            hBonds.append(val)
      print('Hydrogen bonds:', hBonds)
      return hBonds

#Getting info from PDB

def get_phil_base_pairs(pdb_hierarchy, nonbonded_proxies,
    prefix=None, params=None,
    log=sys.stdout, add_segid=None, verbose=-1):
  distance_cutoff = 3.5 #Self-explanitory
  atoms = pdb_hierarchy.atoms()
  #Frankly I don't know why the names are all like this, but it makes the program actually work.
  sites_cart = atoms.extract_xyz()
  get_sorted_result = nonbonded_proxies.get_sorted(
      by_value="delta",
      sites_cart=sites_cart)
  sorted_nonb, n_not_shown = get_sorted_result
  n_nonb = len(sorted_nonb)
  i = 0

# Making dictionary of ligands, though it is empty now
  ligands = ligandConnections()

#Adding ligands to aforementioned dict
  while i < n_nonb and sorted_nonb[i][3] < distance_cutoff:
    (labels, i_seq, j_seq, dist, vdw_distance, sym_op_j, rt_mx) = sorted_nonb[i]
    #Snagging that yummy atom info and making it prettier
    a1 = atoms[i_seq]
    ag1 = a1.parent()
    a2 = atoms[j_seq]
    ag2 = a2.parent()
    #Seeing if there is an atom that is a ligand
    if get_class(ag1.resname)=='other' or get_class(ag2.resname)=='other':
      #print("a1 quote:",a1.quote(),". a2 quote:",a2.quote(),". dist:",dist, ". a1 resname:",ag1.resname, ". a2 resname:",ag2.resname, ". a1 resname class:",get_class(ag1.resname), ". a2 resname class:",get_class(ag2.resname))
      #Specifiying which is ligand (LA) and which isn't (NLA)
      if get_class(ag1.resname)=='other':
        LAg = ag1
        LA = a1
        NLA = a2
      else:
        LAg = ag2
        LA = a2
        NLA = a1
      #Putting atom info into dict        
      ligands.setdefault(LAg.id_str(), [])
      NLAinfo = {'atom': NLA.id_str(), 'dist' : dist, 'vdwDist' : vdw_distance, 'isHydrogen' : NLA.element_is_hydrogen()}
      if rt_mx:
        NLAinfo['rot matrix'] = rt_mx
      NLAinfo['LA element'] = LA.element.strip()
      NLAinfo['NLA element'] = NLA.element.strip()
      ligands[LAg.id_str()].append({LA.name.strip():NLAinfo})
    i += 1
  print('Ligands:', ligands)

  ligands.find_h_bonds()

#This just runs the program

class Program(ProgramTemplate):
  datatypes = ['model', 'phil']

  def validate(self): pass

  def run(self):
    model = self.data_manager.get_model()
    model.process(make_restraints=True)
    hierarchy = model.get_hierarchy()
    #print(dir(model))
    grm = model.get_restraints_manager()
    geometry = grm.geometry
    #print(dir(geometry))
    base_pairs = get_phil_base_pairs(
      pdb_hierarchy=hierarchy,
      nonbonded_proxies=geometry.pair_proxies(
        sites_cart=hierarchy.atoms().extract_xyz()).\
          nonbonded_proxies,
      prefix="test",)