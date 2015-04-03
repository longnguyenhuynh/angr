#!/usr/bin/env python

import logging
l = logging.getLogger("angr_tests")

import angr
import nose

# load the tests
import os
test_location = str(os.path.dirname(os.path.realpath(__file__)))
memset_amd64 = None

def setup_module():
    setup_amd64()

def setup_amd64():
    global memset_amd64
    memset_amd64 = angr.Project(test_location + "/blob/x86_64/memset", load_options={'auto_load_libs': True}, exclude_sim_procedures=['memset'])

def test_amd64():
    explorer = angr.surveyors.Explorer(memset_amd64, find=[0x400608]).run()
    s = explorer.found[0].state
    result = s.se.any_str(s.mem_expr(s.reg_expr(16), 50))
    nose.tools.assert_equals(result, 'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB\x00')

if __name__ == "__main__":
    try:
        __import__('standard_logging')
        __import__('angr_debug')
    except ImportError:
        pass

    setup_amd64()
    test_amd64()
