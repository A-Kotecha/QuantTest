# QuantTest
# QuantumAviationTest

ArduPilot with SITL, Gazebo 9, ROS Melodic and DroneKit with SITL is expected to have been installed beforehand. As well as MAVROS and MAVLink dependacies.

ROS version: Melodic

OS: Ubuntu 18.04

Language: Python 3 (however Python 2 & C++ also needs to be installed natively on the PC)

Use ` conda create --name py27 python=2.7` if SITL does not work to switch to Python 2. To switch to python 2 write `conda activate py27` to switch back to base  `conda activate base`

---


1. Git clone file first

2. If catkin workspaces havent been used before in PC being used:

`sudo apt-get install python-wstool python-rosinstall-generator python-catkin-tools`


Then install the necessary dependancies. Then do:

`cd Quant/catkin_ws`

`catkin build` 

If asked to `catkin clean -b` do so and then run `catkin build` again


3. On a Terminal launch the runway simulation in Gazebo:

`roslaunch iq_sim runway.launch --screen`

4. On a new terminal to run ArduCopter:

`cd QuantumAviation`

` ~/startsitl.sh `

5. On a new terminal launch Mavors

`cd`

`roslaunch iq_sim apm.launch --screen `

6. On a new terminal run Python Script

`cd Quant/src/src2/scripts`

`python Quant_AranKotecha.py`


---
Answers to Questions

Q1. Testing Plan?

A1. A good reason to use ROS is the modular nature of it. This allows each node to be tested independently from other nodes in an independent synthetic environment so that the node can be validated and verified independently. This stage is Software in the loop development before processing to processor in the loop the software must be tested thoroughly. The drone of course would have to be tested for good conditions, bad conditions as well as bad data inputs as suggested. There would also have to be testing for how the drone will act when a goal is no longer possible, or becomes more complicated, such as if an object were blocking its route. How the drone acts when its actions are interrupted should also be tested, for example if a command was sent to it during the middle of the execution of another task. Be that from a manned operator or from the drone itself. Due to the nature of the Quantum’s work, testing in hostile conditions should be tested, whether that is from weather or from enemy actions. 

There should be a code generation report, code coverage to test against industrial standards and code profiling to see if the system meets requirements for real time deployment. Since UAVs could be considered, the software developed for them might have to comply with guidelines like DO-178B.  


Q2. Reasons behind choice of tech stack?

A2. The reason for why this tech stack was chosen is because it is widely used for drone development. Moreover, you can use ArduPilot for commercial use without having to pay a fee, unlike some other source codes. Python was chosen as a language as it is what I have most experience in between that and C++. Ubuntu 18.04 was chosen as it is needed to use ROS Melodic, and Melodic was chosen as it is modern and well tested. While Noetic could have been used Melodic was considered more robust. Moreover, university computers that have Linux available to me only use 18.04.

Q3. What would you add with 1 week extra?

A3. Implementing collision avoidance and adding a motion planning algorithm would be at the top of what should be done. Moreover, using visual inertial odometry data should be considered when implementing movement without a GPS. This is so that optical flow can be done.
