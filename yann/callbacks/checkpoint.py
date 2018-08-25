from .base import Callback


class Checkpoint(Callback):
  def __init__(self, freq=1):
    self.freq = freq

  def on_epoch_end(self, epoch, loss=None, metrics=None, trainer=None):
    if epoch % self.freq == 0 :
      trainer.checkpoint()

