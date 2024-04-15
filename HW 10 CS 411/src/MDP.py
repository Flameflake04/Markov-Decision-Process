# CS 411 - Assignment 10 - Markov decision process
# Name: Duc Tran, UIN: 679876782
# Spring 2024

import random
import math
import time

# This class will build up board as 2D array with user-input row and column
# This class also declare sqaure for user input as well as goal states and its reward
class State:
    def __init__(self, row, column, wallPosition, goalPosition):
        # Build the board and correctsponding wall
        self.row = row
        self.column = column
        self.board = [[0 for _ in range(row)] for _ in range(column)]
        self.goalValue = []
        for element in wallPosition:
            self.board[int(element[2]) - 1][int(element[0]) - 1] = "--------------"

        # Set the goal states and its reward
        for element in goalPosition:
            if element[4] == '-':
                self.board[int(element[2]) - 1][int(element[0]) - 1] = - int(element[5:])
                self.goalValue.append(- int(element[5:]))
            else:
                self.board[int(element[2]) - 1][int(element[0]) - 1] = int(element[5:])
                self.goalValue.append(int(element[5:]))

        # Reverse the row for correcting with output
        if len(self.board) % 2 == 1:
            for i in range(0, len(self.board)//2 + 1):
                temp = self.board[i]
                self.board[i] = self.board[len(self.board) - 1 - i]
                self.board[len(self.board) - 1 - i] = temp
        else:
            for i in range(0, len(self.board)//2):
                temp = self.board[i]
                self.board[i] = self.board[len(self.board) - 1 - i]
                self.board[len(self.board) - 1 - i] = temp


class Markov_Decision_Process:
    def __init__(self, state, reward, discountRate, epsilon, transitionProbabilty):
        self.state = state
        self.transitionProbabilityLeft = transitionProbabilty[1]
        self.transitionProbabilityRight = transitionProbabilty[2]
        self.transitionProbabilityUp = transitionProbabilty[0]
        self.transitionProbabiltyDown = transitionProbabilty[3]
        self.reward = reward
        self.epsilonValue = epsilon
        self.discountRate = discountRate

    # This function checked if the square is non-terminal state square or not
    # Return true if non-terminal, false if goal
    def punishment_bool(self, stateSquare):
        for elements in self.state.goalValue:
            if stateSquare == elements:
                return False
        return True

    # This function calculate the expected value of the square in positionX and positionY with action "move" consists of R, U, L, D
    def transition_model(self, move, positionX, positionY):
        state_row = len(self.state.board) # 3 in this case
        state_column = len(self.state.board[0]) # 4 in this case

        # Check for all sqaure surrounding the block with positionX and positionY
        square_up = self.state.board[max(positionX - 1, 0)][positionY]
        square_right = self.state.board[positionX][min(positionY + 1, state_column - 1)]
        square_down =  self.state.board[min(positionX + 1, state_row -1)][positionY]
        square_left = self.state.board[positionX][max(positionY - 1,0)]
        
        # Check for all wall case, bounce off back to original place if meet with the wall
        if square_up == "--------------":
            square_up = self.state.board[positionX][positionY] 
        if square_down == "--------------":
            square_down = self.state.board[positionX][positionY] 
        if square_left == "--------------":
            square_left = self.state.board[positionX][positionY] 
        if square_right == "--------------":
            square_right = self.state.board[positionX][positionY] 

        # This function calculate all posible actions that player can make, and return the expected value:
        # The value for one move formula will be:
        # Σ (sqaure adjacent), sum up ((discountRate for only non-terminal state * square adjacent + reward only for non-terminal state)) * transitionProbability
        if move == "R":
            value = ((max(self.discountRate, not self.punishment_bool(square_right)) * square_right + self.reward * self.punishment_bool(square_right)) * self.transitionProbabilityUp + 
                    (max(self.discountRate, not self.punishment_bool(square_up)) * square_up + self.reward * self.punishment_bool(square_up))  * self.transitionProbabilityLeft +
                    (max(self.discountRate, not self.punishment_bool(square_down)) * square_down + self.reward * self.punishment_bool(square_down)) * self.transitionProbabilityRight)
        elif move == "U":
            value = ((max(self.discountRate, not self.punishment_bool(square_up)) * square_up + self.reward * self.punishment_bool(square_up)) * self.transitionProbabilityUp +
                     (max(self.discountRate, not self.punishment_bool(square_left)) * square_left + self.reward * self.punishment_bool(square_left)) * self.transitionProbabilityLeft +
                     ( max(self.discountRate, not self.punishment_bool(square_right)) * square_right + self.reward * self.punishment_bool(square_right)) * self.transitionProbabilityRight)
        elif move == "L":
            value = ((max(self.discountRate, not self.punishment_bool(square_left)) * square_left + self.reward * self.punishment_bool(square_left)) * self.transitionProbabilityUp +
                     (max(self.discountRate, not self.punishment_bool(square_down)) * square_down + self.reward * self.punishment_bool(square_down)) * self.transitionProbabilityLeft +
                     (max(self.discountRate, not self.punishment_bool(square_up)) * square_up + self.reward * self.punishment_bool(square_up)) * self.transitionProbabilityRight)
        elif move == "D":
            value = ((max(self.discountRate, not self.punishment_bool(square_down)) * square_down + self.reward * self.punishment_bool(square_down)) * self.transitionProbabilityUp +
                     (max(self.discountRate, not self.punishment_bool(square_right)) * square_right + self.reward * self.punishment_bool(square_right)) * self.transitionProbabilityLeft +
                     (max(self.discountRate, not self.punishment_bool(square_left)) * square_left + self.reward * self.punishment_bool(square_left)) * self.transitionProbabilityRight)
        return value


    # This function advanced the board states though each time step (iteration), and print out the final ultility
    def value_iteration(self):
        termination_condition = self.epsilonValue * (1 - self.discountRate) / (self.discountRate)
        iteration_count = 0

        while True:
            list_value_iteration = []
            delta_difference = 0
            print("Iteration " + str(iteration_count))
            self.print_state()
            # Calculating each square state, one by one and store it in a list

            for i in range(0, len(self.state.board)):
                for j in range(0, len(self.state.board[0])):
                    if self.punishment_bool(self.state.board[i][j]) and self.state.board[i][j] != "--------------":
                        list_value_iteration.append(max(self.transition_model("R", i, j), self.transition_model("U", i, j)
                                                , self.transition_model("L", i, j) , self.transition_model("D", i, j)))
        
            # Reassign the value from the list prior to the board state
            counter = 0
            for i in range(0, len(self.state.board)):
                for j in range(0, len(self.state.board[0])):
                    if self.punishment_bool(self.state.board[i][j]) and self.state.board[i][j] != "--------------":
                        delta_difference = max(delta_difference, abs(self.state.board[i][j] - list_value_iteration[counter]))
                        self.state.board[i][j] = list_value_iteration[counter]
                        counter += 1
            
            # Checking the break condition
            if (delta_difference <= termination_condition):
                break
            iteration_count += 1
            print()
        print()
        print("Final Value After Convergence")
        self.print_state()
        print()
        
        self.final_policy()
        
        

    def final_policy(self):
        print("################ POLICY ITERATION ###########################")
        print()
        directions = ["U", "R", "L", "D"]
        max_direction = "U"
        list_policy = []
        maximum_value = float('-inf')
        for i in range(0, len(self.state.board)):
            for j in range(0, len(self.state.board[0])):
                if self.punishment_bool(self.state.board[i][j]) and self.state.board[i][j] != "--------------":
                    for direction in directions:
                        if self.transition_model(direction, i, j) > maximum_value:
                            maximum_value = self.transition_model(direction, i, j)
                            max_direction = direction
                    list_policy.append(max_direction)
                    maximum_value = float('-inf')
        counter = 0
        for i in range(0, len(self.state.board)):
            for j in range(0, len(self.state.board[0])):
                if self.punishment_bool(self.state.board[i][j]) and self.state.board[i][j] != "--------------":
                    self.state.board[i][j] = list_policy[counter]
                    counter += 1
        
        for list_elements in self.state.board:
            for elements in list_elements:
                if self.punishment_bool(elements):
                    print(str(elements), end = " ")
                # All terminal state has no future, set all to 0
                elif elements == "--------------":
                    print("-", end = " ")
                else:
                    print("T", end = " ")
            print()


    def print_state(self):
        for list_elements in self.state.board:
            for elements in list_elements:
                if self.punishment_bool(elements):
                    print(str(elements), end = " ")
                # All terminal state has no future, set all to 0
                else:
                    print("0", end = " ")
            print()


if __name__ == '__main__':
    x, y = map(int, input("Enter the size of the map, seperate with space: ").split())
    list_wall_position = [str(x) for x in input("Enter all wall position, sepearte with space and comma: ").split(", ")]
    goalPosition = [str(x) for x in input("Enter all goal position and its reward, sepearte with space and comma: ").split(", ")]
    reward = float(input("Enter the reward in non-terminal state: "))
    transitionProbabilty = [float(x) for x in input("Enter 4 transition probability (Up -> Left -> Right -> Down), sepearate with space: ").split(" ")]
    discountRate = float(input("Enter the discount rate: "))
    epsilon = float(input("Enter the epsilon value: "))
    print("################ VALUE ITERATION ###########################")
    print()
    newState = State(x, y, list_wall_position, goalPosition)
    agent = Markov_Decision_Process(newState, reward, discountRate, epsilon, transitionProbabilty)
    agent.value_iteration()