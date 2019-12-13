

import numpy as np

def BuildAbsorptionSpectrum(Hitran,Nu,Temperature,Pressure):
    ###### Loading the universal constants ######
    Const = Constants(1)
    ###### Hitran reference temp and pressure ######
    ReferencePressure    = 1.
    ReferenceTemperature = 296.
    ###### Parsing up Hitran information ######
    Delta            = Hitran[:,7] # Pressure shift from HiTRAN [cm^-1 atm^-1]
    LineCenterRef    = Hitran[:,0] # The frequency of the absorption line  
                                   # center from Hitran [cm^-1]
    LineEnergy       = Hitran[:,5] # Ground state transition energy from 
                                   # Hitran 
    LineStrengthRef  = Hitran[:,1] # Reference line strength from Hitran 
                                   # [cm^-1/(mol*cm^-2)] [cm^-1]
    LineWidthAirRef  = Hitran[:,3] # Air-broadened halfwidth at reference 
                                    # temperature and pressure from Hitran 
                                   # [cm^-1/atm]
    N                = Hitran[:,6] # Linewidth temperature dependence factor 
                                   # from HITRAN
    ###### Reshaping Hitran data ######                       
    Delta            = Delta.reshape(len(Delta),1);
    LineCenterRef    = LineCenterRef.reshape(len(LineCenterRef),1)
    LineEnergy       = LineEnergy.reshape(len(LineEnergy),1)
    LineStrengthRef  = LineStrengthRef.reshape(len(LineStrengthRef),1)
    LineWidthAirRef  = LineWidthAirRef.reshape(len(LineWidthAirRef),1)   
    N                = N.reshape(len(N),1)                     
    ###### Shifting the line cneter reference location based on pressure ######
    LineCenterRef = LineCenterRef+Delta*Pressure/ReferencePressure
    ###### Calculating Doppler width ######
    AlphaD = HalfWidthDoppler(Const, LineCenterRef, Temperature)
    ###### Calculating Lorentz width ######
    AlphaL = HalfWidthLorentz(LineWidthAirRef,N,Pressure,ReferencePressure,ReferenceTemperature,Temperature)
    ###### Calculating the line strentgh ######
    LStrength = LineStrength(Const,LineEnergy,LineStrengthRef,ReferenceTemperature,Temperature)
    ###### Calculating the Voigt profiles ######
    Sigma = Voigt(AlphaD,AlphaL,Nu,LineCenterRef,LStrength,50)
    return Sigma
    
class Constants:
    def __init__(self,*args):
        self.C   = 299792458           # Speed of light in vacuum         [m/s]
        self.Kb  = 1.38064852e-23      # Boltzmann's constant   [m^2 kg /s^2 K]    
        self.M   = 18.015e-3/6.022e23  # Mass of a single water molecule   [kg]
        self.h   = 6.62607004e-34      # Planck's constant         [m^2 kg / s]

def HalfWidthDoppler(Const, Nuij, Temp):
    AlphaD = (Nuij/Const.C)*np.sqrt(2*Const.Kb*Temp*np.log(2)/Const.M)
    return AlphaD

def HalfWidthLorentz(LineWidthR, N, Pressure, RefP, RefT, Temperature):
    AlphaL = LineWidthR*(Pressure/RefP)*(RefT/Temperature)**N
    return AlphaL

def LineStrength(Const,Energy,LS0,RefT,Temperature):
    LS = LS0*((RefT/Temperature)**1.5)*np.exp((100*Const.h*Const.C/Const.Kb)*Energy*(1/RefT - 1/Temperature))
    return LS
        
def Voigt(AlphaD,AlphaL,Nu,Nu0,S,IntNum):
    # Reshaping arrays to allow for proper broadcasting if needed
    if np.isscalar(Nu)==0:
        Nu = Nu.reshape(1,len(Nu))   
    # Calculating Voigt parameters
    X = (Nu-Nu0)*np.sqrt(np.log(2))/AlphaD
    Y = AlphaL*np.sqrt(np.log(2))/AlphaD
    ### not sure why this needs to be negative to make positive Sigma ###
    t = -np.arange(-np.ceil(IntNum/2),np.floor(IntNum/2)+1)
    # Reshaping the Voigt parameter    
    t = np.transpose(np.tile(t[:,None,None],(1,X.shape[0],X.shape[1])),(1,2,0))    
    # Performing integration    
    Integrand = np.exp(-t**2)/(Y[:,:,None]**2 + (X[:,:,None]-t)**2) 
    VoigtProfile = (Y/np.pi)*np.trapz(t[0,0,:],Integrand)
    # Calculating cross section
    Sigma = np.sum((S/AlphaD)*np.sqrt(np.log(2)/np.pi)*VoigtProfile,0)
    return Sigma