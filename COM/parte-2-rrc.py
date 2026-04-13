import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import komm

st.header("Parte 2: Root-raised-cosine")

rng = np.random.default_rng(seed=6)
komm.global_rng.set(rng)
# Parâmetros
Rs = 1.0        # Taxa de símbolos [baud]
Ts = 1 / Rs     # Intervalo de símbolos
sps = 50        # Amostras por símbolo
dt = Ts / sps   # Passo de simulação

α = st.slider(label="Fator de rollof $α$:", min_value=0.0, max_value=1.0, value=0.5, step=0.01) 
N0 = st.select_slider(label="Densidade espectral de potência do ruído $N_0$:", options=[0, 0.01, 0.1, 1.0])
pulse = komm.RootRaisedCosinePulse(rolloff=α)
awgn = komm.GaussianChannel(noise_power=N0/2 / dt)


u_n = rng.choice([-3, -1, 1, 3], size=400)
u_t = komm.sampling_rate_expand(u_n, factor=sps) / dt
p_t = pulse.taps(samples_per_symbol=sps, span=(-16, 16))
x_t = komm.convolve(p_t, u_t) * dt
y_t = awgn.transmit(x_t)
q_t = np.flip(p_t)
v_t = komm.convolve(q_t, y_t) * dt 
v_n = komm.sampling_rate_compress(v_t, factor=sps)

tabs = st.tabs(["Pulso", "Sinal PAM", "Saída do filtro casado"])

with tabs[0]:
    fig, ax = plt.subplots(1, 2, figsize = (6,3))

    ts = np.linspace(-16*Ts, 16*Ts, num=1000)
    ax[0].plot(ts, pulse.waveform(ts / Ts), label="$p(t)$")
    ax[0].set_xlabel("$t$")
    ax[0].set_ylim(-0.5, 1.5)
    ax[0].legend()
    ax[0].grid()

    fs = np.linspace(-1.5*Rs, 1.5*Rs, num=1000)
    ax[1].plot(fs, np.abs(pulse.spectrum(fs / Rs)), label="$P(f)$")
    ax[1].set_xlabel("$f$")
    ax[1].set_ylim(-0.1, 1.1)
    ax[1].legend(loc="upper right")
    ax[1].grid()
    
    st.pyplot(fig)

with tabs[1]:
    ts = np.arange(x_t.size) * dt
    values = st.slider(
        label="Select a range of values",
        min_value=ts[0],
        max_value=ts[-1],
        value=(25.0, 75.0)
    )

    fig, ax = plt.subplots(1, 1, figsize = (6,3))
    ax.plot(ts, y_t, "C1", label="$y(t)$")
    ax.plot(ts, x_t, "C0", label="$x(t)$")

    ax.set_xlabel("$t$")
    ax.set_xlim(values)
    ax.set_ylim(-6, 6)
    ax.legend()
    ax.grid()

    st.pyplot(fig)

with tabs[2]:
    ts = np.arange(v_t.size) * dt
    values = st.slider(
        label="Select a range of values",
        min_value=ts[0],
        max_value=ts[-1],
        value=(25.0, 75.0),
        key=6
    )

    fig, ax = plt.subplots(1, 1, figsize = (6,3))
    ax.plot(ts, v_t, "C2", label="$v(t)$")
    ts = np.arange(v_t.size) * dt
    ts0 = np.arange(v_n.size) * Ts
    ax.plot(ts, v_t, 'C2-', label="$v(t)$")
    ax.plot(ts0, v_n, 'C2o', label="$v[n]$")
    ax.set_xlabel("$t$ [s]")
    ax.set_xlabel("$t$")
    
    ax.set_xlim(values)
    ax.set_ylim(-6, 6)
    ax.legend()
    ax.grid()

    st.pyplot(fig)
