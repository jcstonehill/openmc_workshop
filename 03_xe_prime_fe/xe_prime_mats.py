import openmc

materials = openmc.Materials()


### FUELS ###
code99 = openmc.Material()
code99.add_element("U", 0.438776289, "wo", enrichment=93.15, enrichment_type="wo")
code99.add_element("C", 1.835352478, "wo")
code99.set_density("sum")
code99.temperature = 300
materials.append(code99)

code89 = openmc.Material()
code89.add_element("U", 0.368882230, "wo", enrichment=93.15, enrichment_type="wo")
code89.add_element("C", 1.832985423, "wo")
code89.set_density("sum")
code89.temperature = 300
materials.append(code89)

code79 = openmc.Material()
code79.add_element("U", 0.322738545, "wo", enrichment=93.15, enrichment_type="wo")
code79.add_element("C", 1.846052815, "wo")
code79.set_density("sum")
code79.temperature = 300
materials.append(code79)

code69 = openmc.Material()
code69.add_element("U", 0.261028525, "wo", enrichment=93.15, enrichment_type="wo")
code69.add_element("C", 1.858977906, "wo")
code69.set_density("sum")
code69.temperature = 300
materials.append(code69)

code59 = openmc.Material()
code59.add_element("U", 0.261028525, "wo", enrichment=93.15, enrichment_type="wo")
code59.add_element("C", 1.858977906, "wo")
code59.set_density("sum")
code59.temperature = 300
materials.append(code59)

code49 = openmc.Material()
code49.add_element("U", 0.183589045, "wo", enrichment=93.15, enrichment_type="wo")
code49.add_element("C", 1.874599773, "wo")
code49.set_density("sum")
code49.temperature = 300
materials.append(code49)

code39 = openmc.Material()
code39.add_element("U", 0.134439686, "wo", enrichment=93.15, enrichment_type="wo")
code39.add_element("C", 1.881919595, "wo")
code39.temperature = 300
code39.set_density("sum")
materials.append(code39)

fuel_mats = {
    99: code99,
    89: code89,
    79: code79,
    69: code69,
    59: code59,
    49: code49,
    39: code39,
}


### COATINGS ###
coat99 = openmc.Material()
coat99.add_element("Nb", 6.881670983, "wo")
coat99.add_element("C", 0.889596672, "wo")
coat99.set_density("sum")
coat99.temperature = 300
materials.append(coat99)

coat89 = openmc.Material()
coat89.add_element("Nb", 6.316406222, "wo")
coat89.add_element("C", 0.816524646, "wo")
coat89.set_density("sum")
coat89.temperature = 300
materials.append(coat89)

coat79 = openmc.Material()
coat79.add_element("Nb", 5.939737872, "wo")
coat79.add_element("C", 0.771900404, "wo")
coat79.set_density("sum")
coat79.temperature = 300
materials.append(coat79)

coat69 = openmc.Material()
coat69.add_element("Nb", 6.565315718, "wo")
coat69.add_element("C", 0.848701287, "wo")
coat69.set_density("sum")
coat69.temperature = 300
materials.append(coat69)

coat59 = openmc.Material()
coat59.add_element("Nb", 6.194731122, "wo")
coat59.add_element("C", 0.800795651, "wo")
coat59.set_density("sum")
coat59.temperature = 300
materials.append(coat59)

coat49 = openmc.Material()
coat49.add_element("Nb", 6.604125879, "wo")
coat49.add_element("C", 0.853718294, "wo")
coat49.set_density("sum")
coat49.temperature = 300
materials.append(coat49)

coat39 = openmc.Material()
coat39.add_element("Nb", 5.871033397, "wo")
coat39.add_element("C", 0.758951102, "wo")
coat39.set_density("sum")
coat39.temperature = 300
materials.append(coat39)

ue_coat = openmc.Material()
ue_coat.add_element("Nb", 6.807478078, "wo")
ue_coat.add_element("C", 0.8800057232, "wo")
ue_coat.set_density("sum")
ue_coat.temperature = 300
materials.append(ue_coat)

coat_mats = {
    99: coat99,
    89: coat89,
    79: coat79,
    69: coat69,
    59: coat59,
    49: coat49,
    39: coat39,
}


