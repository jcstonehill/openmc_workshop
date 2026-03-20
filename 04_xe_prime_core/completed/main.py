import openmc
import xe_prime_model
import xe_prime_post

cd_angle = 120
Qth = 1137e6

axial_N = 1
T_fuel = [1600]
T_prop = [1600]
rho_prop = [8.988e-5]

model: openmc.Model = xe_prime_model.generate_model(cd_angle, T_fuel, T_prop, rho_prop)

model.export_to_model_xml()
openmc.plot_geometry()

path = model.run()

xe_prime_post.post_process(path, Qth)
