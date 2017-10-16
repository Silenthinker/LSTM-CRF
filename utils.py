#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET

''' Example
<document id="DrugDDI.d89" origId="Aciclovir">
    <sentence id="DrugDDI.d89.s0" origId="s0" text="Co-administration of probenecid with acyclovir has been shown to increase the mean half-life and the area under the concentration-time curve.">
        <entity id="DrugDDI.d89.s0.e0" origId="s0.p1" charOffset="21-31" type="drug" text="probenecid"/>
        <entity id="DrugDDI.d89.s0.e1" origId="s0.p2" charOffset="37-47" type="drug" text="acyclovir"/>
        <pair id="DrugDDI.d89.s0.p0" e1="DrugDDI.d89.s0.e0" e2="DrugDDI.d89.s0.e1" interaction="true"/>
    </sentence><sentence id="DrugDDI.d89.s1" origId="s1" text="Urinary excretion and renal clearance were correspondingly reduced."/>
    <sentence id="DrugDDI.d89.s2" origId="s2" text="The clinical effects of this combination have not been studied."/>
</document>
'''

class Word:
    def __init__(self, index, text, etype):
        self.index = index
        self.text = text
        self.etype = etype
    
    def __repr__(self):
        return '[index: {}, text: {}, etype: {}]'.format(self.index, self.text, self.etype)
    
    __str__ = __repr__
        

def parse_charoffset(charoffset):
    """
    Parse charoffset to a tuple containing start and end indices.
    Example:
        charoffset = '3-7'
        print(parse_charoffset(charoffset))
        
        [3, 7]
    """
    return [int(s) for s in charoffset.split('-')]
    
def parse_sentence(sent):
    """
    Parse sentence to get a list of Word class
    Example:
        sent = 'it is it'
        print(parse_sentence(sent))
        
        [(0, 'it', 'O'), (3, 'is', 'O'), (6, 'it', 'O')]
    """
    sent = sent.rstrip()
    res = []
    if len(sent) == 0:
        return res
    i = j = 0
    while j <= len(sent):
        if j < len(sent) and sent[j] != ' ':
            j += 1
        else:
            res.append(Word(i, sent[i:j], 'O'))
            i = j + 1
            j = i
    return res

def tag_word(words, entity):
    """
    Args:
        entity: dict has keys charOffset, type, text
    Tag Word with entity type in-place
    Example:
        words = [(0, 'it', O), (3, 'is', O), (6, 'it', O)]
        entity = {'charOffset': [0, 2], 'type': 'eng'} # [inclusive, exclusive]
        print(tag_word(words, entity))
        
        [(0, 'it', 'B-ENG'), (3, 'is', 'O'), (6, 'it', 'O')]
    """
    beg, end = entity['charOffset']
    count = 0
    for word in words:
        if word.index >= beg and word.index < end:
            count += 1
            if count > 1:
                word.etype = 'I-' + entity['type'].upper()
            else:
                word.etype = 'B-' + entity['type'].upper()
            
def generate_annotated_sentences(root):
    """
    Args:
        root: root Element of XML
    """
    for sent in root.findall('sentence'):
        words = parse_sentence(sent.get('text'))
        for entity in sent.findall('entity'):
            attributes = entity.attrib
            attributes['charOffset'] = parse_charoffset(attributes['charOffset'])
            tag_word(words, attributes)
        yield words

    
if __name__ == '__main__':
    data_path = '../data/ddi_tiny/Adalimumab_ddi.xml'
    # import xml data into ElementTree
    tree = ET.parse(data_path)
    root = tree.getroot()
        
    for words in generate_annotated_sentences(root):
        print('\n')
        print(words)
    
    
    
    
            
    
    
            
        