from morse.builder.morsebuilder import *


devices = []

robot = Robot('atrv')
robot.name = 'robot_0'
robot.translate(x=-6.0, y=0, z=0.2)

motion = Actuator('v_omega')
motion.name = 'actuator_motion_0_0'
devices.append(motion)

waypoint = Actuator('waypoint')
waypoint.name = 'actuator_waypoint_0_0'
waypoint.properties(Speed=0)
devices.append(waypoint)

proximity = Sensor('proximity')
proximity.name = 'sensor_proximity_0_0'
proximity.properties(Range=0.35, Track='cookie')
proximity.translate(x=0, y=0, z=0.9)
devices.append(proximity)

control = Actuator('keyboard')
control.properties(Speed=3.0)
devices.append(control)

for device in devices:
    robot.append(device)
    device.configure_mw('socket')

for x, y in eval(open('random.txt').read()):
    puck = PassiveObject('props/ebots.blend', 'Puck')
    puck.properties(cookie=True)
    puck.translate(x=x, y=y, z=0)

env = Environment('custom/base')
env.place_camera([0, 0, 30])
env.aim_camera([0, 0, 0])
