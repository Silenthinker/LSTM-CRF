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
    charoffset = '0-2;4-5'
    return utils.parse_charoffset(charoffset)

def test_parse_sentence():
    sent = 'it( is it'
    charoffset = '0-2;4-5'
    charoffsets = utils.parse_charoffset(charoffset)
    words = utils.parse_sentence(sent)
    print(words)
    entity = {'charOffset': [0, 2], 'type': 'eng'}
    for charoffset in charoffsets:
        entity['charOffset'] = charoffset
        utils.tag_word(words, entity)
        print(words)
    
if __name__ == '__main__':
#    test_parse_charoffset()
    
    test_parse_sentence()
    