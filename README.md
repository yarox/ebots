# Ebots

## Introduction
To follow a wall, or in a more general sense, to follow the contours of an object, is an important behavior for autonomous mobile robots. Robots operating in an unknown, unstructured environment use their sensors to perceive the surroundings and plan their motions or trajectories accordingly. 

The objective of this experiment is to build a robot capable of following walls, but instead of creating fixed rules telling the robot what to do, we will use a more flexible evolutionary approach.

# Dependencies
  + Python 2.7
  + NumPy 1.6.2
  + matplotlib 1.2.x
  + MongoDB 2.2.0
  + PyMongo 2.3
  + Blender 2.63.a
  + MORSE 0.5.2

# How to Run
Open two separate terminal sessions and go to the `ebots/` directory. In one terminal execute `morse run stages/stage_name.py`, and in the other `python experiment-X.py`. A Blender window containing the simulation should appear.

## Approach
Control systems for autonomous robots are often programmed directly by researchers or designers. Such control programs can be very complex. Researchers must anticipate which abilities a given robot will need, and then formulate these into a control program or control hierarchy. 

As the complexity of an environment and task for a given autonomous robot increases, the difficulty of designing an adequate control system by hand becomes a limiting factor in the degree of functional complexity that can be achieved. A potential solution to this problem is to develop methods that allow robots to learn how to perform complex tasks automatically.

*Evolutionary computation* is a subfield of artificial intelligence that involves combinatorial optimization problems. This approach uses iterative progress, such as growth or development in a population. This population is then selected in a guided random search to achieve the desired end. 

In our case, we use an *artificial neural networks* as a control system and an evolutionary algorithm as a training method. This combination is commonly known as *neuroevolution*.

We chose the *differential evolution* (DE) method as the evolutionary algorithm to train our neural networks. This method optimizes a problem by maintaining a population of candidate solutions and creating new candidate solutions by combining existing ones according to a simple formulae, and then keeping whichever candidate solution has the best fitness on the optimization problem at hand. Basically, DE adds the weighted difference between two population vectors to a third vector. This way no separate probability distribution has to be used which makes the scheme completely self-organizing.

Successful evolution of intelligent autonomous robot controllers is ultimately dependent on the formulation of suitable *fitness functions* that are capable of selecting for successful behaviors without specifying the low-level implementation details of those behaviors.

We can distinguish between various kinds of fitness functions based on the degree of a priori knowledge introduced by designer (in descending order):

  + **Training data**: fitness is maximized when the system in question produces a minimum output error when presented with a given set of inputs with a known set of optimal associated outputs.

  + **Behavioral**: task-specific hand-formulated functions that measure various aspects of what a robot is doing and how it is doing it. These types of functions generally include several sub-functions or terms that are combined into a weighted sum or product. These sub-functions or terms are intended to measure simple action-response behaviors, low-level sensor-actuator mappings, or other events/features local to the robot.

  + **Functional incremental**: the evolutionary process begins by selecting for a simple ability upon which a more complex overall behavior can be built. Once the simple ability is evolved, the fitness function is altered or augmented to select for a more complex behavior. This sequence of evolution followed by fitness function augmentation continues until eventually the desired final behavior is achieved. The overall process can be considered one of explicit training for simple sub-behaviors followed by training for successively more complex behaviors.

  + **Tailored**: contain aggregate terms that measure some degree or aspect of task completion that is divorced from any particular behavior or method. Hence, tailored fitness functions combine elements from behavioral fitness functions and aggregate fitness functions.

  + **Environmental incremental**: rather than simply increasing the complexity of the fitness selection function, one form of incremental evolution involves augmenting the difficulty of the environment in which the robots must operate.

  + **Competitive and co-competitive**: utilize direct competition between members of an evolving population. in competitive evolution robot controllers compete against one another within the same environment so that the behavior of one robot directly influences the behavior, and therefore fitness evaluation, of another. In co-competitive evolution two separate populations (performing distinct tasks) compete against each other within the same environment.

  + **Aggregate**: select only for high-level success or failure to complete a task without regard to how the task was completed. This type of selection reduces injection of human bias into the evolving system by aggregating the evaluation of benefit (or deficit) of all of the robot's behaviors into a single success/failure term.

## Implementation
The robot has two laser sensors and a motion actuator. The laser sensors returns the distance to the closest object, and the motion actuator recieves the values of linear and angular speed and applies them to the robot as direct translation.

