from libtbx.program_template import ProgramTemplate
import sys
from iotbx.pdb import common_residue_names_get_class as get_class

def get_phil_base_pairs(pdb_hierarchy, nonbonded_proxies,
    prefix=None, params=None,
    log=sys.stdout, add_segid=None, verbose=-1):
  hbond_distance_cutoff = 3.4
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
  while i < n_nonb and sorted_nonb[i][3] < hbond_distance_cutoff:
    (labels, i_seq, j_seq, dist, vdw_distance, sym_op_j, rt_mx) = sorted_nonb[i]
    a1 = atoms[i_seq]
    ag1 = a1.parent()
    a2 = atoms[j_seq]
    ag2 = a2.parent()
    print(a1.quote(),a2.quote(),dist, ag1.resname, ag2.resname, get_class(ag1.resname), get_class(ag2.resname))
    if (get_class(ag1.resname, consider_ccp4_mon_lib_rna_dna=True) in \
          ["common_rna_dna", "ccp4_mon_lib_rna_dna"] and
        get_class(ag2.resname, consider_ccp4_mon_lib_rna_dna=True) in \
          ["common_rna_dna", "ccp4_mon_lib_rna_dna"] and
        (a1.element in ["N", "O"] and a2.element in ["N", "O"]) and
        a1.name.find("P") < 0 and a2.name.find("P") < 0 and
        a1.name.find("'") < 0 and a2.name.find("'") < 0 and
        not consecutive_residues(a1, a2) and
        (ag1.altloc.strip() == ag2.altloc.strip()) and
        final_link_direction_check(a1, a2)):
      hbonds.append((i_seq, j_seq))
    i += 1

class Program(ProgramTemplate):
  datatypes = ['model', 'phil']

  def validate(self): pass

  def run(self):
    model = self.data_manager.get_model()
    model.process(make_restraints=True)
    hierarchy = model.get_hierarchy()
    print(dir(model))
    grm = model.get_restraints_manager()
    geometry = grm.geometry
    print(dir(geometry))
    print('HI')
    base_pairs = get_phil_base_pairs(
      pdb_hierarchy=hierarchy,
      nonbonded_proxies=geometry.pair_proxies(
        sites_cart=hierarchy.atoms().extract_xyz()).\
          nonbonded_proxies,
      prefix="test",)