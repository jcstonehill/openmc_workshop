import openmc
import openmc.data
import matplotlib.figure
import matplotlib.pyplot as plt

# Gets a directory that points to xs data files for each nuclide.
data_library = openmc.data.DataLibrary.from_xml()

# Pull out the path to the U235 XS data file.
path = data_library.get_by_material("U235")["path"]

# Read the file and get the incident neutron xs data.
u235 = openmc.data.IncidentNeutron.from_hdf5(path)

# I'm only interested in the total xs (MT=1) but there's more available in
# u235.reactions
total = u235[1]

# Get energy data points for T = 294 K
energies = u235.energy["294K"]

# Plot the total xs at all energy data points
plt.loglog(energies, total.xs["294K"](energies))

# Do the same thing for T = 2500 K so we can see the change in xs due to
# temperature
energies = u235.energy["2500K"]
plt.loglog(energies, total.xs["2500K"](energies))

# Finally plot it!
plt.grid(True)
plt.xlabel("Energy (eV)")
plt.ylabel("Cross section (b)")
plt.title("Total XS of U235")
plt.legend(["294 K", "2500 K"])
plt.savefig("u235_xs.png")
