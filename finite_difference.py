import numpy as np
from scipy.linalg import solve

def cn_call_price(S0, K, T, r, sigma, N=200, M=1000):
    s_max = 3*K
    dS = s_max/N
    dt = T/M

    #grid and expiry condition
    S = np.linspace(0, s_max, N+1)
    V = np.maximum(S - K, 0)

    #interior indicies
    i = np.arange(1, N)

    #vectors
    alpha = 0.25 * dt * (sigma**2 * i**2 - r * i)
    beta = -0.5 * dt * (sigma**2 * i**2 + r)
    gamma = 0.25 * dt * (sigma**2 * i**2 + r * i)

    # precompute boundary values for all timesteps
    t_values = np.linspace(0, T, M+1)
    upper_bc = s_max - K * np.exp(-r * (T - t_values))

    # matrices
    A = np.diag(1 - beta) + np.diag(-alpha[1:], -1) + np.diag(-gamma[:-1], 1)
    B = np.diag(1 + beta) + np.diag(alpha[1:], -1)  + np.diag(gamma[:-1], 1)

     # time march backwards
    for j in range(M-1, -1, -1):
        rhs = B @ V[1:N]
        rhs[0]  += alpha[0]  * (upper_bc[j] + upper_bc[j+1]) 
        rhs[-1] += gamma[-1] * (upper_bc[j] + upper_bc[j+1])
        V[1:N] = solve(A, rhs)
        V[N] = upper_bc[j]

    price = np.interp(S0, S, V)
    return price, V, S, dS, S0

price, V, S, dS, S0 = cn_call_price(100, 105, 1, 0.05, 0.2, 200, 1000)

#print("price", price)
#print(S)