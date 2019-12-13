# Written By: Robert Stillwell
# Written For: NCAR
# This program will take a base tempearture and pressure and calculate the 
# water vapor absorption cross section assuming a lapse rate and a hydro-
# statics pressure profile. 

# %% Importing libraries
import numpy as np
import Spectroscopy as Spec

# %% Loading hitran parameters
Hitran = np.genfromtxt('823nm_834nm_HITRAN_2012.csv',delimiter=',')

# %% Processing Constants
XMin      = 828.     # Minimum wavelength to use for line selection
XMax      = 828.55   # Maximum wavelength to use for line selection
LapseRate = 0.0065   # Moist adiabatic lapse rate (K/m)

# %% Input parameters
BaseTemp   = 300     # Temperature of interest [K]
BasePress  = 1.      # Pressure of interest [atm]
Lambda     = 828.2   # Wavelength to use 
BaseAlt    = 0       # Minimum altitude to process
MaxAlt     = 12000   # Maximum altitude to process
AltRes     = 37.5    # Resolution at which to calculate temp/pressure profiles

# %% Calculating temperature and pressure profiles
Alts  = np.arange(BaseAlt,MaxAlt,AltRes)    # Units of meters
Temp  = BaseTemp - LapseRate * Alts         # Units of Kelvin
Press = BasePress*(BaseTemp/Temp)**-5.5     # units of atmospheres)

# %% 
Nu = (1e7)/Lambda  # Converting wavelength to wavenumbers [cm^-1]

# %%
AbsorptionCoeff  = Spec.BuildAbsorptionSpectrum(Hitran,Nu,Temp,Press)

print(AbsorptionCoeff)

############## Plotting ############
#plt.figure
#plt.plot(AbsorptionCoeff,Alts,'k')
## Labeling the axes
#plt.ylabel('Altitudes [$m$]'); plt.xlabel('Absorption Coefficient [$cm^2$]'); 
#plt.title('Range Resolved Absorption Coefficient')
#plt.grid('on')
## showing the plot
#plt.show()

