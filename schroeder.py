import numpy as np

def schroeder(ir, t, C, rms):
    """ Smooths a curve (ir) using Schroeder Integration method. "t" and "C" are Lundeby's compensation arguments,
    rms is Chu's compensation argument """
    a = len(ir[int(t):len(ir)])
    ir = ir[0:int(t)]
    # ir = ir ** 2
    y = np.flip((np.cumsum(np.flip(ir - rms)) + C) / (np.sum(ir - rms) + C))
    x = np.pad(y, (0,a))
    return x
