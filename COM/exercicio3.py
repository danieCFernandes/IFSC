import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import komm

st.header("Exercício 3")

fa = 8.0
Ta = 1 / fa
L = 8 
Δ = 2.0
dt = 1e-3

# Mensagem
ts = np.arange(0.0, 0.1, step=dt)
x_t = 5.0 * np.sin(2*np.pi*ts)

quant = komm.UniformQuantizer.mid_riser(L, Δ)

tabs = st.tabs(["Curva entrada x saída", "Sinais", "Tabela"])

with tabs[0]:
    fig, ax = plt.subplots(figsize = (6,5))
    xs = np.linspace(-10, 10, num=1000)
    ys = quant.quantize(xs)
    ax.plot(xs, ys)
    ax.set_xlabel("$x [V]$")
    ax.set_ylabel("$y [V]$")
    ax.set_xticks(quant.thresholds)
    ax.set_yticks(quant.levels)

    ax.grid()
    st.pyplot(fig)


    pass
with tabs[1]:
    pass
with tabs[2]:
    pass
