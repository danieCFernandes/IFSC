import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import komm

st.header("Quantização baseada em PDF")

def uniform(x):
    return (0.5 / np.sqrt(3)) * (-np.sqrt(3)<= x) * (x <= np.sqrt(3))

def gaussian(x,  mu=0, std=1):
    return 1/np.sqrt(2*np.pi*std**2) * np.exp(-(x - mu)**2 / (2*std**2))

def laplacian(x):
    b = 1/np.sqrt(2)
    return 0.5 / b * np.exp(-np.abs(x) / b)

def gaussian_mixture(x):
    return 0.25 * gaussian(x, mu=-3, std=0.5) + 0.75 * gaussian(x, mu=2, std=0.8)

pdf_options = {
    "Uniform" : uniform,
    "Gausian" : gaussian,
    "Laplacian": laplacian,
    "Gaussian mixture": gaussian_mixture,
}
pdf_radio = st.radio(label="PDF $f_x(x)$", options = pdf_options, horizontal=True)
pdf = pdf_options[pdf_radio]

tabs = st.tabs(["Quantização uniforme", "Quantização não-uniforme"])

with tabs[0]:
    xs = np.linspace(-10, 10, num=100_000)
    fig, ax = plt.subplots(figsize = (6,5))
    ax.plot(pdf(xs))
    ax.grid()
    ax.set_xlabel("$x$")
    ax.set_ylabel("$f_x(x)$")
    st.pyplot(fig)
    pass
with tabs[1]:

    pass