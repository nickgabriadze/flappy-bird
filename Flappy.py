import pygame


class Flappy(object):
    __flappyItself = pygame.transform.scale(pygame.image.load("FlappyBirdAssets/Flappy.png"), (55, 55))
    __flappyDefault = __flappyItself
    __flappyUp = pygame.transform.scale(pygame.image.load("FlappyBirdAssets/FlappyUp.png"), (55, 55))
    __flappyDown = pygame.transform.scale(pygame.image.load("FlappyBirdAssets/FlappyDown.png"), (55, 55))
    __direction = "UP"
    __enableMovement = True

    def __init__(self, x, y):
        self.flappy = pygame.Rect(x // 2 - 50, y // 2 - 50, 40, 20)

    def displayFlappy(self, surface):
        surface.blit(self.__flappyItself.convert_alpha(), (self.flappy.x, self.flappy.y))

    def flappyMovement(self, pressedKey, mousePressed):

        if self.__enableMovement:
            if pressedKey[pygame.K_SPACE] or mousePressed[0]:
                self.__direction = "UP"

                self.__flappyItself = self.__flappyUp
            else:
                self.__direction = "DOWN"
                self.__flappyItself = self.__flappyDefault

            if self.__direction == "UP":

                self.flappy.y -= 10
            elif self.__direction == "DOWN":
                self.flappy.y += 5

        if self.checkForBorders():
            return True

    def checkForBorders(self):
        if self.flappy.y < -8:
            pygame.mixer.music.load("FlappyBirdAssets/ObstacleHit.ogg")
            pygame.mixer.music.play()
            self.flappy.y = -8
            self.__enableMovement = False

            return True
        elif self.flappy.y > 505:
            pygame.mixer.music.load("FlappyBirdAssets/ObstacleHit.ogg")
            pygame.mixer.music.play()
            self.__flappyItself = self.__flappyDown
            self.__enableMovement = False
            self.flappy.y = 505

            return True

    def checkForPipeCollision(self, pipes):
        for pipes in pipes:
            for individualPipe in pipes:
                if self.flappy.colliderect(individualPipe):
                    pygame.mixer.music.load("FlappyBirdAssets/ObstacleHit.ogg")
                    pygame.mixer.music.play()

                    self.__enableMovement = False
                    self.__flappyItself = self.__flappyDown
                    self.flappy.y = 510
                    return True

    def getFlappy(self):
        return self.flappy
