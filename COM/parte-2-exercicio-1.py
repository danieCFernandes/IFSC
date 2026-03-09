import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import komm

st.header("Parte 2: Exercício 1")

# Variáveis

Rs   = 50e3     # Taxa de símbolos [baud]
Ts   = 1 / Rs   # Intervalo de símbolos [s] 
sps  = 100      # Amostras por símbolo
dt   = Ts / sps # Passo de tempo "contínuo" [s]
A    = 0.5      # Amplitudo de p(t) [v]


# Forma de onda de p(t)
def pulse_waveform(t):
    return ((t - 0.2) / 0.3 * ((0.2 <= t) & (t < 0.5)) + \
    (0.8 - t) / 0.3 * ((0.5 <= t) & (t < 0.8)))

def pulse_taps(sps):
    ts = np.arange(sps) / sps
    return pulse_waveform(ts)

# Entrada
u_n = np.array([0.4, -0.1, -0.5, 0.8, -0.2])

# Geração do sinal PAM
u_t = komm.sampling_rate_expand(u_n, factor=sps) / dt
p_t = A * pulse_taps(sps)
x_t = 10 * np.convolve(p_t, u_t) * dt

tabs = st.tabs(["Pulso", "Sinal PAM"])

with tabs[0]:
    ts = np.linspace(0, Ts, num=1000)
    fig, ax = plt.subplots(figsize = (6,3))
    ax.plot(ts / 1e-6, A * pulse_waveform(ts / Ts))
    ax.set_xlabel("$t$ [µs]")
    ax.set_ylabel("$p(t)$ [V]")
    ax.set_xticks(np.arange(0, 21, step=2))
    ax.grid()
    st.pyplot(fig)
    pass

with tabs[1]:
    fig, ax = plt.subplots(figsize = (6,3))
    ts = np.arange(x_t.size) * dt
    ax.plot(ts/1e-6, x_t)
    ax.set_xlabel("$t$ [µs]")
    ax.set_ylabel("$X(t)$ [V]")
    ax.grid()
    st.pyplot(fig)
    pass