### Propellant ###
prop_mat = openmc.Material()
prop_mat.add_element("H", 1)
materials.append(prop_mat)

### Unfueled Element ###
tierod_mat = openmc.Material()
tierod_mat.add_element("C", 0.04 / 100, "wo")
tierod_mat.add_element("Mn", 0.5 * 0.35 / 100, "wo")
tierod_mat.add_element("P", 0.5 * 0.015 / 100, "wo")
tierod_mat.add_element("S", 0.5 * 0.015 / 100, "wo")
tierod_mat.add_element("Si", 0.5 * 0.035 / 100, "wo")
tierod_mat.add_element("Cr", 0.5 * (17 + 21) / 100, "wo")
tierod_mat.add_element("Ni", 0.5 * (50 + 55.5) / 100, "wo")
tierod_mat.add_element("Mo", 0.5 * (2.8 + 3.3) / 100, "wo")
tierod_mat.add_element(
    "Nb", 0.5 * (2.4 + 2.8) / 100 + 0.5 * 0.5 * (4.75 + 5.50) / 100, "wo"
)
tierod_mat.add_element(
    "Ta", 0.5 * (2.4 + 2.8) / 100 + 0.5 * 0.5 * (4.75 + 5.50) / 100, "wo"
)
tierod_mat.add_element("Ti", 0.5 * (0.65 + 1.15) / 100, "wo")
tierod_mat.add_element("Al", 0.5 * (0.2 + 0.8) / 100, "wo")
tierod_mat.add_element("Co", 0.5 * 1 / 100, "wo")
tierod_mat.add_element("B", 0.5 * 0.006 / 100, "wo")
tierod_mat.add_element("Co", 0.5 * 0.3 / 100, "wo")
tierod_mat.add_element("Fe", 12.5745 / 100, "wo")
tierod_mat.set_density("g/cm3", 10.30224)
materials.append(tierod_mat)

ss_mat = openmc.Material()
ss_mat.add_element("Cr", 0.19, "wo")
ss_mat.add_element("Ni", 0.0925, "wo")
ss_mat.add_element("C", 0.0004, "wo")
ss_mat.add_element("Mn", 0.01, "wo")
ss_mat.add_element("Si", 0.00375, "wo")
ss_mat.add_element("P", 0.000225, "wo")
ss_mat.add_element("S", 0.00015, "wo")
ss_mat.add_element("N", 0.00005, "wo")
ss_mat.add_element("Fe", 0.702925, "wo")
ss_mat.set_density("g/cm3", 8.3260562)
materials.append(ss_mat)

pyrographite_mat = openmc.Material()
pyrographite_mat.add_element("C", 1.0, "ao")
pyrographite_mat.set_density("g/cm3", 2.165008473)
materials.append(pyrographite_mat)


### Peripheral ###
unfueled_graphite_mat = openmc.Material()
unfueled_graphite_mat.add_element("C", 1.0, "ao")
unfueled_graphite_mat.set_density("g/cm3", 2.093994125)
materials.append(unfueled_graphite_mat)

be_mat = openmc.Material()
be_mat.add_element("Be", 1.312725, "wo")
be_mat.add_element("Al", 0.0028560743, "wo")
be_mat.add_element("Ti", 0.0535283598, "wo")
be_mat.set_density("sum")
materials.append(be_mat)

poison_mat = openmc.Material()
poison_mat.add_element(
    "B",
    0.2075998882,
    "wo",
    enrichment=96.19,
    enrichment_target="B10",
    enrichment_type="wo",
)
poison_mat.add_element("Al", 0.7924001118, "wo")
poison_mat.set_density("g/cm3", 2.56)
materials.append(poison_mat)

interface_mat = openmc.Material()
interface_mat.add_element("C", 0.063029, "ao")
interface_mat.add_element("Fe", 0.000399, "ao")
interface_mat.add_element("Ni", 0.000051, "ao")
interface_mat.add_element("Cr", 0.000114, "ao")
interface_mat.add_element("Al", 0.000839, "ao")
interface_mat.add_element("Si", 0.000424, "ao")
interface_mat.add_element("O", 0.000849, "ao")
interface_mat.set_density("atom/b-cm", 0.065705)
materials.append(interface_mat)

