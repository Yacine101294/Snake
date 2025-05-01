import pygame
import random
from settings import *

def lancer_jeu(fenetre):
    #Variable du jeu
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    direction = "RIGHT"
    changer_direction = direction

    #Boucle principale du jeu
    jeu_actif = True
    while jeu_actif:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
                # Gestion des touches directionnelles
                if event.key == pygame.K_UP and direction != "DOWN":
                    changer_direction = "UP"
                if event.key == pygame.K_DOWN and direction != "UP":
                    changer_direction = "DOWN"
                if event.key == pygame.K_RIGHT and direction != "LEFT":
                    changer_direction = "RIGHT"
                if event.key == pygame.K_LEFT and direction != "RIGHT":
                    changer_direction = "LEFT"

        # Mise à jour de la direction
        direction = changer_direction

        # Déplacement du serpent
        if direction == "UP":
            snake_pos[1] -= 10
        if direction == "DOWN":
            snake_pos[1] += 10
        if direction == "LEFT":
            snake_pos[0] -= 10
        if direction == "RIGHT":
            snake_pos[0] += 10

        # Mise à jour du corps du serpent
        snake_body.insert(0, list(snake_pos))
        snake_body.pop()

        # Affichage
        fenetre.fill(NOIR)
        for pos in snake_body:
            pygame.draw.rect(fenetre, BLANC, pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.display.flip()

        # Contrôle de la vitesse
        pygame.time.Clock().tick(SNAKE_SPEED)

    return False
        