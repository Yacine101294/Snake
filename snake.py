import pygame
import time
import random

pygame.init()
snake_speed = 15

#Taille de l'écran pour affichage
fenetre = pygame.display.set_mode((600, 480))
pygame.display.set_caption("Snake Game")

# Création d'une surface de la même taille que la fenêtre
background=pygame.Surface(fenetre.get_size())
# Conversion de la surface pour optimiser l'affichage
background = background.convert()
# Remplissage de la surface avec une couleur blanche (RGB: 250, 250, 250)
background.fill((250, 250, 250))

#Afficher du texte
font = pygame.font.Font(None, 36)                         # Création d'une police de caractères de taille 36
text = font.render("Bienvenu dans le jeu Snake", 1, (10, 10, 10))  # Création du texte avec la police choisie, en noir (RGB: 10, 10, 10)
textpos = text.get_rect()                                # Récupération de la position du texte
textpos.centerx= background.get_rect().centerx           # Centrage horizontal du texte sur le fond
background.blit(text, textpos)                           # Affichage du texte sur le fond aux coordonnées définies

#Afficher tout à l'écran
fenetre.blit(background, (0, 0))      # Affichage du fond sur la fenêtre aux coordonnées (0,0)
pygame.display.flip()                  # Mise à jour de l'affichage

#Boucle d'événements
fond = pygame.image.load("C:/Users/yacdu/Desktop/Python/Mes projets/Snake/assets/asset.1.png").convert()
fond = pygame.transform.scale(fond, fenetre.get_size())

continuer = True                                         # Variable pour contrôler la boucle principale du jeu
while continuer:                                        # Boucle principale qui continue tant que continuer est True
    for event in pygame.event.get():                    # Parcours de tous les événements pygame en attente
        if event.type == pygame.QUIT:                   # Si l'utilisateur clique sur le bouton de fermeture de la fenêtre
            continuer = False                           # On met continuer à False pour sortir de la boucle
        fenetre.blit(fond, (0, 0))                # Rafraîchissement du fond d'écran
        pygame.display.flip()                           # Mise à jour de l'affichage