pv_mat = openmc.Material()
pv_mat.add_element("Al", 1.0, "ao")
pv_mat.set_density("atom/b-cm", 0.0625)
materials.append(pv_mat)


## Forward / Aft ###
aft_plate_mat = openmc.Material()
aft_plate_mat.add_element("C", 0.8018855219, "wo")
aft_plate_mat.add_element("Ni", 0.1721212121, "wo")
aft_plate_mat.add_element("Mo", 0.025993266, "wo")
aft_plate_mat.set_density("g/cm3", 1.492114401)
aft_plate_mat.temperature = 300
materials.append(aft_plate_mat)

fwd_al_plate_mat = openmc.Material()
fwd_al_plate_mat.add_element("Al", 1.0, "ao")
fwd_al_plate_mat.set_density("g/cm3", 1.901172627)
fwd_al_plate_mat.temperature = 300
materials.append(fwd_al_plate_mat)

fe_loading_codes = {
    "G-1D": 89,
    "G-1E": 89,
    "H-3F": 89,
    "H-3C": 89,
    "H-3D": 79,
    "H-3E": 79,
    "H-4D": 89,
    "H-4E": 89,
    "H-5E": 89,
    "H-6D": 89,
    "H-6E": 89,
    "H-7F": 89,
    "H-7D": 89,
    "H-7E": 79,
    "J-3F": 79,
    "J-3G": 89,
    "J-3B": 89,
    "J-3C": 79,
    "J-3D": 69,
    "J-3E": 69,
    "J-3H": 39,
    "J-3J": 49,
    "J-3N": 39,
    "J-3V": 49,
    "J-3W": 69,
    "J-3R": 69,
    "J-3S": 49,
    "J-3T": 39,
    "J-3U": 39,
    "J-4F": 59,
    "J-4G": 69,
    "J-4B": 79,
    "J-4C": 69,
    "J-4D": 49,
    "J-4H": 39,
    "J-4K": 39,
    "J-4M": 39,
    "J-5F": 69,
    "J-5G": 79,
    "J-5A": 79,
    "J-5B": 79,
    "J-5C": 69,
    "J-5D": 49,
    "J-5J": 39,
    "J-5H": 39,
    "J-5K": 49,
    "J-6F": 59,
    "J-6G": 79,
    "J-6B": 79,
    "J-6C": 69,
    "J-6D": 59,
    "J-6H": 39,
    "J-6K": 39,
    "J-7F": 49,
    "J-7G": 69,
    "J-7B": 79,
    "J-7C": 69,
    "J-7D": 49,
    "J-7H": 39,
    "J-7K": 39,
    "J-8F": 39,
    "J-8G": 59,
    "J-8B": 69,
    "J-8C": 59,
    "J-8D": 39,
    "J-9H": 39,
    "J-9K": 49,
    "J-9P": 39,
    "J-9F": 69,
    "J-9G": 79,
    "J-9B": 89,
    "J-9C": 89,
    "J-9D": 79,
    "J-9E": 69,
    "J-9V": 59,
    "J-9W": 69,
    "J-9R": 69,
    "J-9S": 49,
    "J-9T": 39,
    "J-9U": 39,
}

plotting_colors = {
    prop_mat: (30, 100, 100),
    code99: (200, 200, 120),
    code89: (100, 200, 120),
    code79: (100, 200, 200),
    code69: (100, 150, 200),
    code59: (100, 100, 200),
    code49: (150, 100, 200),
    code39: (200, 100, 200),
    coat99: (150, 150, 150),
    coat89: (150, 150, 150),
    coat79: (150, 150, 150),
    coat69: (150, 150, 150),
    coat59: (150, 150, 150),
    coat49: (150, 150, 150),
    coat39: (150, 150, 150),
    tierod_mat: (200, 70, 135),
    ss_mat: (150, 150, 150),
    pyrographite_mat: (173, 57, 110),
    unfueled_graphite_mat: (100, 44, 86),
    be_mat: (160, 180, 180),
    poison_mat: (0, 0, 0),
    interface_mat: (180, 200, 200),
    pv_mat: (64, 64, 64),
}
