from libtbx.program_template import ProgramTemplate

class Program(ProgramTemplate):

  datatypes = ['model','phil']

  def validate(self): pass

  def run(self):
    print('hi')
    model = self.data_manager.get_model()
    print('model',dir(model))
    hierarchy = model.get_hierarchy()
    for residue_group in hierarchy.residue_groups():
      print(residue_group.id_str())

  def results(self):
    return self.results



