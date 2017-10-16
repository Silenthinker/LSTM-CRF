#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test methods
"""

import utils

def test_substring_indices():
    substring = 'it'
    string = 'it is it.'
    print(list(utils.substring_indices(substring, string)))
    
def test_parse_charoffset():
    charoffset = '3-7'
    print(utils.parse_charoffset(charoffset))

def test_parse_sentence():
    sent = 'it is it'
    print(utils.parse_sentence(sent))
    
if __name__ == '__main__':
#    test_parse_charoffset()
    
    test_parse_sentence()