from libtbx.program_template import ProgramTemplate
from iotbx.pdb import common_residue_names_get_class as get_class


class Program(ProgramTemplate):

  description = '''
  molecular gaps need a model/pdb file'''

  datatypes = ['model', 'phil']

  def validate(self):
    pass


#----------------------------------------------------------------------------------------------------
  # Gap Finder
  def gap_Finder(self):
    model = self.data_manager.get_model()
    print('model',dir(model))
    hierarchy = model.get_hierarchy()
    for residue_group in hierarchy.residue_groups():
      for atom in residue_group.atoms():
        # print(atom.quote(), atom.xyz)
        # print(atom.parent().resname)
        
        atom_Type = get_class(atom.parent().resname)
        if atom_Type != 'common_amino_acid':
        	continue
        print(residue_group.id_str())
        print(get_class(atom.parent().resname) )

  def run(self): 
    self.gap_Finder()
  

#----------------------------------------------------------------------------------------------------
  # Distance Checker 


#----------------------------------------------------------------------------------------------------



#----------------------------------------------------------------------------------------------------


  def results(self):
    return self.results

  