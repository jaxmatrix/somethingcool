import numpy as np 


# Science 

def NusseltNumber(ReynodNumber,PrandtlNumber,L,D):
    return 1.86*(ReynodNumber*PrandtlNumber/(L/D))**1.5 

def SheerwoodNumber(ReynodNumber,ShmidtNumber):
    return 0.023*ReynodNumber**0.83*ShmidtNumber**0.33

def h_heat(length_channel,equivalent_diameter,themal_conductivity,ReynodNumber,PrandtlNumber):
    return NusseltNumber(ReynodNumber,PrandtlNumber,length_channel,equivalent_diameter)*themal_conductivity/length_channel

def h_mass(ReynodNumber,ShmidtNumber,length_channel,themal_conductivity):
    return SheerwoodNumber(ReynodNumber,ShmidtNumber)*themal_conductivity/length_channel



# Initial Condition

temp_inlet_dry = 
absHumidity_inlet_dry = 
temp_productAir = 
temp_water = 


# Geometrical Parameters 

height = 
length = 
width = 

# Simulation Parameters

steps = 
convergence = 

# Looping function to simulate the value

'''
    Mass flow rate : m 
    Specific Heat Capacity : c
    Absoulte Humidity : w
    enthalpy of vaporisation : iv


    Assumptions :
    1. Temperature of water is maintained using a thermocouple implies (temperature of water remains same)
    2. 
'''


def update_temperature_productAir(self,argv_list):
    return ( h_heat*dx*b*(T_productAir - T_water) + m_productAir*c_productAir*T_productAir )/ ( m_productAir*c_productAir ) 

def update_temperature_workingAir_dry(self,argv_list):
    return ( h_heat*dx*b*(T_workingAir_dry - T_water) + m_workingAir_dry*c_productAir*T_workingAir_dry  ) / ( m_workingAir_dry*c_productAir )

def update_absoluteHumidity_workingAir_wet(self,argv_list):
    return ( h_mass*dx*b*(w_saturated_wet - w_workingAir_wet) + m_workingAir_wet*w_workingAir_wet  ) / ( m_workingAir_wet )

def update_temperature_workingAir_wet(self,argv_list):
    return ( h_heat*dx*b*(T_water-T_workingAir_wet) + h_mass*(dx)*b*iv*(w_saturated_wet - w_workingAir_wet) + T_workingAir_wet*m_workingAir_dry*c_productAir) / (m_workingAir_dry*c_productAir)

# This function will be changed to change in temperature of water in the system

def update_massFlowRate_workingAir_wet(self):
    dT = 
    return -1. * (m_productAir*c_productAir*dT + m_workingAir_wet*iv*(w_saturated_wet - w_workingAir_wet + c_water*m_water*T_water)) / (c_water*T_water)

def waitForConvergence(convergence_factor,function,seed,*argv):
    
    parameter_list = argv
    value1 = function(seed,argv)
    value2 = function(value1,argv)

    if  abs((value1 - value2)/value1) > convergence_factor
        return waitForConvergence(convergence_factor,nunction,value2,argv)
    else
        return value2


# Simulations 

# TODO: make a matrix to solve the equation and the use the internal loop for calculating the value of the values


def simulate(steps,convergence_factor,*initalCondition):

    dx = length_channel/steps 
    T_productAir = []
    T_workingAir_dry = []
    T_workingAir_wet = []
    absoluteHumidity_workingAir_wet = []
    T_water = []

    for n in range(steps):
    
        T_productAir_argumentList = ()
        T_productAir_update = waitForConvergence(convergence_factor,update_temperature_productAir,T_productAir[n],T_productAir_argumentList)
        T_productAir.append(T_productAir_update)

        T_workingAir_dry_argumentList = ()
        T_workingAir_dry_update = waitForConvergence(convergence_factor,update_temperature_workingAir_dry,T_workingAir_dry[n],T_productAir_argumentList) 
        T_workingAir_dry.append(T_workingAir_dry_update)

        T_workingAir_wet_argumentList = ()
        T_workingAir_wet_update = waitForConvergence(convergence_factor,update_temperature_workingAir_wet,T_workingAir_wet[n],T_workingAir_wet_argumentList)
        T_workingAir_wet.append(T_workingAir_wet_update)

        absoluteHumidity_workingAir_wet_argumentList = ()
        absoluteHumidity_workingAir_wet_update = waitForConvergence(convergence_factor,update_absoluteHumidity_workingAir_wet,absoluteHumidity_workingAir_wet[n],absoluteHumidity_workingAir_wet_argumentList)
        absoluteHumidity_workingAir_wet.append(absoluteHumidity_workingAir_wet_update)

        T_water_argumentList = ()
        T_water_update = waitForConvergence(convergence_factor,update_temperature_water,T_water[n],T_water_argumentList)
        T_water.append(T_water_update)


    return T_productAir,T_workingAir_dry,T_workingAir_wet,absoluteHumidity_workingAir_wet,T_water


def simulateTimeBasedCooling():

    # Get this ready 





