from libtbx.program_template import ProgramTemplate
from iotbx.pdb import common_residue_names_get_class as get_class

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
      # print(atom_group.id)
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
        # print(ag.resname,chain.id, rg.resseq)
    # print(dir(ag))
    # print('rg',rg.id_str())
    # print(chain.id)
    # print(ag.resname,chain.id, rg.resseq)

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

    # print(BFactor.get_chain("A"))
    # print(BFactor.get_chain("B"))

  def run(self): 
    self.BFactorFinder()

  def results(self):
    return self.results









