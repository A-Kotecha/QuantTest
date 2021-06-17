#!/usr/bin/env python
# -*- coding: utf-8 -*-



from __future__ import print_function
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal
import numpy as np

# Set up option parsing to get connection string
import argparse
parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--connect',
                    help="Vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect
sitl = None
vehicle = connect('127.0.0.1:14550', wait_ready=True) #'Connects to ArduPilot
'''
# Start SITL if no connection string specified
if not connection_string:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()


# Connect to the Vehicle
print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True)
'''
def pos2meters(lon, lat, h): #frame conversion to get correct units from Global Frame to meters
    R_eq = 6378.137e3
    f = 1/298.257223563
    e2 = f*(2-f)
    CosLat = np.cos(np.radians(lat))
    SinLat = np.sin(np.radians(lat))
    N = R_eq/np.sqrt(1-e2*SinLat**2)
    r = np.zeros(3)
    r[0] = (N + h) * SinLat * np.cos(np.radians(lon))
    r[1] = (N + h) * CosLat * np.sin(np.radians(lon))
    r[2] = h
    return r

def meters2pos(x): # Meters --> Global Frame
    r = np.array([0.00001*x[0],0.00001*x[1],x[2]])
    return r

def arm_and_takeoff(aTargetAltitude): #Arming and Takeoff vehicle of drone


    print("Basic pre-arm checks") # Don't try to arm until autopilot is ready, will say when GPS is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors") # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)


arm_and_takeoff(10)


print("Set default/target airspeed to 4")
vehicle.airspeed = 4
eps = 0.2

def go_to(waypoints):
    wp = []
    for k in waypoints:
        wp.append(meters2pos(k))
    wp = np.array(wp)
    for i in wp:
        while True:
            point = LocationGlobalRelative(i[0],i[1],i[2])
            # Break and return from function just below target altitude.
            vehicle.simple_goto(point)
            x, y, z = pos2meters(vehicle.location.global_relative_frame.lon, vehicle.location.global_relative_frame.lat,
                                 vehicle.location.global_relative_frame.alt)
            xp, yp, zp = pos2meters(point.lon, point.lat, point.alt)
            print(" Position: " + "x: " + str(x) + " y: " + str(y) + " z: " + str(z))
            if (np.sqrt((x - xp) ** 2 + (y - yp) ** 2 + (z - zp) ** 2)) <= eps:
                print("Reached target point !")
                break
            time.sleep(1)

waypoints=[[8,5,5],[4,-5,15],[-10,-5,10],[-10,5,20]]
go_to(waypoints)


# sleep so we can see the change in map
time.sleep(6)

print("Returning to Launch")
vehicle.mode = VehicleMode("RTL")

# Close vehicle object before exiting script
print("Close vehicle object")
vehicle.close()

# Shut down simulator if it was started.
if sitl:
    sitl.stop()
