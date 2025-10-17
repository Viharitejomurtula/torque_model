import matplotlib.pyplot as plt
import matplotlib.animation as animation
from dataclasses import dataclass    #container for data
import numpy as np

@dataclass       
class State:
    xpos : float
    ypos : float
    xvel : float
    rpm  : float
    heading : float 
    
deltaT = 0.1
m=798  #mass of car
radius = 0.67   #radius of car tire
p_max = 74000  #maximum power output in Watts
rpm_max = 74000  #max rpm of car
g_r = 10  #gear ratio thing

def motor_torque(rpm, P_max=p_max, rpm_max=rpm_max):
    # approximate torque curve: high at low rpm, fades near redline
    torque = (1 - rpm / rpm_max) * (P_max / (rpm_max * 2 * np.pi / 60))
    if torque < 0:
        torque = 0
    return torque

def step (state:State) -> State:
    wheel_rpm = (state.xvel / (2 * np.pi * radius)) * 60
    motor_rpm = wheel_rpm * g_r
    tau_motor = motor_torque(motor_rpm)
    tau_wheel = tau_motor * g_r
    acc_x = tau_wheel / (radius * m)             
    new_v = state.xvel + acc_x * deltaT
    yaw_rate = 0.1        
    new_heading = state.heading + yaw_rate * deltaT
    new_x = state.xpos + new_v * np.cos(new_heading) * deltaT
    new_y = state.ypos + new_v * np.sin(new_heading) * deltaT

    return State(xpos=new_x, ypos=new_y, xvel=new_v, rpm=motor_rpm, heading=new_heading)

def animate (i):
    global s0
    s0 = step(s0)
    ax.clear()
    ax.scatter([s0.xpos], [s0.ypos], s = 300, color = 'red')
    ax.set_xlim(0,50)
    ax.set_ylim(0,50)
    ax.set_title("Torque of the car")
    return ax

s0 = State(
    xpos = 0,
    ypos = 2,
    xvel = 0,
    rpm = 0,
    heading=0
)

fig, ax = plt.subplots(figsize=(4,3), dpi=150)
ani = animation.FuncAnimation(fig, animate, interval=50)
plt.show()
