from __future__ import absolute_import, division, print_function

from iotbx.cli_parser import run_program 
import phenix
from phenix.programs.mvc import Program

if (__name__ == '__main__'):
  results = run_program(program_class=Program)
