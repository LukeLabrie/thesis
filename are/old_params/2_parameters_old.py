import numpy as np
import pandas as pd
import math

###############################################################################
# constants
###############################################################################
pi = math.pi
R = 8.314            # ideal gas constant
m_H = 0.004          # molar mass of helium (kg/mol)
P = 2.12             # steady-state power (MW) ORNL-1845 pg. 58
L_eff = 93.65/3.281  # effective tube length of hx's (m) ORNL-1535 pg. 47
V_p_hx = (L_eff/1550)*(math.pi*((1.0/2)-0.109)**2)/2 # volume in hx tubes (m^3) ORNL-1535 pg. 47
rho_inconel = 8.5*1000          # inconel density (kg/m^3)
scp_t = 4.44e-4                 # specific heat capacity of inconel 600 (MJ/kg-C) (https://www.specialmetals.com/documents/technical-bulletins/inconel/inconel-alloy-600.pdf)
V_t_hx = ((L_eff/1550)*math.pi*((1.0/2))**2 - V_p_hx)/2 # tube volume in heat exchangers
rho_h = 0.167                                 # helium density (kg/m^3) NEEDS TO BE TEMPERATURE DEPENDENT
#scp_f = 1.9665e-3  # specific heat capacity of fuel salt (MJ/kg-C) ORNL-TM-0728 p.8
scp_f = 0.26*4.1869e-3 # ORNL 1535 p.16
scp_c = 1.256e-3  # specific heat capacity of cooolant (MJ/kg-C) ORNL-1845 p.113
scp_h = 5.1932e-3            # specigic heat capacity of helium (MJ/kg-C)
A_t_hx = (pi*(1.0-2*0.109)*93.65)/144 # hx inner tube area (ft^2) ORNL-1535 p.47  
A_to_hx = (pi*(1.0)*93.65)/144 # hx outer tube area (ft^2) ORNL-1535 p.47  

# delays
tau_hx_c_f = 3.00 # fuel-helium hx to core delay (unknown)
tau_hx_c_c = 3.00 # coolant-helium hx to core delay (unknown)
tau_c_hx_f = 3.00 # coolant-helium hx to core delay (unknown)

# wights
# k_f1 = 0.465        # fractional power generation (fuel)
# k_f2 = 0.465        # fractional power generation (fuel)
k_f1 = 0.5        # fractional power generation (fuel)
k_f2 = 0.5        # fractional power generation (fuel)
k_b = 1-(k_f1+k_f2) # fractional power generation (beryllium)
k_1 = 0.5
k_2 = 1-k_1

# NEUTRONICS DATA
tau_l = 16.73  # ORNL-TM-0728 %16.44; % (s)
tau_c = 8.46  # ORNL-TM-0728 %8.460; % (s)
n_frac0 = 1.0  # initial fractional neutron density n/n0 (n/cm^3/s)
# Lam = 2.400E-04  # mean generation time ORNL-TM-1070 p.15 U235
Lam = 2.400E-04  # mean generation time ORNL-TM-1070 p.15 U235
# Lam = 4.0E-04;  # mean generation time ORNL-TM-1070 p.15 U233
lam = np.array([1.240E-02, 3.05E-02, 1.11E-01, 3.01E-01, 1.140E+00, 3.014E+00])
beta = np.array([0.000223, 0.001457, 0.001307, 0.002628, 0.000766, 0.00023])  # U235
# beta = np.array([0.00023, 0.00079, 0.00067, 0.00073, 0.00013, 0.00009])  # U233
beta_t = np.sum(beta)  # total delayed neutron fraction MSRE
rho_0 = beta_t-sum(np.divide(beta,1+np.divide(1-np.exp(-lam*tau_l),lam*tau_c))) # reactivity change in going from stationary to circulating fuel
C0 = beta / Lam * (1.0 / (lam - (np.exp(-lam * tau_l) - 1.0) / tau_c))


#################################
# functions
#################################
def iwc_to_Pa(h20):
    '''
    Inches water column -> Pa
    '''
    return h20*248.8

def cfm_to_m3s(v):
    '''
    Cubic ft/min -> m3/s
    '''
    return v/2119

