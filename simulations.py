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

def massflowrate(Velocity):
return Velocity*0.05*0.005*1.1368

# Initial Condition

temp_inlet_dry = 35
absHumidity_inlet_dry = 0.024
temp_productAir = 35
temp_water = 20


# Geometrical Parameters 

height = 0.05
length = 0.5
width = 0.005

# Simulation Parameters

steps = 100
convergence = 0.001

# Looping function to simulate the value

'''
    Mass flow rate : m 
    Specific Heat Capacity : c
    Absoulte Humidity : w
    Latent heat of vaporisation : iv
    Velocity of air input : Velocity

    Assumptions :
    1. Temperature of water is maintained using a thermocouple implies (temperature of water remains same)
    2. Channel is divided into 100 lenghts(dx)
    3. Error for convergence is less than 0.001
    
'''

Velocity;
m = massflowrate(Velocity)

def update_temperature_productAir(self,argv_list):
    h_heat = argv[0],
    dx = argv[1],
    b = argv[2],
    T_water = argv[3],
    m_productAir = argv[4],
    c_productAir = argv[5]
    self = T_productAir
    
    return ( h_heat*dx*b*(T_productAir - T_water) + m_productAir*c_productAir*T_productAir ) / ( m_productAir*c_productAir ) 

def update_temperature_workingAir_dry(self,argv_list):
    h_heat = argv[0],
    dx = argv[1],
    b = argv[2],
    T_water = argv[3],
    m_workingAir_dry = argv[4],
    c_productAir = argv[5]
    self = T_workingAir_dry

    return ( h_heat*dx*b*(T_workingAir_dry - T_water) + m_workingAir_dry*c_productAir*T_workingAir_dry  ) / ( m_workingAir_dry*c_productAir )

def update_absoluteHumidity_workingAir_wet(self,argv_list):
    
    h_heat = argv[0],
    dx = argv[1],
    b = argv[2],
    w_saturated_wet = argv[3],
    m_workingAir_wet = argv[4],
    self = w_workingAir_wet
    
    return ( h_mass*dx*b*(w_saturated_wet - w_workingAir_wet) + m_workingAir_wet*w_workingAir_wet  ) / ( m_workingAir_wet )

def update_temperature_workingAir_wet(self,argv_list):
    
    h_heat = argv[0],
    dx = argv[1],
    b = argv[2],
    T_water = argv[3],
    h_mass = argv[4],
    iv = argv[5],
    w_saturated_wet = argv[6],
    w_workingAir_wet = argv[7],
    T_workingAir_wet = argv[8],
    m_workingAir_dry = argv[9],
    c_productAir = argv[10]
    self = T_workingAir_wet
    
    return ( h_heat*dx*b*(T_water-T_workingAir_wet) + h_mass*(dx)*b*iv*(w_saturated_wet - w_workingAir_wet) + T_workingAir_wet*m_workingAir_dry*c_productAir) / (m_workingAir_dry*c_productAir)

# This function will be changed to change in temperature of water in the system

def update_temperature_water(self,argv_list):
    
    c_water = argv[0],
    w_saturated_wet = argv[1],
    w_workingAir_wet = argv[2],
    m_productAir = argv[3],
    c_productAir = argv[4],
    dT = argv[5],
    iv = argv[6],
    m_water = argv[7],
    T_workingAir_wet = argv[8],
    m_workingAir_dry = argv[9],
    c_productAir = argv[10]
    self = T_water
    
    return (-1. * ((c_water*(w_saturated_wet - w_workingAir_wet)*T_water) + (m_productAir*c_productAir*dT) + (m_workingAir_wet*iv*(w_saturated_wet - w_workingAir_wet))) + (c_water*m_water*T_water)) / (c_water*T_water)

def waitForConvergence(convergence_factor,function,seed,*argv):
    
    parameter_list = argv
    value1 = function(seed,argv)
    value2 = function(value1,argv)

    if  abs((value1 - value2)/value1) > convergence_factor
        return waitForConvergence(convergence_factor,function,value2,argv)
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





