import numpy as np
from scipy.stats import norm

#function for computing d variables
def compute_d1(S, K, T, r, sigma):
    if S <= 0:
        return -np.inf
    return((np.log(S/K) + (r + 0.5*sigma**2)*T)/(sigma*(T)**0.5))

def compute_d2(d1, sigma, T):
    return(d1-sigma*(T)**0.5) 
#test block
#d1 = compute_d1(100, 105, 1, 0.05, 0.2)
#d2 = compute_d2(d1, 1, 1)
#print(d1, d2)

def call_price(S, K, T, r, sigma):
    d1 = compute_d1(S, K , T, r, sigma)
    d2 = compute_d2(d1, sigma, T)
    return (S*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2))
def put_price(S, K, T, r, sigma):
    d1 = compute_d1(S, K , T, r, sigma)
    d2 = compute_d2(d1, sigma, T)
    return (K*np.exp(-r*T)*norm.cdf(-d2)-S*norm.cdf(-d1))

#test block
#Call = call_price(100, 105, 1, 0.05, 0.2)
#print(Call)
#Put = put_price(100, 105, 1, 0.05, 0.2)
#print(Put)

#put-call parity check
def parity_check(S, K, T, r, sigma):
    Call = call_price(S, K, T, r, sigma)
    return (Call - S + K*np.exp(-r*T))
#parity = parity_check(100, 105, 1, 0.05, 0.2)
# print(f"Parity Check: {parity:.6f}, Put:{Put:.6f}")
# print("Nd1", norm.cdf(d1))