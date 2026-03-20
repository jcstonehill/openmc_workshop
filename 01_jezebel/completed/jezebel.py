import openmc

# Example taken directly from OpenMC code.
# https://github.com/openmc-dev/openmc/blob/develop/examples/jezebel/jezebel.py

# Paul K. Romano, Nicholas E. Horelik, Bryan R. Herman, Adam G. Nelson,
# Benoit Forget, and Kord Smith, “OpenMC: A State-of-the-Art Monte Carlo
# Code for Research and Development,” Ann. Nucl. Energy, 82, 90-97 (2015).


### MATERIALS ###
# Create material
pu = openmc.Material()

# Add plutonium to material.
# Nuclide abundances are specified.
pu.add_nuclide("Pu239", 3.7047e-02)
pu.add_nuclide("Pu240", 1.7512e-03)
pu.add_nuclide("Pu241", 1.1674e-04)

# Add gallium to material. Nuclide abundances are assumed to be natural
# abundance, so we can use add_element() instead of adding nuclides
# individually.
pu.add_element("Ga", 1.3752e-03)

# Density is set as the sum of constituents
pu.set_density("sum")

# Create materials object and export it.
mats = openmc.Materials([pu])
mats.export_to_xml()


### GEOMETRY ###
# Define a single cell, a sphere, filled with plutonium alloyed with gallium.
sphere = openmc.Sphere(r=6.3849, boundary_type="vacuum")
cell = openmc.Cell(fill=pu, region=-sphere)

# Create geometry object and export it.
geom = openmc.Geometry([cell])
geom.export_to_xml()


### SETTINGS ###
settings = openmc.Settings()
settings.batches = 50
settings.inactive = 10
settings.particles = 1000
settings.export_to_xml()


### EXECUTION ###
# Run the simulation
openmc.run()


### POST PROCESSING ###
# Get the resulting k-effective value
n = settings.batches
with openmc.StatePoint(f"statepoint.{n}.h5") as sp:
    keff = sp.keff
    print(f"Final k-effective = {keff}")
