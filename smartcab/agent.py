import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.epsilon = 0.05
        self.discount = 0.1
        self.alpha = 0.1
        self.q_values = {}

    def getQValue(self, state, action):
        if (state, action) not in self.q_values:
            return 0.0
        return self.q_values[(state, action)]

    def computeValueFromQValues(self, state):
        return max([(action, self.getQValue(state, action))
            for action in self.env.valid_actions], key=lambda x:x[1])[1]

    def computeActionFromQValues(self, state):
        legalActions = self.env.valid_actions
        q_values = [self.getQValue(state, action) for action in legalActions]
        maxQ = max(q_values)
        bestIndices = [index for index in range(len(q_values)) if q_values[index] == maxQ]
        chosenIndex = random.choice(bestIndices)
        return legalActions[chosenIndex]

    def getAction(self, state):
        if random.random() < self.epsilon:
            action = random.choice(self.env.valid_actions)
        else:
            action = self.computeActionFromQValues(state)
        return action

    def getValue(self, state):
        return self.computeValueFromQValues(state)
        
    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state
        self.state = (self.next_waypoint, inputs['light'], inputs['left'], inputs['oncoming'])
        
        # TODO: Select action according to your policy
        action = self.getAction(self.state)

        # Execute action and get reward
        reward = self.env.act(self, action)

        # TODO: Learn policy based on state, action, reward
        next_inputs = self.env.sense(self)
        next_next_waypoint = self.planner.next_waypoint()
        next_state = (next_next_waypoint, next_inputs['light'], next_inputs['right'], next_inputs['left'], next_inputs['oncoming'])

        oldValue = self.getQValue(self.state, action)
        sample = reward + self.discount*self.computeValueFromQValues(next_state)
        self.q_values[(self.state, action)] = (1-self.alpha)*oldValue + self.alpha*sample

        # print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.5, display=True)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=50)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line


if __name__ == '__main__':
    run()
