from __future__ import absolute_import, division, print_function

from iotbx.cli_parser import run_program
import phenix.programs
import sys
print(sys.path)
import phenix.programs.ligand
from phenix.programs.ligand import Program

if (__name__ == '__main__'):
  results = run_program(program_class=Program)
