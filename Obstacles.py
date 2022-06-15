import pygame
from random import randint as rnInt

class Obstacles(object):
    __facingUpwards = pygame.transform.scale(pygame.image.load("FlappyBirdAssets/PipeUp.png"), (80, 400))
    __facingDownwards = pygame.transform.scale(pygame.image.load("FlappyBirdAssets/PipeDown.png"), (80, 400))
    __passedPipes = 0
    __arrOfYPositions = [
        [-260, 270], [-210, 320], [-310, 220], [-190, 340],
        [-250, 280], [-360, 170], [-330, 200], [-170, 360],
        [-240, 290], [-150, 380], [-295, 235], [-150, 380],
        [-270, 260], [-290, 240], [-200, 330], [-340, 190]
    ]

    def __init__(self):
        arrOfIndices = self.get3RandomIndices()
        self.__pipeDown1 = self.__facingDownwards.get_rect(topleft=[1300, self.__arrOfYPositions[arrOfIndices[0]][0]])
        self.__pipeUp1 = self.__facingUpwards.get_rect(topleft=[1300, self.__arrOfYPositions[arrOfIndices[0]][1]])
        self.__pipeDown2 = self.__facingDownwards.get_rect(topleft=[1720, self.__arrOfYPositions[arrOfIndices[1]][0]])
        self.__pipeUp2 = self.__facingUpwards.get_rect(topleft=[1720, self.__arrOfYPositions[arrOfIndices[1]][1]])
        self.__pipeDown3 = self.__facingDownwards.get_rect(topleft=[2140, self.__arrOfYPositions[arrOfIndices[2]][0]])
        self.__pipeUp3 = self.__facingUpwards.get_rect(topleft=[2140, self.__arrOfYPositions[arrOfIndices[2]][1]])
        self.__pipes = [[self.__pipeUp1, self.__pipeDown1],
                        [self.__pipeUp2, self.__pipeDown2],
                        [self.__pipeUp3, self.__pipeDown3]]

    def get3RandomIndices(self):
        first = rnInt(0, len(self.__arrOfYPositions) - 1)
        second = rnInt(0, len(self.__arrOfYPositions) - 1)
        third = rnInt(0, len(self.__arrOfYPositions) - 1)

        return [first, second, third]

    def displayPipes(self, surface):
        for index, pipe in enumerate(self.__pipes):
            for newIndex, individualPipe in enumerate(pipe):
                if newIndex % 2 == 0:
                    surface.blit(self.__facingUpwards.convert_alpha(), (individualPipe.x, individualPipe.y))
                elif newIndex % 2 == 1:
                    surface.blit(self.__facingDownwards.convert_alpha(), (individualPipe.x, individualPipe.y))

    def movePipes(self):
        for pipe in self.__pipes:
            for individualPipes in pipe:
                individualPipes.x -= 3
        self.checkIfPassedTheBorder()

    def checkIfPassedTheBorder(self):
        if self.__pipeUp1.x < -70:
            arrOfIndices = self.get3RandomIndices()
            self.__pipeUp1.x, self.__pipeDown1.x = 1300, 1300
            self.__pipeUp1.y, self.__pipeDown1.y = self.__arrOfYPositions[arrOfIndices[0]][1], self.__arrOfYPositions[
                arrOfIndices[0]][0]

        if self.__pipeUp2.x < -70:
            arrOfIndices = self.get3RandomIndices()
            self.__pipeUp2.x, self.__pipeDown2.x = 1300, 1300
            self.__pipeUp2.y, self.__pipeDown2.y = self.__arrOfYPositions[arrOfIndices[1]][1], self.__arrOfYPositions[
                arrOfIndices[1]][0]
        if self.__pipeUp3.x < -70:
            arrOfIndices = self.get3RandomIndices()
            self.__pipeUp3.x, self.__pipeDown3.x = 1300, 1300
            self.__pipeUp3.y, self.__pipeDown3.y = self.__arrOfYPositions[arrOfIndices[2]][1], self.__arrOfYPositions[
                arrOfIndices[2]][0]

    def checkForScore(self, flappy):
        for pipes in self.__pipes:
            if pipes[0].x + 30 == flappy.x:
                self.__passedPipes += 1

    def getPipes(self):
        return self.__pipes

    def getPassedPipesValue(self):
        return self.__passedPipes
