import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import solve
from black_scholes import call_price, put_price
from finite_difference import cn_call_price
from greeks import calc_Delta, calc_Gamma
from visualize import Stock_Plot

#defining stock paramters
S0 = 100
K = 105
T = 1
r = 0.05
sigma = 0.2



#black scholes price calculation from known solutions
call_price_bs = call_price(S0, K, T, r, sigma)
put_price_bs = put_price(S0, K, T, r, sigma)
print("Black-Scholes call price:", call_price_bs)
print("Black-Scholes put price:", put_price_bs)

#call price from finite difference method
price, V, S, dS, S0 = cn_call_price(S0, K, T, r, sigma)
call_price_cn = price
difference = call_price_bs-call_price_cn
print("Finite Difference call price:", call_price_cn)
print("Call Price difference", difference )

#greeks from finite difference
idx = np.argmin(np.abs(S-S0))
Delta = calc_Delta(V, idx, dS)
Gamma = calc_Gamma(V, idx, dS)
print("Delta:", Delta)
print("Gamma", Gamma)

#plot visualizations
plot = Stock_Plot(S0, K, T, r, sigma)

#convergence analysis

N_values  = [50, 100, 200, 400, 800]
errors = []
dS_array = []
for N in N_values:
    M = 4*N
    result = cn_call_price(S0, K, T, r, sigma, N=N, M=M)
    fd_price = result[0]
    dS_n = result[3]
    error = abs(fd_price - call_price_bs)
    errors.append(error)
    dS_array.append(dS_n)
plt.subplot(2, 3, 4)
plt.loglog(dS_array, errors)
plt.xlabel("dS (log scale)")
plt.ylabel("Error (log scale)")
plt.title("Spatial Convergence Analysis")
plt.grid(True, which="both")
s_slope = np.polyfit(np.log(dS_array), np.log(errors), 1)[0]
plt.text(0.3, 0.7, f'slope = {s_slope:.2f}', transform=plt.gca().transAxes)
dS_array_np = np.array(dS_array)
plt.loglog(dS_array_np, (dS_array_np**2) * (errors[0]/dS_array[0]**2), 
           'r--', label='slope 2 reference')
plt.legend()

# #temporal convergence
reference = cn_call_price(S0, K, T, r, sigma, N=2000, M=5000)[0]
M_values  = [50, 100, 200, 400, 800]
errors_t = []
dt_array = []
for M in M_values:
    N = 2000
    result = cn_call_price(S0, K, T, r, sigma, N=N, M=M)
    fd_price = result[0]
    dt_n = T/M
    error = abs(fd_price - reference)
    errors_t.append(error)
    dt_array.append(dt_n)
dt_array_np = np.array(dt_array)

plt.subplot(2, 3, 5)
plt.loglog(dt_array_np, errors_t, label='FD error')
plt.loglog(dt_array_np, (dt_array_np**2) * (errors_t[0]/dt_array[0]**2), 
           'r--', label='slope 2 reference')
t_slope = np.polyfit(np.log(dt_array_np), np.log(errors_t), 1)[0]
plt.text(0.3, 0.7, f'slope = {t_slope:.2f}', transform=plt.gca().transAxes)
plt.xlabel("dt (log scale)")
plt.ylabel("Error (log scale)")
plt.title("Temporal Convergence Analysis")
plt.grid(True, which="both")
plt.legend()

#parameter subplot
ax6 = plt.subplot(2, 3, 6)
ax6.axis('off')  # hide axes

params = [
    ['Parameter', 'Value'],
    ['Stock Price (S0)', f'{S0}'],
    ['Strike Price (K)', f'{K}'],
    ['Time to Expiry (T)', f'{T} yr'],
    ['Risk-free Rate (r)', f'{r*100}%'],
    ['Volatility (σ)', f'{sigma*100}%'],
    ['BS Call Price', f'{call_price_bs:.4f}'],
    ['FD Call Price', f'{fd_price:.4f}'],
    ['Δ', f'{Delta:.4f}'],
    ['Γ', f'{Gamma:.4f}'],
]

table = ax6.table(cellText=params[1:], 
                  colLabels=params[0],
                  loc='center',
                  cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.0, 1.0)
ax6.set_title('Simulation Parameters & Results', pad=20)

plt.show()


