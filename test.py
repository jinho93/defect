import numpy as np

"""
Model for the defect charge distribution
q (r) = q [x exp(-r/gamma) + (1-x) exp(-r^2/beta^2)]
"""

q = float(input("charge value:  "))

class PC(object):

    def __init__(self):
        self.gamma = 1.0
        self.beta = 1.0
        self.q = None
        self.x = 0.0

    def q_model(self, g):

        return(self.x / np.sqrt(1+self.gamma * self.gamma * g*g)
               + (1 - self.x) * np.exp(-0.25*self.beta*self.beta*g*g))






