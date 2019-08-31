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

temp_inlet_dry = 308
absHumidity_inlet_dry = 0.024
temp_productAir = 308
temp_water = 293


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

Velocity = 1.16;
m = massflowrate(Velocity)

def update_temperature_productAir(self,argv):
    argv = argv[0]
    h_heat = argv[0]
    dx = argv[1]
    b = argv[2]
    T_water = argv[3]
    m_productAir = argv[4]
    c_productAir = argv[5]
    T_productAir = self 
    
    return ( h_heat*dx*b*(T_productAir - T_water) + m_productAir*c_productAir*T_productAir ) / ( m_productAir*c_productAir ) 

def update_temperature_workingAir_dry(self,argv):
    
    argv = argv[0]
    h_heat = argv[0]
    dx = argv[1]
    b = argv[2]
    T_water = argv[3]
    m_workingAir_dry = argv[4]
    c_productAir = argv[5]
    T_workingAir_dry = self

    return ( h_heat*dx*b*(T_workingAir_dry - T_water) + m_workingAir_dry*c_productAir*T_workingAir_dry  ) / ( m_workingAir_dry*c_productAir )

def update_absoluteHumidity_workingAir_wet(self,argv):
    

    argv = argv[0]
    h_mass = argv[0]
    dx = argv[1]
    b = argv[2]
    w_saturated_wet = argv[3]
    m_workingAir_wet = argv[4]
    w_workingAir_wet = self
    print(argv) 
    return ( h_mass*dx*b*(w_saturated_wet - w_workingAir_wet) + m_workingAir_wet*w_workingAir_wet  ) / ( m_workingAir_wet )

def update_temperature_workingAir_wet(self,argv): 
    argv = argv[0]
    print(argv)
    h_heat = argv[0]
    dx = argv[1]
    b = argv[2]
    T_water = argv[3]
    h_mass = argv[4]
    iv = argv[5]
    w_saturated_wet = argv[6]
    w_workingAir_wet = argv[7]
    T_workingAir_wet = argv[8]
    m_workingAir_dry = argv[9]
    c_productAir = argv[10]
    T_workingAir_wet = self
    
    return ( h_heat*dx*b*(T_water-T_workingAir_wet) + h_mass*(dx)*b*iv*(w_saturated_wet - w_workingAir_wet) + T_workingAir_wet*m_workingAir_dry*c_productAir) / (m_workingAir_dry*c_productAir)

# This function will be changed to change in temperature of water in the system

def update_temperature_water(self,argv_list):
  
    argv = argv_list[0]
    print(argv)
    c_water = argv[0]
    w_saturated_wet = argv[1]
    w_workingAir_wet = argv[2]
    m_productAir = argv[3]
    c_productAir = argv[4]
    dT = argv[5]
    iv = argv[6]
    m_water = argv[7]
    T_workingAir_wet = argv[8]
    m_workingAir_dry = argv[9]
    c_productAir = argv[10]
    m_workingAir_wet = argv[11]
    T_water = self
     
    return (-1. * ((c_water*(w_saturated_wet - w_workingAir_wet)*T_water) + (m_productAir*c_productAir*dT) + (m_workingAir_wet*iv*(w_saturated_wet - w_workingAir_wet))) + (c_water*m_water*T_water)) / (c_water*T_water)

def waitForConvergence(convergence_factor,function,seed,*argv):
    
    parameter_list = argv
    value1 = function(seed,argv)
    value2 = function(value1,argv)

    if  abs((value1 - value2)/value1) > convergence_factor :
        return waitForConvergence(convergence_factor,function,value2,argv)
    else:
        return value2


# Simulations 

# TODO: make a matrix to solve the equation and the use the internal loop for calculating the value of the values


