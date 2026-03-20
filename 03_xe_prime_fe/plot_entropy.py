import openmc
import matplotlib.pyplot as plt


def plot(N_batches):
    with openmc.StatePoint(f"statepoint.{N_batches}.h5") as sp:
        plt.plot(range(sp.n_batches), sp.entropy)
        plt.grid(True)
        plt.xlabel("Batch #")
        plt.ylabel("Shannon Entropy")
        plt.savefig("entropy.png")