# fuel density (kg/m^3) ORNL-1845 pg. 113
def fuel_density(temp):
    return 1000*3.98-0.00093*temp


# F to K conversion
def F_to_K(tempF):
    return (tempF-32)*5/9+273.15

def mass_flow(m,P,V,T):
    '''
    m: molar mass of gas
    P: pressure
    V: volume
    T: temperature
    '''
    return m*P*V/(R*T)       # helium mass flow (kg/s)



###############################################################################
# core
###############################################################################

# thermal feedback (1/Kelvin, temperature provided in Kelvin) ORNL-1845 pg. 115
a_f = (-9.8e-5)*5/9
a_b = (1.1e-5)*5/9

# operating conditions taken from 25-hr Xenon run Exp. H-8
# temperatures 
T_fuel_avg = F_to_K(1311)       # ORNL 1845 pg. 58

# T0_c_f1 = F_to_K(1150)          # core fuel inlet temp (K) ORNL-1845 pg. 121
# T0_c_f2 = F_to_K(1450)          # core fuel outlet temp (K) could be 1480 if taken from previous page ORNL-1845 pg. 121

T0_c_f1 = F_to_K(1250)          # core fuel inlet temp (K) ORNL-1845 pg. 121
T0_c_f2 = F_to_K(1550)          # core fuel outlet temp (K) could be 1480 if taken from previous page ORNL-1845 pg. 121

T0_c_c1 = F_to_K(1105)          # core coolant inlet temp (K) ORNL-1845 pg. 121
T0_c_c2 = F_to_K(1235)          # core coolant outlet temp (K) ORNL-1845 pg. 121

T0_c_t1 = ((T0_c_f1+T0_c_c1)/2) # core tube temp

T0_c_b = T_fuel_avg             # berylliumi initial temp

# flow rates 
F_c_f = 40/15850       # core fuel flow rate (m^3/s) ORNL-1845 pg. 121
F_c_c = 224/15850      # core coolant flow rate (m^3/s) ORNL-1845 pg. 121

# dimensions
V_fuel = 52071.248849/2e6                  # CAD model (m^3)
A_fuel = (69872.856584/2-(6*6.996))/10000  # CAD model (m^2) 
V_tubes = 5453.961/2e6                     # CAD model (m^3)
A_tubes = (73445.338-(12*7.728))/10000     # CAD model (m^2) 
V_coolant = (248933.207)/2e6            # CAD model (m^3)

# density 
rho_c = 1000*0.78                # coolant density (kg/m^3) 

# mass
m_f_c = fuel_density(T_fuel_avg)*V_fuel
m_c_c = rho_c*V_coolant      # coolant mass (kg)


# mass flow rate 
W_f = F_c_f * fuel_density(T_fuel_avg)   # fuel mass flow rate (kg/s)
W_c = F_c_c * rho_c                      # coolant mass flow rate (kg/s)

# heat transfer
# h_ft = 6.480e-01  # heat transfer*area coefficient from primary to tubes (MW/C) ORNL-TM-1647 p.3

def h_US(C,k,D,R,r,Pr,p):
    '''
    convective heat transfer coefficient BTU/(sec*ft^2*degF) ORNL-1535 p.15
    C: leading coefficient
    k: thermal conductivity BTU/(sec*ft^2)
    D: pipe diameter (ft)
    R: Reynold's modulus
    r: Exponent for Reynold's modulus
    Pr: Prandtl modulus 
    p: Exponent for Prandtl modulus
    '''
    return 0.023*(k/D)*(R**0.8)*(Pr**0.4)

def R_US(u,r,nu):
    '''
    Reynold's Modulus ORNL-1345 p.7
    u: fluid velocity (ft/hr)
    r: pipe radius (ft)
    nu: kinematic viscosity (ft^2/hr)
    '''
    return 2*u*r/nu

def Pr_US(nu,rho,c,k):
    '''
    Prandtl Modulus ORNL-1345 p.7
    nu: kinematic viscosity (ft^2/hr)
    rho: density (lb/ft^3)
    c: heat capacity (Btu/(lb*degF))
    k: thermal conductivity BTU/(hr*ft^2)
    '''
    return nu*rho*c/k

