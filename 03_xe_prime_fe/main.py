import openmc
import openmc.model
import numpy as np
import xe_prime_mats as mats
import plot_entropy

# This will create axial layers of material for discretizing temperature.
axial_N = 20
T_fuel = np.linspace(300, 2700, axial_N)
T_prop = np.linspace(300, 2700, axial_N)
rho_prop = np.full(axial_N, 8.988e-5)

# This fe_universe that we're creating has the outer graphite material
# extending infinitely in the x-y directions, and then top and bottom
# stacked regions extending infinitely in the +z and -z directions.
fe_inf_universe = openmc.Universe()
channel_universe = openmc.Universe()
outer_universe = openmc.Universe()

prop_or = openmc.ZCylinder(r=0.1213104)
coating_or = openmc.ZCylinder(r=0.12573)

# This loop will stack layers axially based on axial_N, this is useful for
# temperature discretization.
upper_div = None
for i in range(axial_N):
    coating_mat = mats.coat_mats[99]
    fuel_mat = mats.fuel_mats[99]

    # z position of bottom divider
    z = 129.54 / 2 - 129.54 * (i + 1) / axial_N

    lower_div = openmc.ZPlane(z0=z)

    # If there is no upper_div, then we're creating the region that extends
    # infinitely upward.
    if upper_div is None:
        region = +lower_div

    # If this is the last iteration, then it should extend infinitely
    # downward from the last divider that was created.
    elif i == axial_N - 1:
        region = -upper_div

    # This is a normal region, with a clear upper and lower bound.
    else:
        region = +lower_div & -upper_div

    # Create axial layer of prop for channel universe
    prop_cell = openmc.Cell(region=region & -prop_or, fill=mats.prop_mat)
    prop_cell.density = rho_prop[i]
    prop_cell.temperature = T_prop[i]

    # Create axial layer of coating for channel universe
    coating_cell = openmc.Cell(region=region & +prop_or & -coating_or, fill=coating_mat)
    coating_cell.temperature = T_fuel[i]

    # Create axial layer of prop for fuel universe
    fuel_cell = openmc.Cell(region=region & +coating_or, fill=fuel_mat)
    fuel_cell.temperature = T_fuel[i]

    channel_universe.add_cells([prop_cell, coating_cell, fuel_cell])
    outer_universe.add_cell(openmc.Cell(region=region, fill=fuel_mat))

    upper_div = lower_div

# This is the lattice of 19 cooling channels inside of one fuel element.
# TODO

# Bound the geometry to the top, bottom, and hexagon to yield a fuel element
# TODO

# Create final root universe
root_cell = openmc.Cell(region=-top & +bottom & -outer_hex, fill=fe_lattice)
root = openmc.Universe(cells=[root_cell])

# Now, complete model
geometry = openmc.Geometry(root)
materials = mats.materials

# We're going to check out the shannon entropy
# TODO

# Settings defined here + shannon entropy
settings = openmc.Settings()
settings.batches = 50
settings.inactive = 10
settings.particles = 1000
# TODO Add temperature interpolation
# TODO Add entropy mesh

# x-y cross section plot
plots = openmc.Plots()
plot = openmc.Plot()
plot.basis = "xy"
plot.width = (3, 3)
plot.origin = (0, 0, 0)
plot.color_by = "material"
plot.colors = mats.plotting_colors
plot.pixels = (2000, 2000)
plots.append(plot)

# x-z cross section plot
plot = openmc.Plot()
plot.basis = "xz"
plot.width = (5, 150)
plot.pixels = (5 * 200, 150 * 200)
plot.color_by = "cell"  # By cell so we can see axially discretization
plots.append(plot)

model = openmc.Model(geometry, materials, settings, plots=plots)
model.export_to_model_xml()

# Run that thing!
openmc.plot_geometry()
openmc.run()

plot_entropy.plot(settings.batches)
