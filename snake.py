#!/bin/python3
# Example file showing a circle moving on screen

from tkinter import W
import pygame
import time
import random

COLOR = "green"
DIRECTION = "DOWN"


CLOCK = pygame.time.Clock()
SPEED = 10
PIECE_WIDTH = 10
GAME_OVER = False
score = 0

S_HEIGHT = 1280
S_WIDTH = 720


def setBackground():
    screen.fill("red")
    pos = (10, 10)
    dim = (S_HEIGHT-20, S_WIDTH-20)
    shape_vec = pygame.math.Vector2(pos)
    overlaid_shape = pygame.Rect(shape_vec, dim)
    pygame.draw.rect(screen, "black", overlaid_shape)



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
        self.id = 0


class LinkedList:
    def __init__(self, startingPos: tuple):
        self.head = None
        self.tail = None
        for section in range(5):
            self.addNode(
                (startingPos[0], (startingPos[1] - section*PIECE_WIDTH)))

    def addNode(self, startingPos: tuple, stored_dir = None):
        if self.head is None:
            self.head = Node(startingPos)
            self.tail = self.head
            self.head.id = 0
            return None

        else:
            newNode = Node(startingPos)
            if stored_dir == None:
                stored_dir = []
            self.dir_queue = stored_dir + [DIRECTION]
            self.tail.next = newNode
            newNode.prev = self.tail
            newNode.next = None
            newNode.id = newNode.prev.id + 1
            self.tail = newNode
            return newNode

class Fruit:
    def __init__(self):
        self.fruit_exists = False
        self.pos = (0,0)
        self.fruit_rec = None
        self.color = "yellow"

    def drawFruit(self):
        if self.fruit_exists:
            pygame.draw.rect(screen, self.color, self.fruit_rec)

    def createFruit(self):
        if self.fruit_exists is False:
            self.pos = (random.randrange(40, S_HEIGHT-40), random.randrange(40, S_WIDTH-40))
            dim = (20, 20)
            shape_vec = pygame.math.Vector2(self.pos)
            self.fruit_rec = pygame.Rect(shape_vec, dim)
            self.fruit_exists = True

    def checkPos(self,snake_rec, stored_dir = None):
        global score
        if pygame.Rect.colliderect(snake_rec, self.fruit_rec):
            score += 10
            tail = snake.snake_LL.tail
            X, Y = snake.snake_LL.tail.pos
            
            if tail.dir_queue[0] == "LEFT":
                X += PIECE_WIDTH 
            elif tail.dir_queue[0] == "RIGHT":
                X -= PIECE_WIDTH
            elif tail.dir_queue[0] == "UP":
                Y += PIECE_WIDTH 
            elif tail.dir_queue[0] == "DOWN":
                Y -= PIECE_WIDTH
            t = snake.snake_LL.addNode((X, Y))
            
            self.fruit_exists = False
            self.createFruit()

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
        hR = None
        stored_dir = self.snake_LL.tail.dir_queue
        while curr is not None:
            snake_vec = pygame.math.Vector2(curr.pos)
            snake_rect = pygame.Rect(snake_vec, (PIECE_WIDTH, PIECE_WIDTH))
            if hR == None: 
                hR = snake_rect
            if curr is not None: 
                self.go_obj.checkOverlap(hR, snake_rect)
                self.go_obj.checkGameOver(posList, curr.pos, self.snake_LL)
                posList.append(curr.pos)
                fruit.checkPos(snake_rect, stored_dir)
            snake.handlePieceDir(curr)
            snake_vec = pygame.math.Vector2(curr.pos)
            snake_rect = pygame.Rect(snake_vec, (PIECE_WIDTH, PIECE_WIDTH))
            pygame.draw.rect(screen, curr.color, snake_rect)
            curr = curr.next



class GameOver:
    def checkOverlap(self, hR, cR):
        if hR is not cR and pygame.Rect.colliderect(hR, cR):
            print("Game over because snake body overlap")
            self.load_game_over()

    def checkGameOver(self, posList, curr, LL):
        pos = LL.head.pos

        if pos[0] > S_HEIGHT - 10 or pos[0] < 0:
            print("game over because bounds")
            self.load_game_over()
        if pos[1] > S_WIDTH - 10 or pos[1] < 0:
            print("game over because bounds")
            self.load_game_over()

    def load_game_over(self):
        global GAME_OVER
        GAME_OVER = True
        setBackground()
        GOfont = pygame.font.SysFont("Consolas", 50)
        title_card = GOfont.render("GAME OVER...", True, "RED")
        score_card = GOfont.render(f"SCORE: {score}", True, "GREEN")

        score_rect = score_card.get_rect()
        score_rect.midtop = (((S_HEIGHT/2)), (S_WIDTH/2)-120)

        title_rect = title_card.get_rect()
        title_rect.midtop = (S_HEIGHT/2, S_WIDTH/4)

        screen.blit(title_card, title_rect)
        screen.blit(score_card, score_rect)

        pygame.display.flip()
        time.sleep(4)
        quit()


if __name__ == "__main__":
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode([S_HEIGHT, S_WIDTH])
    pygame.display.set_caption("snake_in_snake")

    # get the center of the screen
    player_pos = (screen.get_width() / 2, screen.get_height() / 2)

    snake = Snake(LinkedList(player_pos))
    fruit = Fruit()
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

        # create a fruit if there isn't one on the board, and draw it on the screen
        fruit.createFruit()
        fruit.drawFruit()

        # update the snake body positions, and draw them on the screen
        snake.updateSectionPositions()
        CLOCK.tick(120)

        # flip() the display to put your work on screen
        pygame.display.flip()
        pygame.display.update()

pygame.quit()
