#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import utils

import numpy as np

import torch
import torch.autograd as autograd
import torch.nn as nn
import torch.optim as optim

from LSTM_CRF import prepare_sequence, BiLSTM_CRF


START_TAG = "<START>"
STOP_TAG = "<STOP>"
EMBEDDING_DIM = 100
HIDDEN_DIM = 100


data_path = '../data/DrugDDI/ddi.txt'
dataset = utils.load_data(data_path)

train_data = dataset
test_data = dataset

# create dictionary
word_to_ix = {}
for sentence, tags in train_data:
    for word in sentence:
        if word not in word_to_ix:
            word_to_ix[word] = len(word_to_ix)

tag_to_ix = {"B-DRUG": 0, "I-DRUG": 1, "O": 2, START_TAG: 3, STOP_TAG: 4}

model = BiLSTM_CRF(len(word_to_ix), tag_to_ix, EMBEDDING_DIM, HIDDEN_DIM)
optimizer = optim.SGD(model.parameters(), lr=0.01, weight_decay=1e-4)

# Check predictions before training
precheck_sent = prepare_sequence(train_data[0][0], word_to_ix)
precheck_tags = torch.LongTensor([tag_to_ix[t] for t in train_data[0][1]])
print(model(precheck_sent))

# Make sure prepare_sequence from earlier in the LSTM section is loaded
for epoch in range(5):  # again, normally you would NOT do 300 epochs, it is toy data
    for i, (sentence, tags) in enumerate(train_data, 1):
        # Step 1. Remember that Pytorch accumulates gradients.
        # We need to clear them out before each instance
        model.zero_grad()

        # Step 2. Get our inputs ready for the network, that is,
        # turn them into Variables of word indices.
        sentence_in = prepare_sequence(sentence, word_to_ix)
        targets = torch.LongTensor([tag_to_ix[t] for t in tags])

        # Step 3. Run our forward pass.
        neg_log_likelihood = model.neg_log_likelihood(sentence_in, targets)

        # Step 4. Compute the loss, gradients, and update the parameters by
        # calling optimizer.step()
        neg_log_likelihood.backward()
        optimizer.step()
        
        if i % 200 == 0:
            print('Trained {}/{} data points'.format(i, len(train_data)))
        
    # Check predictions after training
    n_entities = 0
    n_correct = 0
    for i, (sentence, tags) in enumerate(test_data):
        precheck_sent = prepare_sequence(sentence, word_to_ix)
        y = np.array([tag_to_ix[i] for i in tags])
        _, y_pred = model(precheck_sent)
        y_pred = np.array(y_pred)
        is_entity = y == tag_to_ix['B-DRUG']
        is_correct = y == y_pred
        n_entities += np.sum(is_entity)
        n_correct += np.sum(is_entity * is_correct)
    print('Precision: {}'.format(n_correct / n_entities))        
        
        
        

