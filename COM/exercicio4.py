import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import komm

st.header("Exercício 4")
cols = st.columns(2)

D = 2  # Duração do sinal [s]
with cols[0]:
    fa = st.slider(label="Taxa de amostragem $f_a$", min_value = 1e3, max_value=20e3, step=500.0,value=8e3, format="%g amostras/s")  # Taxa de amostragem
Ta = 1 / fa
with cols[1]:   
    L = st.select_slider(label="Número de níveis de quantização:", options=[2, 4, 8, 16, 32, 64, 128, 256], value=128)
Δ = 2 / L
dt = 1e-6

tabs = st.tabs(["Curva entrada x saída", "Sinais", "Erro", "Histograma","Dados"])

# Mensagem
ts = np.arange(0.0, D, step=dt)
x_t = np.sin(2*np.pi*50*ts)

x_n = komm.sampling_rate_compress(x_t, int(Ta / dt))
ns = np.arange(x_n.size)

quant = komm.UniformQuantizer.mid_riser(L, Δ)
y_n = quant.quantize(x_n)
d_n = quant.digitize(x_n)

k = int(np.log2(L))
labeling = komm.NaturalLabeling(k)
bits = labeling.indices_to_bits(d_n)

# SNR
Px = np.mean(x_n**2)
e_n = y_n - x_n
Pe = np.mean(e_n**2)
SNR_db = 10*np.log10(Px / Pe)
 
with tabs[0]:
    fig, ax = plt.subplots(figsize = (6,5))
    xs = np.linspace(-10, 10, num=1000)
    ys = quant.quantize(xs)
    ax.plot(xs, ys)
    ax.set_xlabel("$x [V]$")
    ax.set_ylabel("$y [V]$")


    ax.grid()
    st.pyplot(fig)


    pass
with tabs[1]:
    fig, ax = plt.subplots(figsize = (6,4))
    ax.plot(ts / 1e-3, x_t, "C0", label="$x(t)$")
    ax.plot((ns * Ta) / 1e-3, x_n, "C2o", label="$x[n]$")
    ax.plot((ns * Ta) / 1e-3, y_n, "C1o", label="$y[n]$")
    ax.set_xlabel("$t$ [ms]")
    ax.set_xlim(0, 50)
    ax.grid()
    ax.legend()
    st.pyplot(fig)
    pass

with tabs[2]:
    fig, ax = plt.subplots(figsize = (6,4))
    ax.plot((ns * Ta) / 1e-3, e_n, "C3o")
    ax.set_ylim(-0.6, 0.6)
    ax.set_xlim(0, 10)
    ax.grid()
    st.pyplot(fig)
    pass

with tabs[3]:
    fig, ax = plt.subplots(figsize = (6,4))
    ax.hist(e_n, bins=50, density=True)
    ax.set_xlim(-0.6, 0.6)
    st.pyplot(fig)
    pass

with tabs[4]:
    st.write(f"Número de bits/amostra $k = {k}$")
    st.write(f"Tamanho: {bits.size} bits")
    st.write(f"Tamanho: {bits.size / 8000} kB")
    st.write(f"Potência do sinal:$P_x = {Px}$")
    st.write(f"Potência do erro:$P_e = {Pe:.6f}$")
    st.write(f"Razão sinal--ruído: SNR = {SNR_db:.2f}")
    
    



