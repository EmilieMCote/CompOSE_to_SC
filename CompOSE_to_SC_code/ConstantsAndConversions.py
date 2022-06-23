import numpy as np

GNewton = 6.67408e-11       #Gravitational constant in SI
GNewton_cgs = 6.67408e-8    #Gravitational constant in cgs
kBoltzmann = 1.3806e-23     #Boltzmann constant in SI
clight = 2.99792458e8       #speed of light in SI
clight_cgs = 2.99792458e10  #speed of light in cgs
Msol = 1.989e30             #Solar mass in SI
permittivity = 8.854187e-12 #permittivity of free space in SI
nuetronMassCgs = 1.6749e-24 #Mass of neutron in grams

#internal Cactus conversion factors
cactusM = 5.028916268544129e-34
cactusL = 6.772400341316594e-06
cactusT = 2.0303145448833407e5
cactusV = 1.0/(cactusL*cactusL*cactusL)

Gc2 = GNewton/clight**2*1e-3*Msol
Gc2_cgs = GNewton_cgs/clight_cgs**2
convMsoltokm = Gc2
convMsoltokg = 1.989e30
convkmtos = 1./(clight*1e-3)
convkmtoinvGauss = np.sqrt(permittivity*GNewton/clight**2)*1e3*1e-4
convinvkm2togpercm3=1e-10/Gc2_cgs
convinvm2togpercm3=1e-10/Gc2_cgs*1e-6
convcactustocgs_density=1./(convMsoltokm**2)*convinvkm2togpercm3
convcactustocgs_pressure=1./(convMsoltokm**2)*convinvkm2togpercm3*clight_cgs**2
convcgstocactus_density = cactusM*cactusV
convcgstocactus_pressure = cactusM/(cactusL*cactusT*cactusT)

convGeVtokg = 1.78e-27
convGeVtoinvcm = 5.06e13
convGeVtoinvs = 1.52e24
convGeVtoK =1.16e13
convamutokg =1.6605e-27

convcmtoinvGeV = 5.06e13
convstoinvGeV = 1.52e24

convinvGeVtocm = 1.98e-14
convinvGeVtos = 6.58e-25

convkgtoGeV = 5.62e26
convinvcmtoGeV = 1.98e-14
convinvstoGeV = 6.58e-25
convKtoGeV =8.62e-14
convGeVtoinvFM = 0.0008065*(2*np.pi)*1e-3
convgtoGeV = 624.15
convGeVtog = 1/624.15

convfmtocm = 1.0e-13
convMeVtoGeV = 1.0e-3
