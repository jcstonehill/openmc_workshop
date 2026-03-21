import openmc
import numpy as np
import matplotlib.pyplot as plt

import xe_prime_mats as mats


def generate_model(cd_angle, T_fuel, T_prop, rho_prop):
    axial_N = len(T_fuel)

    f2f = 1.91516
    edge = 1.91516 / np.sqrt(3)

    # Active core universe
    core = openmc.Universe()

    ### Infinite Unfueled Graphite ###
    unfueled = openmc.Cell(fill=mats.unfueled_graphite_mat)
    unfueled_universe = openmc.Universe(cells=[unfueled])

    # This is just a nested list of universes to correspond to the hex lattice, all
    # being unfueled universe to start.
    universes = [[unfueled_universe]]
    N = 6
    for _ in range(26):
        universes.insert(0, N * [unfueled_universe])
        N += 6

    ### Unfueled Element ###
    # This is basically a bunch of concentric cylinders.
    # We only consider one type of UE and assume they're all the same.
    ue_universe = openmc.Universe()

    annuli_d = [0.2794, 0.57404, 0.60198, 0.62484, 0.90678, 0.9175496, 0.92456]
    annuli_mat = [
        mats.tierod_mat,
        None,
        mats.ss_mat,
        None,
        mats.pyrographite_mat,
        None,
        mats.ue_coat,
        mats.unfueled_graphite_mat,
    ]

    prev_surf = None
    for i in range(len(annuli_d)):
        surf = openmc.ZCylinder(r=annuli_d[i] / 2)

        if prev_surf is None:
            region = -surf

        else:
            region = -surf & +prev_surf

        cell = openmc.Cell(region=region, fill=annuli_mat[i])
        ue_universe.add_cell(cell)

        prev_surf = surf

    cell = openmc.Cell(region=+prev_surf, fill=annuli_mat[-1])
    ue_universe.add_cell(cell)

    def get_loading_code(fe_id):
        # Get the loading code for a given fuel element id.
        fe_id = fe_id[1:]
        if fe_id in mats.fe_loading_codes.keys():
            return mats.fe_loading_codes[fe_id]

        return 99

    ### Fueled Elements ###
    fe_universes = {}

    # Make one universe for each loading code
    for loading_code, mat in mats.fuel_mats.items():

        # This fe_universe that we're creating has the outer graphite material
        # extending infinitely in the x-y directions, and then top and bottom
        # stacked regions extending infinitely in the +z and -z directions.
        fe_universe = openmc.Universe(name="fe_code_" + str(loading_code))
        channel_universe = openmc.Universe()
        outer_universe = openmc.Universe()

        prop_or = openmc.ZCylinder(r=0.1213104)
        coating_or = openmc.ZCylinder(r=0.12573)

        # This loop will stack layers axially based on axial_N, this is useful for
        # temperature discretization.
        upper_div = None
        for i in range(axial_N):
            # Get mats
            coating_mat = mats.coat_mats[loading_code]
            fuel_mat = mats.fuel_mats[loading_code]

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

            # Create channel universe for this fe
            prop_cell = openmc.Cell(region=region & -prop_or, fill=mats.prop_mat)
            prop_cell.density = rho_prop[i]
            prop_cell.temperature = T_prop[i]

            coating_cell = openmc.Cell(
                region=region & +prop_or & -coating_or, fill=coating_mat
            )
            coating_cell.temperature = T_fuel[i]

            fuel_cell = openmc.Cell(region=region & +coating_or, fill=fuel_mat)
            fuel_cell.temperature = T_fuel[i]

            channel_universe.add_cells([prop_cell, coating_cell, fuel_cell])

            # The outside of the channel is just fuel
            outer_universe.add_cell(openmc.Cell(region=region, fill=fuel_mat))

            upper_div = lower_div

        # This is the lattice of 19 cooling channels inside of one fuel element.
        fe_lattice = openmc.HexLattice()
        fe_lattice.center = (0.0, 0.0)
        fe_lattice.pitch = [0.44]
        fe_lattice.outer = outer_universe
        fe_lattice.orientation = "x"
        fe_lattice.universes = [
            12 * [channel_universe],
            6 * [channel_universe],
            1 * [channel_universe],
        ]

        # Create the cell and add that single cell to the universe.
        cell = openmc.Cell(
            name="fe_lattice_code_" + str(loading_code), region=region, fill=fe_lattice
        )
        fe_universe.add_cell(cell)

        fe_universes[loading_code] = fe_universe

    ### Core Hex Lattice ###
    # We create the hex lattice here so that we can populate it as we interpret the
    # fuel elements.
    # TODO create core hex lattice

    # Create control drum universe
    cd_fill_universe = openmc.Universe()
    cd_or = openmc.ZCylinder(r=4.76 + 0.125)
    poison_ir = openmc.ZCylinder(r=4.76)
    poison_plane1 = openmc.YPlane()
    poison_plane2 = openmc.Plane.from_points(
        [0, 0, 0], [-0.5, 0.866025, 0], [-0.5, 0.866025, 1]
    )

    # Special attention to this poison & cd region, it's complicated.
    poison_region = +poison_plane1 & +poison_plane2 & +poison_ir & -cd_or

    # We have to say "anything that isn't poison is cd" inside of the cd_or
    cd_region = ~poison_region & -cd_or
    cd_flow_region = +cd_or

    cd_fill_universe.add_cell(openmc.Cell(region=cd_region, fill=mats.be_mat))
    cd_fill_universe.add_cell(openmc.Cell(region=poison_region, fill=mats.poison_mat))
    cd_fill_universe.add_cell(openmc.Cell(region=cd_flow_region, fill=None))

    # Core Periphery
    core_or = openmc.ZCylinder(r=2.54 * 17.785)
    interface_or = openmc.ZCylinder(r=2.54 * 40 / 2)
    gap1_or = openmc.ZCylinder(r=50.96637)
    refl_or = openmc.ZCylinder(r=62.69863)
    gap2_or = openmc.ZCylinder(r=2.54 * 49.562 / 2)

    core = openmc.Universe()
    core_cell = openmc.Cell(fill=hex_lattice, region=-core_or)
    core.add_cell(core_cell)

    interface_cell = openmc.Cell(
        fill=mats.interface_mat, region=+core_or & -interface_or
    )
    gap1_cell = openmc.Cell(fill=None, region=-gap1_or & +interface_or)
    core.add_cells([interface_cell, gap1_cell])

    refl_region = +gap1_or & -refl_or

    # Place the 12 control drums
    for i in range(12):
        angle0 = -np.arctan(0.5 * f2f / (4.5 * edge))

        angle = angle0 + 2 * np.pi * i / 12
        x = 56.8325 * np.cos(angle)
        y = 56.8325 * np.sin(angle)

        surf = openmc.ZCylinder(x, y, r=5.42798)

        refl_region = refl_region & +surf

        cell = openmc.Cell(region=-surf, fill=cd_fill_universe)

        # We have to translate each one since its at x, y = 0, 0
        cell.translation = (x, y, 0)

        # We have to rotate each one too. As we move around the reflector, the
        # universe needs to rotate 360/12 degrees. But also make sure they're all at
        # cd_angle which is a user input.
        cell.rotation = (0, 0, i * 360 / 12 + 120 - cd_angle)

        core.add_cell(cell)

    # Add periphery to core universe
    cell = openmc.Cell(region=refl_region, fill=mats.be_mat)
    core.add_cell(cell)

    cell = openmc.Cell(region=+refl_or & -gap2_or, fill=None)
    core.add_cell(cell)

    cell = openmc.Cell(region=+gap2_or, fill=mats.pv_mat)
    core.add_cell(cell)

    # Pressure vessel has a vacuum boundary condition.
    pv_or = openmc.ZCylinder(r=2.54 * 50.530 / 2)
    pv_or.boundary_type = "vacuum"

    # Top components which includes a vacuum boundary condition
    top_active_core = openmc.ZPlane(129.54 / 2)
    top_cluster_plate = openmc.ZPlane(129.54 / 2 + 3.332)
    top_al_plate = openmc.ZPlane(129.54 / 2 + 3.332 + 15.24)
    top_al_plate.boundary_type = "vacuum"

    # Same for bottom components, this is the last boundary condition we need.
    bottom_active_core = openmc.ZPlane(-129.54 / 2)
    bottom_aft_plate = openmc.ZPlane(-129.54 / 2 - 8.255)
    bottom_aft_plate.boundary_type = "vacuum"

    # Trim the infinitely extending core top & bottom of active core.
    cell = openmc.Cell(fill=core, region=-top_active_core & +bottom_active_core)

    # Now we add fwd and aft components.
    aft_cell = openmc.Cell(fill=mats.aft_plate_mat, region=-bottom_active_core)
    fwd_cluster_cell = openmc.Cell(
        fill=mats.ss_mat, region=+top_active_core & -top_cluster_plate
    )
    fwd_al_plate = openmc.Cell(fill=mats.fwd_al_plate_mat, region=+top_cluster_plate)

    # This is infinitely extending in all directions with fwd & aft components.
    inf_root = openmc.Universe(cells=[cell, aft_cell, fwd_cluster_cell, fwd_al_plate])

    # Finally trim by boundary surfaces to yield a final cell
    root_cell = openmc.Cell(
        fill=inf_root, region=-pv_or & +bottom_aft_plate & -top_al_plate
    )

    # Make a universe with the final cell
    root = openmc.Universe(cells=[root_cell])

    # x-y cross section plot
    plots = openmc.Plots()
    plot = openmc.Plot()
    plot.basis = "xy"
    plot.width = (150, 150)
    plot.origin = (0, 0, 0)
    plot.color_by = "material"
    plot.colors = mats.plotting_colors
    plot.pixels = (2000, 2000)
    plots.append(plot)

    # x-z axial plot
    plot = openmc.Plot()
    plot.basis = "xz"
    plot.width = (150, 175)
    plot.pixels = (1500, 1750)
    plot.colors = mats.plotting_colors
    plot.color_by = "material"
    plots.append(plot)

    ### Tallies ###
    tallies = openmc.Tallies()

    # Total heating
    tally = openmc.Tally(name="total_heat")
    tally.scores = ["heating"]
    tallies.append(tally)

    # Flux spectrum plot
    energies = np.logspace(np.log10(1e-5), np.log10(20.0e6), 501)
    e_filter = openmc.EnergyFilter(energies)
    tally = openmc.Tally(name="spectrum")
    tally.filters = [e_filter]
    tally.scores = ["flux"]
    tallies.append(tally)

    # A very fine x-y mesh for other tallies
    # TODO

    # Total heating x-y
    # TODO

    # Thermal flux x-y
    # TODO

    # Fast Flux x-y
    # TODO

    # Now create settings
    settings = openmc.Settings()
    settings.batches = 50
    settings.inactive = 10
    settings.particles = 1000
    settings.temperature = {"method": "interpolation"}

    # Create and export openmc Model
    model = openmc.Model()
    model.materials = mats.materials
    model.geometry = openmc.Geometry(root)
    model.plots = plots
    model.settings = settings
    model.tallies = tallies

    return model
