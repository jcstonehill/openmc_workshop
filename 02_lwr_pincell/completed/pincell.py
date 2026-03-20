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
borated_water.add_s_alpha_beta("c_H_in_H2O")

# Collect the materials together and export to XML
materials = openmc.Materials([uo2, helium, zircaloy, borated_water])
materials.export_to_xml()


### GEOMETRY ###

# Create cylindrical surfaces
fuel_or = openmc.ZCylinder(r=0.39218, name="Fuel OR")
clad_ir = openmc.ZCylinder(r=0.40005, name="Clad IR")
clad_or = openmc.ZCylinder(r=0.45720, name="Clad OR")

# Create a region represented as the inside of a rectangular prism
pitch = 1.25984
box = openmc.model.RectangularPrism(pitch, pitch, boundary_type="reflective")

# Create cells, mapping materials to regions
fuel = openmc.Cell(fill=uo2, region=-fuel_or)
gap = openmc.Cell(fill=helium, region=+fuel_or & -clad_ir)
clad = openmc.Cell(fill=zircaloy, region=+clad_ir & -clad_or)
water = openmc.Cell(fill=borated_water, region=+clad_or & -box)

# Create a geometry and export to XML
geometry = openmc.Geometry([fuel, gap, clad, water])
geometry.export_to_xml()


### SETTINGS ###

# Indicate how many particles to run
settings = openmc.Settings()
settings.batches = 50
settings.inactive = 10
settings.particles = 1000

# Create an initial uniform spatial source distribution over fissionable zones
lower_left = (-pitch / 2, -pitch / 2, -1)
upper_right = (pitch / 2, pitch / 2, 1)
uniform_dist = openmc.stats.Box(lower_left, upper_right)
settings.source = openmc.IndependentSource(
    space=uniform_dist, constraints={"fissionable": True}
)

settings.export_to_xml()

### TALLIES ###

# Let's create a tally to get the flux energy spectrum. We start by
# creating an energy filter
e_min, e_max = 1e-5, 20.0e6
groups = 500
energies = np.logspace(log10(e_min), log10(e_max), groups + 1)
energy_filter = openmc.EnergyFilter(energies)

spectrum_tally = openmc.Tally(name="Flux spectrum")
spectrum_tally.filters = [energy_filter]
spectrum_tally.scores = ["flux"]

# Instantiate a Tallies collection and export to XML
tallies = openmc.Tallies([spectrum_tally])
tallies.export_to_xml()

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