# convective heat transfer coefficient for the core fuel
rho_c_f = 187                           # core fuel density in (lb/ft^3) ORNL-1535 p.16
cp_c_f = 0.26                           # core fuel heat capacity (Btu/(lb*degF)) ORNL-1535 p.16
mu_c_f = 60*60*8.27e-3                  # absolute viscosity of core fuel lb/(hr*ft) ORNL-1535 p.16 
nu_c_f = mu_c_f/rho_c_f                 # kinematic viscosity (ft^2/hr)
d_c_f = 0.097933071                     # fuel pipe diameter (ft) CAD Model
v_c_f = (40*8.02083)/(pi*(d_c_f/2)**2)  # velocity of core fuel (ft/hr) (gpm->ft^3/hr conversion)
k_f_US = 4.17e-4                        # thermal conductivity of the fuel in BTU/(sec*ft^2) ORNL-1535 p.16
k_f_US_hr = 60*60*4.17e-4               # thermal conductivity of the fuel in BTU/(hr*ft^2) ORNL-1535 p.16
R_c_f = R_US(v_c_f,d_c_f/2,nu_c_f)      # Reynold's number for core fuel 
r_c_f = 0.8                             # coefficient on Reynold's modulus
Pr_c_f = Pr_US(nu_c_f,rho_c_f,cp_c_f,k_f_US_hr) # Prandtl modulus core fuel
p_c_f = 0.4                                     # Coefficient on Prandtl's modulus
C_c_f = 0.023                                   # leading coefficient
h_f_US = h_US(C_c_f,k_f_US,d_c_f,R_c_f,r_c_f,Pr_c_f,p_c_f)        # Convective heat transfer coefficient core fuel (BTU/(sec*ft^2*degF))
h_f_US_hr = h_f_US*60*60                        # Convective heat transfer coefficient core fuel (BTU/(hr*ft^2*degF))
h_f_c = ((h_f_US_hr/0.1761)*1e-6)                   # Convective heat transfer coefficient core fuel (MW/(m^2*degC))
hA_f_c = h_f_c*A_fuel

# convective heat transfer coefficient for the core tubes
hA_t_hx_US = 1/0.137 # BTU/(sec*degF) ORNL-1535 p. 47
h_t_US = (hA_t_hx_US/11.15+hA_t_hx_US/8.02)/2 # tube htc (Btu/(sec*ft^2*defF))
hA_t_c_US = h_t_US*A_fuel*10.764
hA_t_c = hA_t_c_US*(5/9)*(1.05504)*(1e-3) 

# fuel-tube coefficient
hA_ft_c = 1/((1/hA_t_c)+(1/hA_f_c))

# coolant
h_c_c_US = 166 # coolant heat transfer coefficient (BTU/(hr*ft^2*defF))
h_c_c = ((h_c_c_US/0.1761)*1e-6)
hA_c_c = h_c_c*A_tubes/2
hA_tc_c = 1/((1/hA_c_c)+(1/hA_t_c))  

m_t     = V_tubes*rho_inconel   # mass of tubes (kg)  
mcp_t_c   = m_t*scp_t;          # from ratio of (A_phe/mcp_t)msbr = (A_phe/mcp_t)msre m_tn*cp_tn; % mass*(heat capacity) of tubes per lump in MW-s/°C 
mcp_f_c = scp_f*m_f_c
mcp_c_c = scp_c*m_c_c 

# moderator 
k_m_US = 0.73 # thermal conductivity of the moderator (Btu/(hr*ft^2)) # ORNL-1535 p.2
scp_m_US = 0.48 # thermal conductivity of the moderator (Btu/(lb*(degF))) # ORNL-1535 p.2

###############################################################################
# fuel-helium heat exchanger
###############################################################################

# initial temperatures
T0_hfh_f1 = F_to_K(1450)   # fuel-helium hx fuel inlet temp (K) ORNL-1845 pg. 121
T0_hfh_f2 = F_to_K(1150)   # fuel-helium hx fuel oulet temp (K) ORNL-1845 pg. 121

