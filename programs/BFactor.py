from libtbx.program_template import ProgramTemplate
from iotbx.pdb import common_residue_names_get_class as get_class
from cctbx import adptbx

class pv_data(dict):
  def __re1pr__(self):
    outl = 'test'
    return outl

  def get_chain(self, chain_id):
    tmp = {}
    for key, item in self.items():
      if key.find(chain_id)>-1:
        tmp[key]=item
    return tmp

class Program(ProgramTemplate):

  datatypes = ['model','phil']

  def validate(self): 
    pass

#--------------------------------------------------------
  def BFactorFinder(self):
    model = self.data_manager.get_model()
    print('model',dir(model))
    BFactor = pv_data()
    hierarchy = model.get_hierarchy()
    for residue_group in hierarchy.residue_groups():
      averages = {}
      num_mc = 0
      num_sc = 0
      atom_group = residue_group.atom_groups()[0]
      # assert 0
      atom_Type = get_class(atom_group.resname)
      if atom_Type != 'common_amino_acid': 
        continue

      for atom in residue_group.atoms():
        ag = atom.parent()
        rg = ag.parent()
        chain = rg.parent()
        if atom.element_is_hydrogen():
          continue
        # print(dir(atom))
#------------------------------------------------------------
  #Anisotropic BFactor Check
      # if (atom.uij_is_defined):
      #   print(atom.uij)
      #   print(adptbx.u_as_b(adptbx.u_cart_as_u_iso(atom.uij)))
      #   print(atom.b)
#------------------------------------------------------------
  #See Different Classes and Branches
        # print(ag.resname,chain.id, rg.resseq)
    # print(dir(ag))
    # print('rg',rg.id_str())
    # print(chain.id)
    # print(ag.resname,chain.id, rg.resseq)
#------------------------------------------------------------
  #Averages 
        averages.setdefault('res', 0)
        averages['res'] += atom.b

        if atom.name.strip() == 'CA':
          averages['CA'] = atom.b
          #print('foundCA')
        if atom.name.strip() in ['CA', 'N', 'C', 'O', 'OXT']:
          averages.setdefault('main', 0)
          averages['main'] += atom.b
          num_mc += 1
          #print('foundMC',atom.name)
        else:
          averages.setdefault('side', 0)
          averages['side'] += atom.b
          num_sc += 1      
      #print (num_mc,num_sc)
      if num_mc != 0:
        averages['main'] /= num_mc
      if num_sc != 0:
        averages['side'] /= num_sc
      averages['res'] /= (num_mc + num_sc)

      # BFactor['chain.id'] = chain.id
      # BFactor['rg.resseq'] = rg.resseq
      BFactor[ag.id_str()] = averages

    # print(BFactor)
    for key, item in BFactor.items():
      print(key, item)
    print(BFactor.get_chain("A"))
    print(BFactor.get_chain("B"))


  def run(self): 
    self.BFactorFinder()

  def results(self):
    return self.results


# MainChain normally should be < SideChain (more movement outside)
#1yjp
  #(' TYR A   7 ', {'res': 15.122307692307695, 'CA': 15.18, 'main': 15.807999999999998, 'side': 14.693750000000001})
  #(' ASN A   6 ', {'res': 12.60625, 'CA': 12.3, 'main': 12.9025, 'side': 12.31})
  #Pi Stacking
    #Above the maine chain has a higher BFactor average than the side chain. But it can be justified because the side chain is stacked with other proteins, it restricted the movements of the side chain, which reduced the BFactor. 






