from matplotlib import pyplot as plt
from spherical_resonator import SphericalResonator
from scipy.optimize import curve_fit
from scipy.special import sph_harm
import numpy as np


resonator = SphericalResonator()

# Define angular grid
theta = np.linspace(0, 2 * np.pi, 200)       # polar angle
phi = np.linspace(0, 2*np.pi, 200)       # azimuthal angle
phi_grid, theta_grid = np.meshgrid(phi, theta)

def spherical_harmonic_proj(m, l, theta):
    amp_theta = np.sqrt(np.mean(sph_harm(m, l, phi_grid, theta) ** 2, axis=1))
    amp_theta /= amp_theta.max()
    return amp_theta

def fit_eqn(theta):
    pass

plt.scatter(resonator.angular_position, resonator.amplitude, linewidths=0.1, label="Data")
plt.plot(theta * 180 / np.pi, 7 * spherical_harmonic_proj(0, 2, theta_grid), color="red", label=r"$Y_{2}^0$")
plt.xlabel(r'Angular Position ($^\circ$)')
plt.ylabel('Amplitude (V)')
plt.title('Spherical Resonator - Angular Sweep @ 4970 Hz')
plt.legend().set_loc("upper right")
plt.show()
