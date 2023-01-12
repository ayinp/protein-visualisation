from libtbx.program_template import ProgramTemplate
import sys
from iotbx.pdb import common_residue_names_get_class as get_class

class ligandConnections(dict):
  # def __init__ (self):

  def __repr__(self):
    outl = 'ligand connection'
    for other, item in self.items():
      outl += 'other\n'
      for an1 in item:
        outl += '  %s\n' % an1
    return outl

  def find_h_bonds(self):
    # 2.8
    assert 0

def get_phil_base_pairs(pdb_hierarchy, nonbonded_proxies,
    prefix=None, params=None,
    log=sys.stdout, add_segid=None, verbose=-1):
  hbond_distance_cutoff = 2.9
  if params is not None:
    hbond_distance_cutoff = params.hbond_distance_cutoff
  hbonds = []
  result = ""
  atoms = pdb_hierarchy.atoms()
  sites_cart = atoms.extract_xyz()
  get_sorted_result = nonbonded_proxies.get_sorted(
      by_value="delta",
      sites_cart=sites_cart)
  if get_sorted_result is None:
    return result
  sorted_nonb, n_not_shown = get_sorted_result

  # Get potential hbonds
  n_nonb = len(sorted_nonb)
  i = 0

  ligands = ligandConnections()

  while i < n_nonb and sorted_nonb[i][3] < hbond_distance_cutoff:
    (labels, i_seq, j_seq, dist, vdw_distance, sym_op_j, rt_mx) = sorted_nonb[i]
    a1 = atoms[i_seq]
    ag1 = a1.parent()
    a2 = atoms[j_seq]
    ag2 = a2.parent()
    if get_class(ag1.resname)=='other' or get_class(ag2.resname)=='other':
      print("a1 quote:",a1.quote(),". a2 quote:",a2.quote(),". dist:",dist, ". a1 resname:",ag1.resname, ". a2 resname:",ag2.resname, ". a1 resname class:",get_class(ag1.resname), ". a2 resname class:",get_class(ag2.resname))
      if get_class(ag1.resname)=='other':
        LAg = ag1
        LA = a1
        NLA = a2
      else:
        LAg = ag2
        LA = a2
        NLA = a1
      ligands.setdefault(LAg.id_str(), [])
      extraInfo = {'atom': NLA.id_str(), 'dist' : dist, 'vdwDist' : vdw_distance}
      # rename that ^ lol
      if sym_op_j:
        extraInfo['sym op j'] = sym_op_j
      if rt_mx:
        extraInfo['rot matrix'] = rt_mx
      ligands[LAg.id_str()].append({LA.name.strip():extraInfo})
    i += 1
  print(ligands)

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