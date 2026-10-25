import numpy as np
import matplotlib.pyplot as plt

#pingpong ball properties
mass = 0.0027 #kg
radius = 0.02 #m
air_density = 1.184 #kg/m^3
gravity = 9.81 #m/s^2

#vector of velocity x = forward, y = sideways, lateral, z = vertical
velocity = np.array([5.0, 0.0, 0.0])

#initial position vector (a table that's 1.0m tall)
position = np.array([0.0, 0.0, 1.0])

area = np.pi * radius**2 #cross sectional area of the ball
kinematic_viscosity = 15.52e-6 #m^2/s air at room T
diameter = 2 * radius

#speed calculation
speed = np.linalg.norm(velocity)

#Input different speeds to check the Reynolds number
def reynolds_number(speed, diameter, kinematic_viscosity):
    return (speed * diameter) / kinematic_viscosity

test_speeds = [5.0, 8.0, 12.0, 20.0]

for v in test_speeds:
    Re = reynolds_number(v, diameter, kinematic_viscosity)
    print(Re)


#drag coefficient
def drag_coefficient(spin_parameter):
    S_points  = [0.37, 0.75, 1.12, 1.50, 1.88, 2.26]
    Cd_points = [0.500, 0.600, 0.577, 0.579, 0.589, 0.589]
    return np.interp(spin_parameter, S_points, Cd_points)

#drag force
def drag_force(velocity, omega, air_density, area, radius):
    speed = np.linalg.norm(velocity)
    if speed < 1e-9:
        return np.array([0.0, 0.0, 0.0])

    spin_parameter = radius * omega / speed
    Cd = drag_coefficient(spin_parameter)
    force = -0.5 * air_density * Cd * area * speed * velocity
    return force




#Magnus Force
def lift_coefficient(spin_parameter):
    S_points  = [0.37, 0.75, 1.12, 1.50, 1.88, 2.26]
    Cl_points = [0.274, 0.340, 0.269, 0.343, 0.376, 0.395]
    return np.interp(spin_parameter, S_points, Cl_points)


def magnus_force(velocity, omega, air_density, area, radius):
    speed = np.linalg.norm(velocity)
    if speed < 1e-9:
        return np.array([0.0, 0.0, 0.0])


    spin_parameter = radius * omega / speed
    Cl = lift_coefficient(spin_parameter)


    omega_vector = np.array([0.0, 0.0, omega])
    direction = np.cross(omega_vector, velocity)
    direction_norm = np.linalg.norm(direction)


    if direction_norm < 1e-9:
        direction_normalized = np.array([0.0, 0.0, 0.0])
    else:
        direction_normalized = direction / direction_norm


    force = 0.5 * air_density * Cl * area * speed**2 * direction_normalized
    return force

#acceleration
def get_acceleration(velocity, omega, mass, air_density, area, gravity):
    F_drag = drag_force(velocity, omega, air_density, area, radius)
    F_magnus = magnus_force(velocity, omega, air_density, area, radius)
    F_gravity = np.array([0.0, 0.0, -mass * gravity])
    F_total = F_drag + F_magnus + F_gravity
    return F_total / mass

#For other omega values
def simulate(omega):
    velocity = np.array([5.0, 0.0, 0.0])
    position = np.array([0.0, 0.0, 1.0])
    dt = 0.0001
    

    while position [2] > 0:
        acceleration = get_acceleration(velocity, omega, mass, air_density, area, gravity)
        velocity = velocity + acceleration * dt
        position = position + velocity * dt

    return position[1]


#range of omega values
omega_values = np.linspace(100,500,51) # 51 evenly spaced values from 100 to 500 rad/s
displacements = []


for w in omega_values:
    result = simulate(w)
    displacements.append(result)


#plotting on graph and table (omega vs lateral displacement)
print(f"{'Omega (rad/s)':>15} | {'Lateral displacement (m)':>25}")
for w, d in zip(omega_values, displacements):
    print(f"{w:>15} | {d:>25}")

plt.savefig("lateral_displacement_plot.png", dpi=200)

plt.plot(omega_values, displacements, marker ='o')
plt.xlabel("Angular velocity (rad/s)")
plt.ylabel("Lateral displacement (m)")
plt.title("Lateral displacement vs angular velocity")
plt.grid(True)
plt.show()





