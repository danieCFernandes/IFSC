import komm
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

st.header("Parte 4 -- Exercício 5")

rng = np.random.default_rng(seed=6)
komm.global_rng.set(rng)

M  = 16                 # Ordem da constelação
k  = int(np.log2(M))    # Número de bits por símbolo
P  = 100e-3              # Potência recebida em W
N0 = 1e-9               # Densidade espectral de potência do ruído em W/Hz
Rb = 8.8667e6           # Taxa de bits em bps
Rs = Rb / k             # Taxa de símbolos em baud
Es = P / Rs             # Energia por símbolo em J
Eb = Es / k             # Energia por bit em J
EbNo_dB = 10 * np.log10(Eb / N0)  # Relação Eb/No em dB
Ps = 3 * komm.gaussian_q(np.sqrt(Es / (5 * N0)))  # Probabilidade de símbolo em erro
Pb_teo = Ps / k         # Probabilidade de bit em erro teórica
Δ = np.sqrt((6*Es) / (M - 1))  # Distância entre os pontos da constelação

# Simulação
N_bits = 100_000
source = komm.DiscreteMemorylessSource(2)  # Fonte binária equiprovável
const  = komm.QAMConstellation(M)  # Constelação QAM
labeling = komm.ReflectedRectangularLabeling(k)  # Rotulagem refletida retangula
awgn = komm.GaussianChannel(noise_power=N0)  # Canal AWGN
b = source.emit(N_bits)  # Gerar bits
m = labeling.bits_to_indices(b)  # Mapear bits para índices de símbolos
u = const.indices_to_symbols(m)  # Mapear índices para símbolos
v = awgn.transmit(u)  # Transmitir símbolos pelo canal
m_hat = const.closest_indices(v)  # Decodificar símbolos recebidos para índices
b_hat = labeling.indices_to_bits(m_hat)  # Mapear índices decodificados para bits
Pb_sim = np.mean(b != b_hat)  # Probabilidade de bit em erro simulada
print(EbNo_dB, Pb_teo, Pb_sim)
cols = st.columns(3)
with cols[0]:
    st.metric(label="SNR de bit $E_b/N_0$ (dB)", value=f"{EbNo_dB:.2f} dB")
with cols[1]:
    st.metric(label="BER teórica $P_b$", value=f"{Pb_teo:.3%}")
with cols[2]:
    st.metric(label="BER simulada $P_b$", value=f"{Pb_sim:.3%}")

# Plot
fig, ax = plt.subplots()

ax.plot(v.real/Δ, v.imag/Δ, 'C1.')
ax.plot(const.matrix.real/Δ, const.matrix.imag/Δ, 'C0o')
ax.set_xlabel("Re")
ax.set_ylabel("Im")
ax.set_aspect("equal")
ax.grid()
st.pyplot(fig)
