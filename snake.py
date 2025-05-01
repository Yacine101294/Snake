import pygame
import time
import random
from settings import *  # Importer les paramètres
from game import lancer_jeu  # Importer la fonction de jeu

pygame.init()


BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
GRIS = (200, 200, 200)

#Création d'une classe Button pour faciliter la gestion des boutons
class Button:
    def __init__(self, x, y, largeur, hauteur, texte):                    # Méthode d'initialisation avec les paramètres de position (x,y), taille et texte du bouton
        self.rect = pygame.Rect(x, y, largeur, hauteur)                   # Création d'un rectangle pygame avec les dimensions spécifiées
        self.texte=texte                                                  # Stockage du texte à afficher sur le bouton
        self.couleur= BLANC                                               # Définition de la couleur de fond du bouton (blanc par défaut)
        self.couleur_texte = NOIR                                         # Définition de la couleur du texte (noir par défaut)
        self.font = pygame.font.Font(None, 36)                            # Création d'une police de caractères de taille 36

    def dessiner(self, surface):                                          # Surface est l'objet pygame sur lequel on va dessiner (fenêtre ou autre surface)
        #Dessine le rectangle du bouton
        pygame.draw.rect(surface, self.couleur, self.rect)                # Dessine le rectangle avec la couleur de fond
        pygame.draw.rect(surface, NOIR, self.rect, 2)                     # Dessine la bordure noire de 2 pixels
        
        #Dessiner le texte
        texte_surface = self.font.render(self.texte, True, self.couleur_texte)  # Crée une surface avec le texte rendu
        texte_rect = texte_surface.get_rect(center=self.rect.center)      # Centre le texte dans le rectangle du bouton
        surface.blit(texte_surface, texte_rect)                       # Affiche le texte sur la surface aux coordonnées calculées

    def est_clique(self, pos):                    # Méthode qui vérifie si un point donné est sur le bouton
        return self.rect.collidepoint(pos)        # Retourne True si les coordonnées 'pos' sont dans le rectangle du bouton

#Création des boutons
bouton_start = Button(75, 215, 200, 50, "START")
bouton_reglages = Button(325, 215, 200, 50, "REGLAGES")

#Taille de l'écran pour affichage
fenetre = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake Game")

# Création d'une surface de la même taille que la fenêtre
background = pygame.Surface(fenetre.get_size())

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

#Charger l'image de fond
fond = pygame.image.load("C:/Users/yacdu/Desktop/Python/Mes projets/Snake/assets/asset.1.png").convert()
fond = pygame.transform.scale(fond, fenetre.get_size())

#Boucle principale
continuer = True
while continuer:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False
        # Gestion du clic sur les boutons
        if event.type == pygame.MOUSEBUTTONDOWN:
            if bouton_start.est_clique(event.pos):
                print("Démarrage du jeu...")
                continuer = lancer_jeu(fenetre)
            elif bouton_reglages.est_clique(event.pos):
                print("Réglages cliqués!")
                
    # Affichage du menu
    fenetre.blit(fond, (0, 0))
    bouton_start.dessiner(fenetre)  # Dessine le bouton
    bouton_reglages.dessiner(fenetre)
    pygame.display.flip()

# Quitter proprement Pygame
pygame.quit()