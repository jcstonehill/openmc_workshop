import openmc
import numpy as np
import matplotlib.pyplot as plt


def post_process(path, Qth):
    with openmc.StatePoint(path) as sp:
        # Get total heat score for tally normalization
        tally: openmc.Tally = sp.get_tally(name="total_heat")
        total_heat_score = tally.mean.ravel()[0]

        # Plot flux spectrum
        tally: openmc.Tally = sp.get_tally(name="spectrum")
        energies = np.logspace(np.log10(1e-5), np.log10(20.0e6), 501)
        flux_mean = tally.mean.ravel()

        fig, ax = plt.subplots()
        ax.step(energies[:-1], flux_mean / np.diff(energies))
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel("Energy [eV]")
        ax.set_ylabel("Flux [n-cm/eV-src]")
        ax.grid()
        fig.savefig("spectrum.png")
        plt.clf()

        # Plot Heating x-y
        tally: openmc.Tally = sp.get_tally(name="heating_xs")
        heating = tally.get_slice(scores=["heating"])
        plt.imshow(heating.mean.reshape(1000, 1000) * (Qth / total_heat_score))
        plt.savefig("heating_xs.png", dpi=600)
        plt.clf()

        # Plot Thermal Flux x-y
        tally: openmc.Tally = sp.get_tally(name="thermal_flux_xs")
        heating = tally.get_slice(scores=["flux"])
        plt.imshow(heating.mean.reshape(1000, 1000))
        plt.savefig("thermal_flux_xs.png", dpi=600)
        plt.clf()

        # Plot Fast Flux x-y
        tally: openmc.Tally = sp.get_tally(name="fast_flux_xs")
        heating = tally.get_slice(scores=["flux"])
        plt.imshow(heating.mean.reshape(1000, 1000))
        plt.savefig("fast_flux_xs.png", dpi=600)
        plt.clf()
