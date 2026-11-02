"""Compare the simulated horn with the classical pyramidal-horn design equations.

    python design_check.py

Dimensions are those of hfss/horn.aedt. The HFSS result used for comparison is the
peak GainTotal at 10 GHz (129.77 linear), read from figures/gain_3d.png.
"""
import math

c = 299_792_458.0
f = 10e9
lam = c / f * 1e3                     # wavelength in mm

a, b = 22.86, 10.16                   # WR-90 broad (y, H-plane) and narrow (x, E-plane) walls, mm
A, B = 148.0, 110.0                   # aperture: H-plane (y) and E-plane (x), mm
L = 190.0                             # flare length from waveguide to aperture (z = 30 ... 220 mm)
G_hfss = 129.77                       # simulated peak gain (linear)

# distance from the aperture to each virtual apex, and the slant lengths
R_h = L * A / (A - a)
R_e = L * B / (B - b)
rho_h = math.hypot(R_h, A / 2)
rho_e = math.hypot(R_e, B / 2)

# optimum-gain conditions (Balanis): A = sqrt(3 lam rho_h), B = sqrt(2 lam rho_e)
A_opt = math.sqrt(3 * lam * rho_h)
B_opt = math.sqrt(2 * lam * rho_e)

# maximum phase error across the aperture, in wavelengths: s = d^2 / (8 lam rho)
s_h = A ** 2 / (8 * lam * rho_h)
s_e = B ** 2 / (8 * lam * rho_e)

G_ideal = 4 * math.pi * A * B / lam ** 2  # uniform aperture
G_opt = 0.51 * G_ideal                    # optimum horn, aperture efficiency ~0.51

def db(x):
    return 10 * math.log10(x)

print(f"wavelength at 10 GHz          : {lam:.2f} mm")
print(f"slant lengths rho_h / rho_e   : {rho_h:.1f} / {rho_e:.1f} mm")
print(f"optimum aperture for them     : A = {A_opt:.1f} mm (built {A:.0f}),  B = {B_opt:.1f} mm (built {B:.0f})")
print(f"aperture phase error s_h / s_e: {s_h:.3f} / {s_e:.3f} wavelengths (optimum 3/8 = 0.375 and 1/4 = 0.25)")
print(f"gain, uniform aperture        : {db(G_ideal):.2f} dBi")
print(f"gain, optimum horn (0.51 eff.): {db(G_opt):.2f} dBi")
print(f"gain, HFSS                    : {db(G_hfss):.2f} dBi  ->  aperture efficiency {G_hfss / G_ideal:.2f}")
