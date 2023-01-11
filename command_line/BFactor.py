from __future__ import absolute_import, division, print_function
import sys

print(sys.path)
from iotbx.cli_parser import run_program
import protein_visualisation
from protein_visualisation.programs.BFactor import Program

if (__name__ == '__main__'):
  results = run_program(program_class=Program)