T0_hfh_h1 = F_to_K(180)    # fuel-helium hx helium inlet temp (K) ORNL-1845 pg. 121
T0_hfh_h2 = F_to_K(620)    # fuel-helium hx helium outlet temp (K) ORNL-1845 pg. 121

T0_hfh_t1 = ((T0_hfh_f1+T0_hfh_h1)/2) # initial tube temp

# flow rates 
F_hfh_h1 = (7300*2)/15850    # fuel-helium hx helium fuel inlet flow rate (m^3/s) ORNL-1845 pg. 121
F_hfh_h2 = (12300*2)/15850    # fuel-helium hx helium fuel outlet flow rate (m^3/s) ORNL-1845 pg. 121

# mass 
m_f_hx = V_p_hx * fuel_density(T_fuel_avg)

# heat transfer
#hA_f_hx_US = h_f_US*(A_t_hx*10.764)
#hA_t_hx_US = h_t_US*A_t_hx*10.764
hA_f_hx_US = h_f_US*2*(11.15+8.02)
hA_t_hx_US = h_t_US*2*(11.15+8.02)
hA_ft_hx_US = 1/((1/hA_f_hx_US)+(1/hA_t_hx_US))
hA_ft_hx = hA_ft_hx_US*(5/9)*(1.05504)*(1e-3) 

mcp_t_hx = V_t_hx*rho_inconel*scp_t
m_h_hxfh = (((24.75*26.25)/61020)-V_t_hx)*rho_h/2 # hx dimension minus tube volume, factor of two for two nodes

hA_h_US_hx = (0.955+0.800+0.580)/3         # ORNL-1535 p.47 (average)
hA_ht_US_hx = 1/((1/hA_t_hx_US)+(1/hA_h_US_hx))  # BTU/(sec*degF)
hA_th_hx = hA_ht_US_hx*(5/9)*(1.05504)*(1e-3) # MW/C

mcp_f_hx = scp_f*m_f_hx
mcp_h_hxfh = m_h_hxfh*scp_h

# mass flow rates 
P_hfh_h1 = iwc_to_Pa(2.8)
V_hfh_h1 = cfm_to_m3s(7300)
W_hfh_h1 = mass_flow(m_H,P_hfh_h1,V_hfh_h1,F_to_K(180))

P_hfh_h2 = iwc_to_Pa(1.5)
V_hfh_h2 = cfm_to_m3s(12300)
W_hfh_h2 = mass_flow(m_H,P_hfh_h1,V_hfh_h1,F_to_K(620))

###############################################################################
# helium-water heat exchanger (fuel loop)
###############################################################################

# initial temperatures
T0_hhwf_h1 = F_to_K(620)    # helium-water hx (fuel loop) helium inlet temp (K) ORNL-1845 pg. 121
T0_hhwf_h2 = F_to_K(180)    # helium-water hx (fuel loop) helium outlet temp (K) ORNL-1845 pg. 121

T0_hhwf_w1 = F_to_K(70)    # helium-water hx (fuel loop) water inlet temp (K) ORNL-1845 pg. 121 
T0_hhwf_w2 = F_to_K(135)   # helium-water hx (fuel loop) water water outlet temp (K) ORNL-1845 pg. 121

T0_hhwf_t1 = ((T0_hhwf_h1+T0_hhwf_w1)/2)

F_hhwf_h1 = (12300*2)/15850    # helium-water hx helium inlet flow rate (m^3/s) ORNL-1845 pg. 121
F_hhwf_h2 = (7300*2)/15850    # helium-water hx helium outlet flow rate (m^3/s) ORNL-1845 pg. 121

m_h_hxhw = V_p_hx*rho_h

# mass flow rates 
P_hhwf_h1 = iwc_to_Pa(1.5)
V_hhwf_h1 = cfm_to_m3s(12300)
W_hhwf_h1 = mass_flow(m_H,P_hfh_h1,V_hfh_h1,F_to_K(620))

P_hhwf_h2 = iwc_to_Pa(1.2)
V_hhwf_h2 = cfm_to_m3s(7300)
W_hhwf_h2 = mass_flow(m_H,P_hfh_h1,V_hfh_h1,F_to_K(180))

