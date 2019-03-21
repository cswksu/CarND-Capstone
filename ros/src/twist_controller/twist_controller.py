
GAS_DENSITY = 2.858
ONE_MPH = 0.44704


class Controller(object):
    def __init__(self, vehParams):
        vehicle_mass = vehParams[0]
        fuel_capacity = vehParams[1]
        brake_deadband = vehParams[2]
        decel_limit = vehParams[3]
        accel_limit = vehParams[4]
        wheel_radius = vehParams[5]
        wheel_base = vehParams[6]
        steer_ratio = vehParams[7]
        max_lat_accel = vehParams[8]
        max_steer_angle = vehParams[9]
        
        #calculate vehicle mass with fuel
        vehicle_net_mass = vehicle_mass+fuel_capacity * GAS_DENSITY

    def control(self, current_velocity, proposed_linear_velocity, proposed_angular_velocity, drive_by_wire_enabled):
        # TODO: Change the arg, kwarg list to suit your needs
        # Return throttle, brake, steer
        return 1., 0., 0.
