import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import komm

st.header("Parte 2: Root-raised-cosine")

rng = np.random.default_rng(seed=6)

# Parâmetros
Rs = 1.0        # Taxa de símbolos [baud]
Ts = 1 / Rs     # Intervalo de símbolos
sps = 50        # Amostras por símbolo
dt = Ts / sps   # Passo de simulação

α = st.slider(label="Fator de rollof $α$:", min_value=0.0, max_value=1.0, value=0.5, step=0.01) 

pulse = komm.RootRaisedCosinePulse(rolloff=α)

u_n = rng.choice([-3, -1, 1, 3], size=400)
u_t = komm.sampling_rate_expand(u_n, factor=sps) / dt
p_t = pulse.taps(samples_per_symbol=sps, span=(-16, 16))
x_t = komm.convolve(p_t, u_t) * dt

tabs = st.tabs(["Pulso", "Sinal PAM transmitido"])

with tabs[0]:
    fig, ax = plt.subplots(1, 2, figsize = (6,3))

    ts = np.linspace(-16*Ts, 16*Ts, num=1000)
    ax[0].plot(ts, pulse.waveform(ts / Ts), label="$p(t)$")
    ax[0].set_xlabel("$t$")
    ax[0].set_ylim(-0.5, 1.5)
    ax[0].legend()
    ax[0].grid()

    fs = np.linspace(-1.5*Rs, 1.5*Rs, num=1000)
    ax[1].plot(fs, pulse.spectrum(fs / Rs), label="$P(f)$")
    ax[1].set_xlabel("$f$")
    ax[1].set_ylim(-0.1, 1.1)
    ax[1].legend(loc="upper right")
    ax[1].grid()
    
    st.pyplot(fig)

with tabs[1]:
    values = st.slider(
        label="Select a range of values",
        min_value=ts[0],
        max_value=ts[-1],
        value=(25.0, 75.0)
    )

    fig, ax = plt.subplots(1, 1, figsize = (6,3))
    ts = np.arange(x_t.size) * dt
    ax.plot(ts, x_t, label="$x(t)$")
    ax.set_xlabel("$t$")
    ax.set_xlim(values)
    ax.set_ylim(-6, 6)
    ax.legend()
    ax.grid()

    st.pyplot(fig)
