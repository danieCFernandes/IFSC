import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import komm

rng = np.random.default_rng(seed=6)

st.header("Parte 2: Exercício 2")

# Variáveis

Rs      =  50e3        # Taxa   de   símbolos   [baud]
Ts      =  1 / Rs      # Intervalo   de   símbolos [s] 
sps     =  100         # Amostras      por     símbolo
dt      =  Ts / sps    # Passo de tempo "contínuo" [s]
A       =  10.0        # Amplitudo   de    p(t)    [v]
Ns      =  100         # Número de símbolos de entrada
n_iters =  1000        # Número     de     realizações
dur     =  Ns * Ts     # Duração    do   sinal    x(t)

pulse = komm.RectangularPulse() # Retangular NRZ

psd_teo = lambda f: 5 * A**2 * Ts * np.sinc(Ts* f)**2
## psd_sim = 

# Entrada
u_n = rng.choice([-3, -1, 1, 3], size=(n_iters, Ns))

# Geração do sinal PAM
u_t = komm.sampling_rate_expand(u_n, factor=sps) / dt
p_t = A * pulse.taps(sps)
x_t = np.array([np.convolve(p_t, u) * dt for u in u_t])

tabs = st.tabs(["Pulso", "Sinal PAM", "Densidade espectral de potência"])

with tabs[0]:
    ts = np.linspace(-10*Ts, 10*Ts, num=1000)
    fig, ax = plt.subplots(figsize = (6,3))
    ax.plot(ts / 1e-6, A * pulse.waveform(ts / Ts))
    ax.set_xlabel("$t$ [µs]")
    ax.set_ylabel("$p(t)$ [V]")
    ax.grid()
    st.pyplot(fig)
with tabs[1]:
    fig, ax = plt.subplots(figsize = (6,3))
    ts = np.arange(x_t[0].size) * dt
    ax.plot(ts/1e-6, x_t[0])
    ax.set_xlabel("$t$ [µs]")
    ax.set_ylabel("$X(t)$ [V]")
    ax.grid()
    st.pyplot(fig)
with tabs[2]:
    X_f, f = komm.fourier_transform(x_t, time_step=dt)
    psd_sim = (1/dur) * np.mean(np.abs(X_f)**2, axis=0)
    fig, ax = plt.subplots(figsize = (6,3))
    ax.plot(f / 1e3, psd_sim, "C1", label="Simulada")
    ax.plot(f / 1e3, psd_teo(f), "C0--", label="Teórica")
    ax.set_xlabel("$f$ [kHz]")
    ax.set_ylabel("$S_x(f)$ [W/Hz]")
    ax.set_xlim(-4*Rs/1e3, 4*Rs/1e3)
    ax.grid()
    st.pyplot(fig)

    