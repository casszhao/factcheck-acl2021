# coding: utf-8


import torch
from torch.autograd import Variable

import numpy as np
from runner.metrics import get_batch_accuracy, get_batch_sparsity, get_batch_continuity


def evaluate(model, data, args, set_name):
    
    model.eval()  # Set model to eval mode.

    # Initialize records.
    accs = []
    anti_accs = []
    sparsities = []
    continuities = []

    instance_count = data.data_sets[set_name].size()
    for start in range(instance_count // args.batch_size):

        # Get a batch.
        batch_idx=range(start * args.batch_size, (start + 1) * args.batch_size)
        x_mat, y_vec, x_mask = data.get_batch(set_name, batch_idx=batch_idx, sort=True)

        # Save values to torch tensors.
        batch_x_ = Variable(torch.from_numpy(x_mat))
        batch_m_ = Variable(torch.from_numpy(x_mask)).type(torch.FloatTensor)
        batch_y_ = Variable(torch.from_numpy(y_vec))
        if args.cuda:
            batch_x_ = batch_x_.cuda()
            batch_m_ = batch_m_.cuda()
            batch_y_ = batch_y_.cuda()

        # Get predictions.
        predict, anti_predict, z, neg_log_probs = model(batch_x_, batch_m_)

        # Evaluate classification accuracy.
        _, y_pred = torch.max(predict, dim=1)
        _, anti_y_pred = torch.max(anti_predict, dim=1)
        accs.append(get_batch_accuracy(y_pred, batch_y_))
        anti_accs.append(get_batch_accuracy(anti_y_pred, batch_y_))
        
        # Evaluate sparsity and continuity measures..
        sparsities.append(get_batch_sparsity(z, batch_m_))
        continuities.append(get_batch_continuity(z, batch_m_))

    # Average.
    acc = np.mean(accs)
    anti_acc = np.mean(anti_accs)
    sparsity = np.mean(sparsities)
    continuity = np.mean(continuities)
    print(set_name, "acc:", acc, "anti acc:", anti_acc, "sparsity:", sparsity, "continuity:", continuity)
    return acc, anti_acc, sparsity, continuity