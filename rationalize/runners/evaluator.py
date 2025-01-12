# coding: utf-8


import torch
from torch.autograd import Variable

import numpy as np
from runners.metrics import precision, recall, f1, accuracy, percentage


def evaluate(model, data, args, set_name):
    
    model.eval()  # Set model to eval mode.

    # Initialize records.
    metric_funcs = {"precision": precision, "recall": recall, "f1": f1, "accuracy": accuracy, "percentage": percentage}
    y_history = {"true": [], "pred": []}
    r_history = {"precision": [], "recall": [], "f1": [], "accuracy": [], "percentage": []}

    instance_count = data.data_sets[set_name].size()
    for start in range(instance_count // args.batch_size + 1):

        # Get a batch.
        batch_idx = range(start * args.batch_size,
                          min((start + 1) * args.batch_size, instance_count))
        samples = data.get_batch(set_name, batch_idx=batch_idx, sort=True)
        x, y, m, r, s, d = samples

        # Save values to torch tensors.
        x = Variable(torch.from_numpy(x))
        y = Variable(torch.from_numpy(y))
        m = Variable(torch.from_numpy(m)).float()
        r = Variable(torch.from_numpy(r)).float()
        s = Variable(torch.from_numpy(s)).float()
        d = Variable(torch.from_numpy(d)).float()
        if args.cuda:
            x = x.cuda()
            y = y.cuda()
            m = m.cuda()
            r = r.cuda()
            s = s.cuda()
            d = d.cuda()

        # Get predictions and rationales.
        predict, _, r_pred, _, _ = model(x, m)
        _, y_pred = torch.max(predict, dim=1)

        # Extend predictions y to history.
        y_history["true"].extend(y.tolist())
        y_history["pred"].extend(y_pred.tolist())

        if not bool(args.rationale_binary):
            r_pred = (r_pred > args.binarize_threshold).float()

        # Extend metrics of rationale r to history.
        for a_r, a_r_pred, a_m in zip(r, r_pred, m):
            for metric_name, metric_func in metric_funcs.items():
                metric_vals = metric_func(a_r.tolist(), a_r_pred.tolist(), mask=a_m.tolist(), average="binary")
                r_history[metric_name].append(metric_vals)

    # Get metrics for predictions y and rationales r.
    y_metrics = {}
    r_metrics = {}
    for metric_name, metric_func in metric_funcs.items():
        metric_vals = metric_func(y_history["true"], y_history["pred"], average="macro")
        y_metrics[metric_name] = metric_vals
        r_metrics[metric_name] = np.nanmean(r_history[metric_name])

    return {"prediction": y_metrics, "rationale": r_metrics}