def simulate(steps,convergence_factor,initalCondition):

    initalCondition = initalCondition[0]
    
    length_channel = initalCondition[6]
    dx = length_channel/steps 
    T_productAir = [initalCondition[0]]
    T_workingAir_dry = [initalCondition[1]]
    T_workingAir_wet = [initalCondition[2]]
    w_workingAir_wet = [initalCondition[3]]
    T_water = [initalCondition[4]]
    h_heat = initalCondition[5]
    
    b = initalCondition[7]
    #T_water = [initalCondition[8]]
    h_mass = initalCondition[8]
    iv = initalCondition[9]
    w_saturated_wet = initalCondition[10]
    #w_workingAir_wet = [initalCondition[12]]
    #T_workingAir_wet = [initalCondition[13]]
    m_workingAir_dry = initalCondition[11]
    c_productAir = initalCondition[12]
    m_productAir = initalCondition[13]
    c_water = initalCondition[14]
    m_water = dx*b

    for n in range(steps):
        T_workingAir_dry_argumentList = ( h_heat,dx,b,T_water,m_workingAir_dry,c_productAir )
        T_workingAir_dry_update = waitForConvergence(convergence_factor,update_temperature_workingAir_dry,T_workingAir_dry[n],T_productAir_argumentList) 
        T_workingAir_dry.append(T_workingAir_dry_update)

    m_workingAir_wet = m_workingAir_dry
    
    for n in range(steps):
   
        m_productAir = 91.6*0.00001
        T_productAir_argumentList = ( h_heat,dx,b,T_water[n],m_productAir,c_productAir )
        T_productAir_update = waitForConvergence(convergence_factor,update_temperature_productAir,T_productAir[n],T_productAir_argumentList)
        T_productAir.append(T_productAir_update)
     
        #Calculate m_workingAir_wet
        
        w_workingAir_wet_argumentList = (h_heat,dx,b,w_saturated_wet,m_workingAir_wet)
        w_workingAir_wet_update = waitForConvergence(convergence_factor,update_absoluteHumidity_workingAir_wet,w_workingAir_wet[n],w_workingAir_wet_argumentList)
        w_workingAir_wet.append(w_workingAir_wet_update)
        m_workingAir_wet = m_workingAir_wet +((w_saturated_wet - w_workingair_wet)*dx*0.05*0.005)
        
        T_workingAir_wet_argumentList = ( h_heat,dx,b,T_water[n],h_mass,iv,w_saturated_wet,w_workingAir_wet[n],T_workingAir_wet[n],m_workingAir_dry,c_productAir)
        T_workingAir_wet_update = waitForConvergence(convergence_factor,update_temperature_workingAir_wet,T_workingAir_wet[n],T_workingAir_wet_argumentList)
        T_workingAir_wet.append(T_workingAir_wet_update)

        # Calculate m_water
        
        T_water_argumentList = (c_water,w_saturated_wet,w_workingAir_wet[n],m_productAir,c_productAir,T_productAir[n+1]-T_productAir[n],iv,m_water,T_workingAir_wet[n],m_workingAir_dry,c_productAir,m_workingAir_wet)
        T_water_update = waitForConvergence(convergence_factor,update_temperature_water,T_water[n],T_water_argumentList)
        T_water.append(T_water_update)
        m_water = m_water +((w_saturated_wet - w_workingair_wet)*dx*0.05*0.005)

    return T_productAir,T_workingAir_dry,T_workingAir_wet,w_workingAir_wet,T_water,m_productAir 


#Check the parameters again as few of them are added to check wheather calculation are working or not
print (simulate(10,1,308,308,308,0.024,293,0.026,0.5,0.05,0.027,2.26e6 ,0.03,91.6e-5,1007,12,10))

def simulateTimeBasedCooling(number_channel,timeDivision,duration_inMin,volumn_room,water_temp,temp_room,humidity_room,*initalCondition):
   
    # Write the variable about the area of cross section of channel that will be used to release air into the room
    global area = 0.05*0.005
    global velocity_air_intake = 3

    timeDuration = 1/timeDivision
    indexes = range(timeDivision*60*duration_inMin)
    total_volume_exchange = area*number_channel*velocity_air_intake*timeDuration 

    # Constants
    '''
    length_channel = initalCondition[6]
    dx = length_channel/steps 
    T_productAir = initalCondition[0]
    T_workingAir_dry = initalCondition[1]
    T_workingAir_wet = initalCondition[2]
    w_workingAir_wet = initalCondition[3]
    T_water = initalCondition[4]
    h_heat = initalCondition[5]
    
    b = initalCondition[7]
    #T_water = [initalCondition[8]]
    h_mass = initalCondition[8]
    iv = initalCondition[9]
    w_saturated_wet = initalCondition[10]
    #w_workingAir_wet = [initalCondition[12]]
    #T_workingAir_wet = [initalCondition[13]]
    m_workingAir_dry = initalCondition[11]
    c_productAir = initalCondition[12]
    m_productAir = initalCondition[13]
    c_water = initalCondition[14]
    '''

    # variable to store the output
    T_productAir_allTime = []
    T_workingAir_dry_allTime = []
    T_workingAir_wet_allTime = []
    w_workingAir_wet_allTime = []
    T_water_allTime = []
    

    for i in indexes:
        #Simulations Variables
        T_productAir_temp,T_workingAir_dry_temp,T_workingAir_wet_temp,w_workingAir_wet_temp,T_water_temp,m_flowRate =     simulate(100,0.01,initalCondition) 

        # saveVariables form the simulation
        T_productAir_allTime.append(T_productAir_temp)
        T_workingAir_dry_allTime.append(T_workingAir_dry)
        T_workingAir_wet_allTime.append(T_workingAir_wet_temp)
        w_workingAir_wet_allTime.append(w_workingAir_wet_temp)
        T_water_allTime.append(T_water_temp)

    
        #modifing the inital condition for next step of simulation
        initalCondition[0]= cool_room(m_flowRate,(n+1)*timeDuration,volume_room,T_productAir[-1],temp_room)


    np.savetxt('output/T_productAir',np.array(T_productAir_allTime))
    np.savetxt('output/T_workingAir_dry',np.array(T_workingAir_dry_allTime))
    np.savetxt('output/T_workingAir_wet',np.array(T_workingAir_wet_allTime))
    np.savetxt('output/w_workingAir_wet',np.array(w_workingAir_wet_allTime))
    np.savetxt('output/T_water',np.array(T_water_allTime))


    print("Simulation executed successfully")

# Make global variable given below in the function


def cool_room(m_flowrate,duration,volumn_room,temp_airOut, temp_room):
    global heat_capacity_air
    global density
    
    Final_temp = ( volumn_room*density*heat_capacity_air*temp_room +m_flowrate*duration*heat_capacity_air*temp_airOut ) / (volumn_room*density*heat_capacity_air + m_flowrate*duration*heat_capacity_air)
    return Final_temp
  
simulateTimeBasedCooling(110,2,900,53.11904,293,308,0.024,*initialCondition)
