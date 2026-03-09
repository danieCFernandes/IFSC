import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import komm

st.header("Exercício 2")

dt = 1e-6
t = np.arange(-0.1, 0.1, step=dt)
fa = st.slider(label="Taxa de amostragem $f_a$", min_value=50, max_value=400, step=10)
Ta = 1/fa
st.write(f"Intervalo de amostragem: $Ta = {1000 * Ta: .2f}$ ms")
ti = -0.1
tf =  0.1

# Mensagem
x_t = 2 + 600*np.sinc(200*t) + 8*np.cos(2*np.pi*50*t)

# Amostragem
x_n = komm.sampling_rate_compress(x_t, int(Ta / dt))
ns = np.arange(0, x_n.size, step=1)

# Reconstrução

x_hat_t = np.zeros_like(x_t)
for n in ns:
    x_hat_t += x_n[n] * np.sinc((t - n*Ta - ti) / Ta)


fig, ax = plt.subplots(figsize = (6,3))
ax.plot(t / 1e-3, x_t, "C0", label="$x(t)$")
ax.plot((ns*Ta - 0.1) / 1e-3, x_n, "C2o")
ax.plot(t / 1e-3, x_hat_t, "C1", label="$\\hat{x}(t)")

ax.set_xlabel("$t$ [ms]")
ax.grid()
ax.legend()
st.pyplot(fig)