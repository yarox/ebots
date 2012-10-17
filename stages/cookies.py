from morse.builder.morsebuilder import *


devices = []

robot = Robot('atrv')
robot.name = 'robot_0'
robot.translate(x=0, y=0, z=0.2)

motion = Actuator('v_omega')
motion.name = 'actuator_motion_0_0'
devices.append(motion)

waypoint = Actuator('waypoint')
waypoint.name = 'actuator_waypoint_0_0'
waypoint.properties(Speed=0)
devices.append(waypoint)

proximity = Sensor('proximity')
proximity.name = 'sensor_proximity_0_0'
proximity.properties(Range=0.5, Track='cookie')
proximity.translate(x=0, y=0, z=0.9)
devices.append(proximity)

sensorL = Sensor('sick-ld-mrs')
sensorL.name = 'sensor_ranger_L_0'
sensorL.translate(x=0.2, y=0.3, z=0.5)
sensorL.rotate(z=0.523)
sensorL.properties(Visible_arc=True, resolution=1, scan_window=60,
                   laser_range=5)
sensorL.create_sick_arc()
devices.append(sensorL)

sensorR = Sensor('sick-ld-mrs')
sensorR.name = 'sensor_ranger_R_0'
sensorR.translate(x=0.2, y=-0.3, z=0.5)
sensorR.rotate(z=-0.523)
sensorR.properties(Visible_arc=True, resolution=1, scan_window=60,
                   laser_range=5)
sensorR.create_sick_arc()
devices.append(sensorR)

for device in devices:
    robot.append(device)
    device.configure_mw('socket')

for i in range(-4, 5, 1):
    puck = PassiveObject('props/ebots.blend', 'Puck')
    puck.properties(cookie=True)
    puck.translate(x=i, y=4, z=0)

for i in range(-4, 5, 1):
    puck = PassiveObject('props/ebots.blend', 'Puck')
    puck.properties(cookie=True)
    puck.translate(x=i, y=-4, z=0)

for i in range(-4, 5, 1):
    puck = PassiveObject('props/ebots.blend', 'Puck')
    puck.properties(cookie=True)
    puck.translate(x=-4, y=i, z=0)

for i in range(-4, 5, 1):
    puck = PassiveObject('props/ebots.blend', 'Puck')
    puck.properties(cookie=True)
    puck.translate(x=4, y=i, z=0)

env = Environment('custom/cookies')
env.place_camera([0, 0, 15])
env.aim_camera([0, 0, 0])
