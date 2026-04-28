import numpy as np
from finite_difference import cn_call_price

price, V, S, dS, S0 = cn_call_price(100, 105, 1, 0.05, 0.2, 500, 2000)

idx = np.argmin(np.abs(S-S0))

def calc_Delta(V, idx, dS):
    Delta = (V[idx+1] - V[idx-1]) / (2*dS)
    return Delta

def calc_Gamma(V, idx, dS):
    Gamma = (V[idx+1] - 2*V[idx] + V[idx-1])/(dS)**2
    return Gamma



# print("price", price)
# print("Delta", Delta)
# print("Gamma", Gamma)