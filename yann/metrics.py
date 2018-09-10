import torch
from yann import to_numpy
import numpy as np
from functools import partial
from collections import deque


def get_preds(scores):
  score, preds = torch.max(scores, dim=1)
  return preds


def top_k(scores, k=5, largest=True):
  return torch.topk(scores, k=k, dim=1, largest=largest)


def accuracy(targets, preds):
  if targets.shape != preds.shape:
    preds = get_preds(preds)
  return (targets == preds).sum().float() / len(preds)


def top_k_accuracy(targets, preds, k=1):
  if len(targets.shape) != 1:
    raise ValueError('Multi label targets not supported')
  scores, preds = preds.topk(k, 1, True, True)
  preds.t_()
  correct = (preds == targets.view(1, -1).expand_as(preds))

  return correct.sum().float() / len(targets)

top_3_accuracy = partial(top_k_accuracy, k=3)
top_5_accuracy = partial(top_k_accuracy, k=5)
top_10_accuracy = partial(top_k_accuracy, k=10)


def evaluate_multiclass(
    targets,
    outputs,
    preds=None,
    classes=None
):
  preds = preds or get_preds(outputs)
  targets, outputs, preds = (
    to_numpy(targets),
    to_numpy(outputs),
    to_numpy(preds)
  )






def evaluate_multilabel(
    targets,
    outputs,
    preds=None,
    classes=None,
):
  targets, outputs, preds = (
    to_numpy(targets),
    to_numpy(outputs),
    to_numpy(preds)
  )




class Meter:
  def __init__(self):
    self.reset()

  def reset(self):
    self.max = None
    self.min = None
    self.sum = 0
    self.count = 0

  def update(self, val):
    if self.max is None or val > self.max:
      self.max = val
    if self.min is None or val < self.min:
      self.min = val

    self.sum += val
    self.count += 1

  def average(self):
    return self.sum / self.count


class MovingAvgMeter:
  def __init__(self, window=10):
    self.queue = deque(maxlen=window)

  def update(self, val):
    self.queue.append(val)

  def value(self):
    if not self.queue: return None
    return sum(self.queue) / len(self.queue)


def exp_moving_avg(cur, prev=None, alpha=.05, steps=None):
  """exponential moving average"""
  if prev is None:
    return cur
  avg = alpha * cur + prev * (1 - alpha)
  return avg / (1 - alpha ** steps) if steps else avg


def moving_average(data, window=10):
  cumsum = np.cumsum(np.insert(data, 0, 0))
  return (cumsum[window:] - cumsum[:-window]) / float(window)