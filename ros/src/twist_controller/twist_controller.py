
GAS_DENSITY = 2.858
ONE_MPH = 0.44704

from yaw_controller import YawController

class Controller(object):
    def __init__(self, vehParams):
        self.vehicle_mass = vehParams[0]
        self.fuel_capacity = vehParams[1]
        self.brake_deadband = vehParams[2]
        self.decel_limit = vehParams[3]
        self.accel_limit = vehParams[4]
        self.wheel_radius = vehParams[5]
        self.wheel_base = vehParams[6]
        self.steer_ratio = vehParams[7]
        self.max_lat_accel = vehParams[8]
        self.max_steer_angle = vehParams[9]
        
        
        
        self.steer_c=YawController(self.wheel_base, self.steer_ratio, 0.1, self.max_lat_accel, self.max_steer_angle)
        
        #calculate vehicle mass with fuel
        self.vehicle_net_mass = self.vehicle_mass+self.fuel_capacity * GAS_DENSITY

    def control(self, current_velocity, proposed_linear_velocity, proposed_angular_velocity, drive_by_wire_enabled):
        # TODO: Change the arg, kwarg list to suit your needs
        # Return throttle, brake, steer
        
        #if !drive_by_wire_enabled:
            #set all integral terms to zero for PID controllers
        steer = 0
        throt=0
        brake=0
        
        if proposed_linear_velocity and proposed_angular_velocity and current_velocity:
            steer = self.steer_c.get_steering(proposed_linear_velocity, proposed_angular_velocity, current_velocity)
        
        return throt, brake, steer
