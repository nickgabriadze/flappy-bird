import pygame
from random import randint as rnInt

pygame.init()
pygame.mixer.init()


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


class App:
    __WIDTH = 1200
    __HEIGHT = 700
    __gameStarted = True
    __gameBG = pygame.image.load("FlappyBirdAssets/FlappyCityView.png")
    __ground = pygame.image.load("FlappyBirdAssets/FlappyGroundBG.png")
    __spaceButtonIcon = pygame.transform.scale(pygame.image.load("FlappyBirdAssets/PressSpace.png"), (600, 100))
    __restartICON = pygame.image.load("FlappyBirdAssets/RestartIcon.png")
    __endICON = pygame.image.load("FlappyBirdAssets/EndIcon.png")

    __gameOver = False
    __gameScore = 0
    __inGame = False
    __welcome = True
    __movableGround = False

    def __init__(self):
        self.running = False
        self.clock = None
        self.screen = None
        self.flappy = None
        self.obstacles = None
        self.__flappyGround = self.__ground.get_rect(topleft=[0, 560])

    def run(self):
        self.init()

        while self.running:
            self.clock.tick(60)
            self.update()
            self.render()
            self.pressSpace()
            self.checkForRestartOrQuit()
            pygame.display.flip()
        self.cleanUp()

    def init(self):
        self.screen = pygame.display.set_mode((self.__WIDTH, self.__HEIGHT))
        pygame.display.set_caption("Flappy Bird")
        windowIcon = pygame.image.load("FlappyBirdAssets/WindowIcon.png").convert()
        pygame.display.set_icon(windowIcon)
        self.clock = pygame.time.Clock()
        self.running = True
        self.flappy = Flappy(self.__WIDTH, self.__HEIGHT)
        self.obstacles = Obstacles()

    def update(self):
        self.events()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def render(self):
        if self.__gameStarted:
            pressedKeys = pygame.key.get_pressed()
            mousePress = pygame.mouse.get_pressed()

            if self.__inGame:
                if self.flappy.flappyMovement(pressedKeys, mousePress) or \
                        self.flappy.checkForPipeCollision(self.obstacles.getPipes()):
                    self.__gameOver = True
                    self.__gameStarted = False
                    self.__inGame = False

            self.cleanUp()
            self.screen.blit(self.__gameBG.convert(), (0, 0))
            self.obstacles.displayPipes(self.screen)
            self.obstacles.checkForScore(self.flappy.getFlappy())
            self.__gameScore = self.obstacles.getPassedPipesValue()
            if self.__inGame:
                self.obstacles.movePipes()
                self.displayScore()

            self.flappy.displayFlappy(self.screen)

            if self.__movableGround:
                self.movingGround()
            else:
                self.screen.blit(self.__ground.convert_alpha(), (0, 560))

            self.gameOver()

    def displayScore(self):
        width = 40
        if 10 <= self.__gameScore < 100:
            width += 17
        if 100 <= self.__gameScore < 1000:
            width += 30
        if 1000 <= self.__gameScore < 10000:
            width += 50
        if self.__inGame:
            scoreFont = pygame.font.Font("FlappyBirdAssets/BungeeShade-Regular.ttf", 60)
            score = scoreFont.render(f"{self.__gameScore}", False, (255, 255, 255))
            self.screen.blit(score, (self.__WIDTH // 2 - width, 100))

    def gameOver(self):
        width = 112
        if 10 <= self.__gameScore < 100:
            width += 17
        if 100 <= self.__gameScore < 1000:
            width += 35
        if 1000 <= self.__gameScore < 10000:
            width += 50
        if self.__gameOver:
            pygame.display.set_caption("Game Over")
            gameOverFont = pygame.font.Font("FlappyBirdAssets/BungeeShade-Regular.ttf", 45)
            gameOverText = gameOverFont.render(f"Score:{self.__gameScore}", False, (4, 5, 115))
            self.screen.blit(gameOverText, (self.__WIDTH // 2 - width, self.__HEIGHT // 2 - 45))
            self.screen.blit(self.__restartICON.convert_alpha(), (self.__WIDTH // 2 - 120, self.__HEIGHT // 2 + 5))
            self.screen.blit(self.__endICON.convert_alpha(), (self.__WIDTH // 2 + 5, self.__HEIGHT // 2 + 5))

    def checkForRestartOrQuit(self):
        if self.__gameOver:
            mouseClick = pygame.mouse.get_pressed()
            if mouseClick[0]:
                mousePosX, mousePosY = pygame.mouse.get_pos()

                if 487 < mousePosX < 595 and 357 < mousePosY < 401:
                    newGame = App()
                    newGame.run()
                if 611 < mousePosX < 723 and 359 < mousePosY < 400:
                    self.running = False

    def pressSpace(self):
        if self.__welcome:
            pressedKeys = pygame.key.get_pressed()
            flappyBirdFont = pygame.font.Font("FlappyBirdAssets/Aldrich-Regular.ttf", 100)
            flappyBirdText = flappyBirdFont.render("FlappyBird", False, (255, 255, 255))
            self.screen.blit(self.__spaceButtonIcon.convert_alpha(), (self.__WIDTH // 2 - 300, self.__HEIGHT // 2 + 20))
            self.screen.blit(flappyBirdText, (335, 100))
            if pressedKeys[pygame.K_SPACE]:
                self.__gameStarted = True
                self.__inGame = True
                self.__welcome = False
                self.__movableGround = True

    def movingGround(self):
        self.screen.blit(self.__ground.convert_alpha(), (self.__flappyGround.x, self.__flappyGround.y))
        if self.__flappyGround.x < - 300:
            self.__flappyGround.x = -51
        else:
            self.__flappyGround.x -= 3

    def cleanUp(self):
        self.screen.fill(0)


if __name__ == "__main__":
    app = App()
    app.run()
