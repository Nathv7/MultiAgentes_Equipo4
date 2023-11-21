from mesa import Agent
import random

class Car(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of eight directions
    """
    def __init__(self, unique_id, model):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.visited_cells = []
        self.position_stack = []
        self.steps_taken = 0
        self.direction = None

    def move(self):
        """
        Determines if the agent can move in the direction that was chosen
        """
        # Check all contents in the current cell to find a Road agent.
        current_cell_contents = self.model.grid.get_cell_list_contents(self.pos)
        road_direction = None
        for content in current_cell_contents:
            if isinstance(content, Road):
                self.direction = content.direction
                print(content.direction)
                break

        # Get possible steps (Moore neighborhood without center cell)
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )

        # Filter out steps that lead to a cell with an Obstacle
        self.neighbor_queue = [
            pos for pos in possible_steps 
            if not any(isinstance(agent, Obstacle) for agent in self.model.grid.get_cell_list_contents(pos))
        ]


        # Filter the neighbor_queue based on the current direction
        if self.direction == "Right":
            self.neighbor_queue = [pos for pos in self.neighbor_queue if pos[0] > self.pos[0]]
        elif self.direction == "Left":
            self.neighbor_queue = [pos for pos in self.neighbor_queue if pos[0] < self.pos[0]]
        elif self.direction == "Up":
            self.neighbor_queue = [pos for pos in self.neighbor_queue if pos[1] > self.pos[1]]
        elif self.direction == "Down":
            self.neighbor_queue = [pos for pos in self.neighbor_queue if pos[1] < self.pos[1]]

        # Choose the next move
        next_move = None
        if self.neighbor_queue:
            next_move = self.random.choice(self.neighbor_queue)
        else:
            # If no valid move found, backtrack if possible
            if self.position_stack:
                previous_position = self.position_stack.pop()
                if previous_position in possible_steps:
                    next_move = previous_position

        # Execute the move if possible
        if next_move:
            self.model.grid.move_agent(self, next_move)
            self.visited_cells.append(next_move)
            self.steps_taken += 1
            if next_move not in self.position_stack:
                self.position_stack.append(self.pos)



    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        self.move()

class Traffic_Light(Agent):
    """
    Traffic light. Where the traffic lights are in the grid.
    """
    def __init__(self, unique_id, model, state = False, timeToChange = 10):
        super().__init__(unique_id, model)
        """
        Creates a new Traffic light.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            state: Whether the traffic light is green or red
            timeToChange: After how many step should the traffic light change color 
        """
        self.state = state
        self.timeToChange = timeToChange

    def step(self):
        """ 
        To change the state (green or red) of the traffic light in case you consider the time to change of each traffic light.
        """
        if self.model.schedule.steps % self.timeToChange == 0:
            self.state = not self.state

class Destination(Agent):
    """
    Destination agent. Where each car should go.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class Obstacle(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class Road(Agent):
    """
    Road agent. Determines where the cars can move, and in which direction.
    """
    def __init__(self, unique_id, model, direction= "Left"):
        """
        Creates a new road.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            direction: Direction where the cars can move
        """
        super().__init__(unique_id, model)
        self.direction = direction

    def step(self):
        pass
