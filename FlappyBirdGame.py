from Obstacles import Obstacles
from Flappy import Flappy
import pygame
pygame.init()
pygame.mixer.init()


class FlappyBirdGame:
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
                    newGame = FlappyBirdGame()
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
    app = FlappyBirdGame()
    app.run()
