import numpy as np



q = float(input("charge value:  "))

class PC(object):
    """
    Model for the defect charge distribution
    q (r) = q [x exp(-r/gamma) + (1-x) exp(-r^2/beta^2)]
    """
    def __init__(self):
        self.gamma = 1.0
        self.beta = 1.0
        self.q = None
        self.x = 0.0

    def q_model(self, g):
        """
        In reciprocal space, the defect charge distribution is changed to (excluding
        the Fourier normalization constant)
        """
        return(self.x / np.sqrt(1+self.gamma * self.gamma * g*g)
               + (1 - self.x) * np.exp(-0.25*self.beta*self.beta*g*g))






