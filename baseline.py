#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: jyao
Go over all n-grams up to length k (say 5) in a text, check which of these n-grams appear in the p(e|m) dictionary. 
For each mention that appears, take the top scored entity e based on p(e|m) value, 
and check its wikipedia page to see if it contains a DrugBank id. 
If it does, link it, otherwise do not link it
"""

from collections import Counter
from operator import itemgetter

import pywikibot
import nltk

def generate_ngrams(input_list, nums=2):
    """
    Generate n-grams from input_list
    Args:
        input_list: list of strings
        nums: if single int, only generate n-gram, by default 2-gram; if a list of int, generate grams specified by the list
    
    Return:
        list of list of ngrams as tuple
        
    Example:
        >>> a = ngrams('this is an exmaple'.split(), range(4))
        >>> a
        [[('this',), ('is',), ('an',), ('exmaple',)],
         [('this', 'is'), ('is', 'an'), ('an', 'exmaple')],
         [('this', 'is', 'an'), ('is', 'an', 'exmaple')]]
        
    """
    if type(nums) == int:
        nums = [nums]
    res = []
    for n in nums:
        if n > 0:
            res.append(list(zip(*(input_list[i:] for i in range(n)))))
    return res

def parse_pem(data_path='../data/crosswikis_wikipedia_p_e_m.txt', verbose=False):
    """
    Example:
        broncho	2	308453,1,Bronchiole	308449,1,Bronchus	
        Georgiana Molloy	9	2123300,9,Georgiana_Molloy
    Note:
        entities are sorted in descending order of frequency
    """
    pem = {} # p(e|m)
    e_map = {} # mapping entity to int id
    with open(data_path, 'r') as f:
        for i, line in enumerate(f, 1):
            if i % 500000 == 0:
                print('parsing {} lines'.format(i))
            mention, total_freq, *entities = line.strip().split('\t')
            unpacked_entities = (entity.split(',') for entity in entities)
            unpacked_entities = ((int(entity[0]), int(entity[1]), entity[2]) for entity in unpacked_entities)
            _counter = Counter()
            for idx, freq, name in unpacked_entities:
                # sanity check: if entity id is unique
                if verbose and name in e_map and e_map[name] != idx:
                     print('when dealing with {}, entity {} has non-unique idx: {} vs {}'.format(mention, name, e_map[name], idx))
                else:
                    e_map[name] = idx
                if name not in _counter:
                    _counter[name] = freq
                else:
                    _counter[name] += freq
            if mention not in pem:
                pem[mention] = _counter
            else:
                pem[mention] += _counter
    # cast Counter first to dict, then cast to list, then sort in descending order of frequency
    pem = {k:sorted(list(dict(v).items()), key=itemgetter(1), reverse=True) for k, v in pem.items()}
    return pem

if __name__ == '__main__':
    # configure
    site = pywikibot.Site('en', 'wikipedia')
    data_path = '../data/crosswikis_wikipedia_p_e_m.txt'
    text = "In a placebo-controlled trial in normal volunteers, the administration of a single 1 mg dose of doxazosin on day 1 of a four-day regimen of oral cimetidine (400 mg twice daily) resulted in a 10% increase in mean AUC of doxazosin (p=0.006), and a slight but not statistically significant increase in mean Cmax and mean half-life of doxazosin."
#    pem = parse_pem(data_path)
    nums = range(6)
    text = nltk.word_tokenize(text)
    all_ngrams = generate_ngrams(text, nums=nums)
    for single_ngrams in all_ngrams:
        for ngram in single_ngrams:
            ngram = '_'.join(ngram)
            if ngram in pem:
                top_entity, _ = pem[ngram][0]
                title = top_entity.replace('_', ' ')
                page = pywikibot.Page(site, title)
                print('looking for {}'.format(ngram))
                if 'DrugBank' in page.text:
                    print('find drug {}'.format(title))
    


