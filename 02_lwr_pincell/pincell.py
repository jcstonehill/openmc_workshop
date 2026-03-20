from math import log10

import numpy as np
import matplotlib.pyplot as plt
import openmc
import openmc.model
import openmc.stats

# Example taken directly from OpenMC code.
# https://github.com/openmc-dev/openmc/blob/develop/examples/pincell/build_xml.py

# Paul K. Romano, Nicholas E. Horelik, Bryan R. Herman, Adam G. Nelson,
# Benoit Forget, and Kord Smith, “OpenMC: A State-of-the-Art Monte Carlo
# Code for Research and Development,” Ann. Nucl. Energy, 82, 90-97 (2015).

### MATERIALS ###
uo2 = openmc.Material(name="UO2 fuel at 2.4% wt enrichment")
uo2.set_density("g/cm3", 10.29769)
uo2.add_element("U", 1.0, enrichment=2.4)
uo2.add_element("O", 2.0)

helium = openmc.Material(name="Helium for gap")
helium.set_density("g/cm3", 0.001598)
helium.add_element("He", 2.4044e-4)

zircaloy = openmc.Material(name="Zircaloy 4")
zircaloy.set_density("g/cm3", 6.55)
zircaloy.add_element("Sn", 0.014, "wo")
zircaloy.add_element("Fe", 0.00165, "wo")
zircaloy.add_element("Cr", 0.001, "wo")
zircaloy.add_element("Zr", 0.98335, "wo")

borated_water = openmc.Material(name="Borated water")
borated_water.set_density("g/cm3", 0.740582)
borated_water.add_element("B", 4.0e-5)
borated_water.add_element("H", 5.0e-2)
borated_water.add_element("O", 2.4e-2)
# TODO Add thermal scattering to H2O

# Collect the materials together and export to XML
materials = openmc.Materials([uo2, helium, zircaloy, borated_water])
materials.export_to_xml()


### GEOMETRY ###
# Create cylindrical surfaces
# TODO

# Create a region represented as the inside of a rectangular prism
# TODO

# Create cells, mapping materials to regions
# TODO

# Create a geometry and export to XML
# TODO

### SETTINGS ###
# Indicate how many particles to run
settings = openmc.Settings()
settings.batches = 50
settings.inactive = 10
settings.particles = 1000

# Create an initial uniform spatial source distribution over fissionable zones
# TODO

### TALLIES ###

# Let's create a tally to get the flux energy spectrum. We start by
# creating an energy filter
# TODO

### PLOTS ###
# x-y cross section plot
plots = openmc.Plots()
plot = openmc.Plot()
plot.basis = "xy"
plot.width = (pitch, pitch)
plot.origin = (0, 0, 0)
plot.color_by = "material"
plot.colors = {
    uo2: (200, 60, 60),
    helium: (200, 200, 120),
    clad: (150, 150, 150),
    borated_water: (30, 100, 200),
}
plot.pixels = (2000, 2000)
plots.append(plot)

# MODEL
model = openmc.Model(geometry, materials, settings, tallies, plots)
model.export_to_model_xml()


### RUN THAT THING! ###
openmc.plot_geometry()
openmc.run()


### POST PROCESSING###
# Plot the flux spectrum
with openmc.StatePoint(f"statepoint.{settings.batches}.h5") as sp:
    t: openmc.Tally = sp.get_tally(name="Flux spectrum")

    # Get the energies from the energy filter
    energy_filter = t.filters[0]
    energies = energy_filter.bins[:, 0]

    # Get the flux values
    mean = t.get_values(value="mean").ravel()
    uncertainty = t.get_values(value="std_dev").ravel()

# Plot flux spectrum
fix, ax = plt.subplots()
ax.loglog(energies, mean, drawstyle="steps-post")
ax.set_xlabel("Energy [eV]")
ax.set_ylabel("Flux")
ax.grid(True, which="both")
plt.savefig("spectrum.png")
