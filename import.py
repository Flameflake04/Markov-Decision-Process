# CS 411 - Assignment 10 - Markov decision process
# Name: Duc Tran, UIN: 679876782
# Spring 2024

import random
import math
import time

# This class will build up board as size (x,y) as user input:
class State:
    def __init__(self, row, column, wallPosition, goalPosition, reward, discountRate, epsilon, transitionProbabilty):
        self.row = row
        self.column = column
        
        self.board = [[0 for _ in range(row)] for _ in range(column)]
        for element in wallPosition:
            self.board[int(element[2]) - 1][int(element[0]) - 1] = "--------------"

        for element in goalPosition:
            if element[4] == '-':
                self.board[int(element[2]) - 1][int(element[0]) - 1] = - int(element[5])
            else:
                self.board[int(element[2]) - 1][int(element[0]) - 1] = int(element[5])

        self.reward = reward

        self.epsilonValue = epsilon
        self.discountRate = discountRate

        self.transitionProbabilityLeft = transistionProbabilty[1]
        self.transitionProbabilityRight = transistionProbabilty[2]
        self.transitionProbabiltyUp = transistionProbabilty[0]
        self.transistionProbabiltyDown = transistionProbabilty[3]

    def make_move(self):
        pass


    def print_state(self):
        for list_elements in self.board:
            for elements in list_elements:
                print(str(elements), end = " ")
            print()


class Markov_Decision_Process():
    def MDP(self, stateObject):
        pass
    def print_output(self):
        pass

if __name__ == '__main__':
    x, y = map(int, input("Enter the size of the map, seperate with space: ").split())
    list_wall_position = [str(x) for x in input("Enter all wall position, sepearte with space and comma: ").split(", ")]
    goalPosition = [str(x) for x in input("Enter all goal position and its reward, sepearte with space and comma: ").split(", ")]
    reward = input("Enter the reward in non-terminal state: ")
    transistionProbabilty = [float(x) for x in input("Enter 4 transistion probability (Up -> Left -> Right -> Down), sepearate with space: ").split(" ")]
    discountRate = float(input("Enter the discount rate: "))
    epsilon = float(input("Enter the epsilon value: "))
    newState = State(x, y, list_wall_position, goalPosition, reward, discountRate, epsilon, transistionProbabilty)

    newState.print_state()