![robot](https://www.dropbox.com/s/82zesxox29fahdg/robot.png?dl=0)

A *feed forward neural network* (FFANN) with two inputs and two outputs is used to control our robot. For the activation function, we used a *logistic function* bounded between `-5` and `5`. We feed the FFANN with the values from the two laser sensors, and send the output to the motion actuator. This causes the robot to move around the environment.

![controller](https://www.dropbox.com/s/8sanm4pz3s91xfs/controller.png?dl=0)

The weights of the FFANNs are evolved using the differential evolution algorithm with the following parameters: weighting factor `F = 0.8`, crossover constant `CR = 0.9`, and number of parents `NP = 20`.

We let the system evolve for `20` generations. In each generation, the fitness of a robot is calculated as the average fitness obtained after two executions, each execution lasting `100` clock cycles.

An aggregate fitness function was designed with an energetic model in mind: a robot could gain or lose energy depending on her actions when moving around the environment. Thus, the fitness is determined only by the energy level at the end of the evaluation period. 

To implement this model, several objects ("cookies") were placed near the walls. The more "cookies" a robot gets during its execution time, the higher its energy. We assume that a robot that has managed to get a large number of "cookies" (and therefore energy) has developed a controller that allows her to follow the walls efficiently. 

The whole process can be summarized as follows:

1. Create a robot.
2. Create a population of networks. For each generation:
 
    1. Perturbate the current population creating a candidate population. For each candidate network:

        1. Set the network as the robot controller.
        2. Put the robot in the middle of the room and start the evaluation. 
        3. The network fitness is the final robot energy.

    3. Once we have evaluated the whole candidate population, the selection process starts, yielding a new current population.

3. Return the network with the highest fitness. 

## Results
At the end of the 20 generations the DE algorithm had converged significantly. The following figure shows how the fitness of the population improved, reaching maximum levels. Although there is some room for improvement, we will accept this suboptimal result due to long simulation times.

![figure1](https://www.dropbox.com/s/eae54shv1rzwp40/fitness_evo.png?dl=0)

[Next video](http://youtu.be/ffNPedVsot4) shows the best robot in action. As evidence shows, we can conclude that her has managed to develop the task satisfactorily, even though maximum fitness level was not reached. 

[In this other video](http://youtu.be/unuObGm6SQ0), we can see an evolution overview, showing the behavior of the best robot of each generation. At first, robots move randomly, but after a short period of time, they learn to stay at a distance of the walls. Finally, they manage to get most of the "cookies" during their evaluation time. The fact that they seems to prefer turning to the right is due to chance.  

## Conclusion
Automatic robot controller development methods that do not require hand coding or in-depth human knowledge are potentially of great value because it may be possible to apply them to domains in which humans have insufficient knowledge to develop adequate controllers directly.

Under a short number of iterations and with a small population, a near optimum behavior was achieved. We introduced very little knowledge about the problem into the robots; they exploited the environment and their bodies, improving their fitness generation after generation.

We have shown that this approach is simple, yet flexible and powerful. It can be applied to more complex domains, taking into account that the difficult part is coming up with a good fitness function. 

## References
1. Artificial neural network. (2012, October 13). In Wikipedia, The Free Encyclopedia. Retrieved 07:46, October 18, 2012, from <http://en.wikipedia.org/w/index.php?title=Artificial_neural_network&oldid=517534177>
2. Feedforward neural network. (2012, September 21). In Wikipedia, The Free Encyclopedia. Retrieved 07:32, October 18, 2012, from <http://en.wikipedia.org/w/index.php?title=Feedforward_neural_network&oldid=513807431>
3. Evolutionary computation. (2012, October 1). In Wikipedia, The Free Encyclopedia. Retrieved 07:34, October 18, 2012, from <http://en.wikipedia.org/w/index.php?title=Evolutionary_computation&oldid=515418753>
4. Storn, R., & Price, K. (1997). Differential Evolution – A Simple and Efficient Heuristic for Global Optimization over Continuous Spaces. Journal of Global Optimization, 11(4), 341-359. Springer. Retrieved from <http://www.springerlink.com/index/X555692233083677.pdf>
5. Nelson, A. L., Barlow, G. J., & Doitsidis, L. (2009). Fitness functions in evolutionary robotics: A survey and analysis. Robotics and Autonomous Systems, 57(4), 345-370. Elsevier B.V. Retrieved from <http://www.nelsonrobotics.org/paper_archive_nelson/nelson-jras-2009.pdf>
6.  Braitenberg, V. (1986). Vehicles: Experiments in Synthetic Psychology. MIT.
7. Binti, R. (2005). Wall Following Mobile Robot. Kolej Universiti Teknikal Kebangsaan Malaysia. Retrieved from <http://library.utem.edu.my/index2.php?option=com_docman&task=doc_view&gid=3878&Itemid=208>
