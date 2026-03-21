import openmc

# Example taken directly from OpenMC code.
# https://github.com/openmc-dev/openmc/blob/develop/examples/jezebel/jezebel.py

# Paul K. Romano, Nicholas E. Horelik, Bryan R. Herman, Adam G. Nelson,
# Benoit Forget, and Kord Smith, “OpenMC: A State-of-the-Art Monte Carlo
# Code for Research and Development,” Ann. Nucl. Energy, 82, 90-97 (2015).


### MATERIALS ###
# Create material
# TODO

# Add plutonium to material.
# Nuclide abundances are specified.
# TODO

# Add gallium to material. Nuclide abundances are assumed to be natural
# abundance, so we can use add_element() instead of adding nuclides
# individually.
# TODO

# Density is set as the sum of constituents
# TODO

# Create materials object and export it.
# TODO

### GEOMETRY ###
# Define a single cell, a sphere, filled with plutonium alloyed with gallium.
# TODO

# Create geometry object and export it.
# TODO

### SETTINGS ###
# TODO

### EXECUTION ###
# Run the simulation
# TODO

### POST PROCESSING ###
# Get the resulting k-effective value
# TODO