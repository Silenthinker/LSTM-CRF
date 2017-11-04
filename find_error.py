#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import utils

filename = '../data/drugddi2011/pred.ddi'
with open(filename, 'r') as f:
    pred = utils.labelseq2conll(f.readlines())

filename = '../data/drugddi2011/test.ddi'
with open(filename, 'r') as f:
    gold = utils.iob2etype(f.readlines())
utils.find_error(gold, pred, '../data/drugddi2011/error.txt')