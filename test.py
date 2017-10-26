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

def test_parse_sentence(sent, charoffset):
    charoffsets = utils.parse_charoffset(charoffset)
    words = utils.parse_sentence(sent)
    print(words)
    entity = {'charOffset': [29, 39], 'type': 'drug'}
    for charoffset in charoffsets:
        entity['charOffset'] = charoffset
        utils.tag_word(words, entity)
        print(words)
    
if __name__ == '__main__':
#    test_parse_charoffset()
    
    sent = "Antidepressants, tricyclic?Amphetamines may enhance the activity of tricyclic antidepressants or sympathomimetic agents;"
    charoffset = '68-93'
    test_parse_sentence(sent, charoffset)
    
    '''
    filename = '../data/drugddi2011/pred.ddi'
    with open(filename, 'r') as f:
        pred = utils.labelseq2conll(f.readlines())
    
    filename = '../data/drugddi2011/test.ddi'
    with open(filename, 'r') as f:
        gold = utils.iob2etype(f.readlines())
    utils.find_error(gold, pred, '../data/drugddi2011/error.txt')
    '''
    