import numpy as np
import matplotlib.pyplot as plt
from finite_difference import cn_call_price
from black_scholes import call_price

def Stock_Plot(S0, K, T, r, sigma):
    price, V, S, dS, S0 = cn_call_price(100, 105, 1, 0.05, 0.2, 500, 2000)
    bs_price = [call_price(s, 105, 1, 0.05, 0.2) for s in S]
    fd_at_S0 = np.interp(S0, S, V)
    bs_at_S0 = call_price(S0, K, T, r, sigma)

    plt.subplot(2, 3, 1)
    plt.plot(S, V)
    plt.plot(S, bs_price, color = 'g')
    plt.title("European Call Option Price — FD vs Black-Scholes")
    plt.xlabel("Stock Price")
    plt.ylabel("Option Price")
    plt.legend(["Finite Difference", "Black-Scholes"])
    plt.plot(S0, fd_at_S0, 'o', color='blue', markersize=8)
    plt.annotate(f'FD: {fd_at_S0:.3f}\nBS: {bs_at_S0:.3f}', 
             xy=(S0, fd_at_S0),           # point to annotate
             xytext=(S0+5, fd_at_S0-3),   # where the text sits
             fontsize=9,
             arrowprops=dict(arrowstyle='->', color='black'))
    plt.xlim(60, 120)
    plt.ylim(-2, 25)
    Delta_vec = (V[2:] - V[:-2]) / (2 * dS)   # centered difference across all points
    Gamma_vec = (V[2:] - 2*V[1:-1] + V[:-2]) / (dS**2)
    mask = S[1:-1] > 10
    gamma_peak_value = np.max(Gamma_vec[mask])
    gamma_peak_S = S[1:-1][mask][np.argmax(Gamma_vec[mask])]
    
    plt.subplot(2, 3, 2)
    plt.plot(S[1:-1], Delta_vec, label='Delta')
    plt.title("Delta Plot vs Stock Price")
    plt.xlabel("Stock Price")
    plt.ylabel("Delta")
    plt.xlim(60, 150)
    plt.ylim(0, 1)
    plt.axhline(y=0.5, color='red', linestyle='--', label='Delta=0.5 (At The Money Reference)')
    plt.legend()
    
    plt.subplot(2, 3, 3)
    plt.plot(S[1:-1], Gamma_vec, label='Gamma')
    plt.title("Gamma Plot vs Stock Price")
    plt.xlabel("Stock Price")
    plt.ylabel("Gamma")
    plt.xlim(60, 150)
    plt.ylim(0, 0.04)
    plt.axvline(x=100, color='red', linestyle='--', label='K = 105 (Strike Price Reference)')
    plt.legend()
    plt.annotate(f'Peak: {gamma_peak_value:.4f}\nat S={gamma_peak_S:.1f}',
             xy=(gamma_peak_S, gamma_peak_value),
             xytext=(gamma_peak_S + 10, gamma_peak_value-.002),
             fontsize=9,
             arrowprops=dict(arrowstyle='->', color='black'))
    return gamma_peak_value