W_hhwf_w = 65/15850                # water flow (m^3/s)
m_w = (((24.75*26.25)/61020)-V_t_hx)*998/2 
scp_w = 4.181e-3
mcp_w = m_w*scp_w
mcp_h_hxhw = m_h_hxhw*scp_h

hA_h_US_hxhw = (3.22+2.37+1.40)/3 # ORNL-1535 p.47
hA_w_US_hxhw = (30.8+22.8+12.5)/3 # ORNL-1535 p.47
hA_t_US_hxhw = 1/0.00456          # ORNL-1535 p.47

hA_ht_US_hxhw = 1/((1/hA_h_US_hxhw)+(1/hA_t_US_hxhw))
hA_tw_US_hxhw = 1/((1/hA_w_US_hxhw)+(1/hA_t_US_hxhw))

hA_ht_hxhw = hA_ht_US_hxhw*(5/9)*(1.05504)*(1e-3)
hA_tw_hxhw = hA_tw_US_hxhw*(5/9)*(1.05504)*(1e-3) 

###############################################################################
# coolant-helium heat exchanger 
###############################################################################

# initial temperatures
T0_hch_c1 = F_to_K(1235)  # coolant-helium hx coolant inlet temp (K) ORNL-1845 pg. 121 
T0_hch_c2 = F_to_K(1105)  # coolant-helium hx coolant outlet temp (K) ORNL-1845 pg. 121 

T0_hch_h1 = F_to_K(170)  # coolant-helium hx helium inlet temp (K) ORNL-1845 pg. 122 
T0_hch_h2 = F_to_K(1020)  # coolant-helium hx helium outlet temp (K) ORNL-1845 pg. 122 

T0_hch_t1 = ((T0_hch_c1+T0_hch_h1)/2)

# heat transfer parameters
m_c_hx = V_p_hx * rho_c
mcp_h_c = m_c_hx*scp_c      

# mass flow rates 
P_hch_h1 = iwc_to_Pa(4)
V_hch_h1 = cfm_to_m3s(2000)
W_hch_h1 = mass_flow(m_H,P_hfh_h1,V_hfh_h1,F_to_K(170))

P_hch_h2 = iwc_to_Pa(2)
V_hch_h2 = cfm_to_m3s(4700)
W_hch_h2 = mass_flow(m_H,P_hfh_h1,V_hfh_h1,F_to_K(1020))

hA_c_hx_US = h_c_c_US*A_to_hx*10.764
hA_ct_US_hx = 1/((1/hA_c_hx_US)+(1/hA_t_hx_US))  # BTU/(sec*degF)
hA_ct_hx = hA_ct_US_hx*(5/9)*(1.05504)*(1e-3) # MW/C

###############################################################################
# helium-water heat exchanger (coolant loop) 
###############################################################################

# initial temperatures 
T0_hhwc_h1 = F_to_K(1020)    # helium-water hx (coolant loop) helium inlet temp (K) ORNL-1845 pg. 122
T0_hhwc_h2 = F_to_K(170)    # helium-water hx (coolant loop) helium outlet temp (K) ORNL-1845 pg. 122

T0_hhwc_w1 = F_to_K(70)    # helium-water hx (coolant loop) water inlet temp (K) ORNL-1845 pg. 121 
T0_hhwc_w2 = F_to_K(100)   # helium-water hx (coolant loop) water water outlet temp (K) ORNL-1845 pg. 121

T0_hhwc_t1 = ((T0_hhwc_h1+T0_hhwc_w1)/2)

# mass flow rates
P_hhwc_h1 = iwc_to_Pa(2.0)
V_hhwc_h1 = cfm_to_m3s(4700)
W_hhwc_h1 = mass_flow(m_H,P_hfh_h1,V_hfh_h1,F_to_K(1020))

P_hhwc_h2 = iwc_to_Pa(0.0)
V_hhwc_h2 = cfm_to_m3s(2000)
W_hhwc_h2 = mass_flow(m_H,P_hfh_h1,V_hfh_h1,F_to_K(170))

W_hhwc_w = 77/15850  














