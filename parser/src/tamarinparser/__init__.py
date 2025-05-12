from .ast_builder import *
from .tok import *
from .syntax import *
from .scenarios import *
import ply.yacc as yacc
import os.path
import copy

def parse_theory(content):
    parser = yacc.yacc()
    s_parser = parser
    return parser.parse(content)
