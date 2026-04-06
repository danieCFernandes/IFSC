import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import komm

st.header("Parte 2: Exercício 4")

Rs  = 50e3              # Taxa de símbolos          [baud]
Ts  = 1 / Rs            # Intervalo de símbolos     [s]
sps = 100               # Amostras / símbolo        [samples/symbol]
dt  = Ts / sps          # Passo de simulação        [s]
A   = np.sqrt(1 / Ts)   # Amplitude do pulso        [sqrt(Hz)]
N0      = 1e-2


pulse   = komm.RectangularPulse()
p_t     = A*pulse.taps(sps) # pulso de TX
q_t     = np.flip(p_t)      # puslo de RX
awgn    = komm.GaussianChannel(noise_power=N0/2 / dt)

u_n = np.array([-1.0, +1.0, +1.0, -3.0])    # Sequência de entrada
u_t = komm.sampling_rate_expand(u_n, factor=sps) / dt
x_t = komm.convolve(p_t, u_t) * dt
y_t = awgn.transmit(x_t)   # Ausência de ruído
v_t = komm.convolve(y_t, q_t) * dt  # Sinal na saída do filtro casado
v_n = komm.sampling_rate_compress(v_t, factor=sps)


tabs = st.tabs([ "Sinal PAM $x(t)$", "Pulso equivalente $h(t)$", "Sinal $v(t)$"])

with tabs[0]:
    fig, ax = plt.subplots(figsize = (6,3))
    ts = np.arange(x_t.size) * dt
    ax.plot(ts/1e-6, y_t / A, "C3", label="y(t) / A") 
    ax.plot(ts/1e-6, x_t / A, "C0", label="x(t) / A")
    ax.set_xlabel("$t$ [µs]")
    ax.set_ylabel("$X(t) / A$ [V]")
    ax.set_ylim(-5.5, 5.5)
    ax.legend()
    ax.grid()
    st.pyplot(fig)

with tabs[1]:
    h_t = komm.convolve(p_t, q_t) * dt
    fig, ax = plt.subplots(figsize = (6,3))
    ts = np.arange(h_t.size) * dt
    ax.plot(ts/1e-6, h_t)
    ax.set_xlabel("$t$ [µs]")
    ax.set_ylabel("$h(t)$")
    ax.grid()
    st.pyplot(fig)

with tabs[2]:
    h_t = komm.convolve(p_t, q_t) * dt
    fig, ax = plt.subplots(figsize = (6,3))
    ts = np.arange(v_t.size) * dt
    ts0 = np.arange(v_n.size) * Ts
    ax.plot(ts/1e-6, v_t, 'C2-', label="$v(t)$")
    ax.plot(ts0/1e-6, v_n, 'C2o', label="$v[n]$")
    ax.set_xlabel("$t$ [µs]")
    ax.set_ylabel("$v(t)$ [V]")
    ax.legend()
    ax.grid()
    st.pyplot(fig)
