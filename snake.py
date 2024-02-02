#!/bin/python3
# Example file showing a circle moving on screen

import pygame
import time


COLOR = "green"
DIRECTION = "DOWN"

CLOCK = pygame.time.Clock()
SPEED = 10
PIECE_WIDTH = 10
GAME_OVER = False

S_HEIGHT = 1280
S_WIDTH = 720


def setBackground():
    screen.fill("black")


def keyHandler(keys, snake_instance):
    global DIRECTION
    if keys[pygame.K_UP]:
        if DIRECTION != "DOWN":
            DIRECTION = "UP"

    if keys[pygame.K_DOWN]:
        if DIRECTION != "UP":
            DIRECTION = "DOWN"

    if keys[pygame.K_RIGHT]:
        if DIRECTION != "LEFT":
            DIRECTION = "RIGHT"

    if keys[pygame.K_LEFT]:
        if DIRECTION != "RIGHT":
            DIRECTION = "LEFT"

    if keys[pygame.K_q]:
        quit()


class Node:
    def __init__(self, startingPos: tuple):
        self.next = None
        self.prev = None
        self.dir_queue = [DIRECTION]
        self.pos = startingPos
        self.color = COLOR


class LinkedList:
    def __init__(self, startingPos: tuple):
        self.head = None
        self.tail = None
        for section in range(5):
            self.addNode(
                (startingPos[0], (startingPos[1] - section*PIECE_WIDTH)))

    def addNode(self, startingPos: tuple):
        if self.head is None:
            self.head = Node(startingPos)
            self.tail = self.head

        else:
            newNode = Node(startingPos)
            self.tail.next = newNode
            newNode.prev = self.tail
            self.tail = self.tail.next


class Snake:
    def __init__(self, snake_pieces: LinkedList):
        self.snake_LL = snake_pieces
        self.spd = SPEED
        self.go_obj = GameOver()

    def handlePieceDir(self, piece):
        if piece is self.snake_LL.head:
            self.snake_LL.head.dir_queue = [DIRECTION]

        # remove the most recent action from the queue
        dir = piece.dir_queue.pop(0)

        # append the new work to the next node
        if piece.next is not None:
            piece.next.dir_queue += [dir]

        if dir == "LEFT":
            piece.pos = (piece.pos[0] - self.spd, piece.pos[1])
            piece.color = "yellow"

        elif dir == "RIGHT":
            piece.pos = (piece.pos[0] + self.spd, piece.pos[1])
            piece.color = "green"

        elif dir == "UP":
            piece.pos = (piece.pos[0], piece.pos[1] - self.spd)
            piece.color = "red"
        elif dir == "DOWN":
            piece.pos = (piece.pos[0], piece.pos[1] + self.spd)
            piece.color = "white"

    def updateSectionPositions(self):
        curr = self.snake_LL.head
        posList = []

        while curr is not None:
            snake.handlePieceDir(curr)
            snake_vec = pygame.math.Vector2(curr.pos)
            snake_rect = pygame.Rect(snake_vec, (PIECE_WIDTH, PIECE_WIDTH))
            pygame.draw.rect(screen, curr.color, snake_rect)
            curr = curr.next

            if curr is not None:
                self.go_obj.checkGameOver(posList, curr.pos, self.snake_LL)
                posList.append(curr.pos)


class GameOver:
    def checkGameOver(self, posList, curr, LL):
        if curr in posList:
            print("THIS ONE")
            self.load_game_over()

        pos = LL.head.pos

        if pos[0] > S_WIDTH - 10 or pos[0] < 0:
            self.load_game_over()
        if pos[1] > S_HEIGHT - 10 or pos[1] < 0:
            self.load_game_over()

    def load_game_over(self):
        global GAME_OVER
        GAME_OVER = True
        setBackground()
        GOfont = pygame.font.SysFont("Consolas", 50)
        title_card = GOfont.render("GAME OVER...", True, "RED")

        title_rect = title_card.get_rect()
        title_rect.midtop = (S_HEIGHT/2, S_WIDTH/4)

        screen.blit(title_card, title_rect)
        pygame.display.flip()
        time.sleep(4)
        quit()


if __name__ == "__main__":
    # pygame setup
    pygame.init()

    screen = pygame.display.set_mode((S_HEIGHT, S_WIDTH))
    pygame.display.set_caption("snake_in_snake")

    # get the center of the screen
    player_pos = (screen.get_width() / 2, screen.get_height() / 2)

    snake = Snake(LinkedList(player_pos))

    while True:

        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                keyHandler(pygame.key.get_pressed(), snake)

        # fill the screen with a color to wipe away anything from last frame
        setBackground()

        # update the snake body positions, and draw them on the screen
        snake.updateSectionPositions()
        CLOCK.tick(30)

        # flip() the display to put your work on screen
        pygame.display.flip()
        pygame.display.update()

pygame.quit()
