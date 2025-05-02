import pygame
import random
from settings import *

# Classe Button pour la fenêtre de fin de partie
class Button:
    def __init__(self, x, y, largeur, hauteur, texte):
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        self.texte = texte
        self.couleur = BLANC
        self.couleur_texte = NOIR
        self.font = pygame.font.Font(None, 36)

    def dessiner(self, surface):
        # Dessine le rectangle du bouton
        pygame.draw.rect(surface, self.couleur, self.rect)
        pygame.draw.rect(surface, NOIR, self.rect, 2)
        
        # Dessiner le texte
        texte_surface = self.font.render(self.texte, True, self.couleur_texte)
        texte_rect = texte_surface.get_rect(center=self.rect.center)
        surface.blit(texte_surface, texte_rect)

    def est_clique(self, pos):
        return self.rect.collidepoint(pos)

def afficher_fin_partie(fenetre, score):
    global HIGH_SCORE
    
    # Mettre à jour le record si nécessaire
    if score > HIGH_SCORE:
        HIGH_SCORE = score
    
    # Créer les boutons
    bouton_rejouer = Button(WINDOW_WIDTH // 2 - 220, WINDOW_HEIGHT // 2 + 50, 200, 50, "REJOUER")
    bouton_reglages = Button(WINDOW_WIDTH // 2 + 20, WINDOW_HEIGHT // 2 + 50, 200, 50, "RÉGLAGES")
    
    affichage_actif = True
    while affichage_actif:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUITTER"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "MENU"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_rejouer.est_clique(event.pos):
                    return "REJOUER"
                if bouton_reglages.est_clique(event.pos):
                    return "REGLAGES"
        
        # Fond semi-transparent
        fond = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        fond.set_alpha(200)
        fond.fill(NOIR)
        fenetre.blit(fond, (0, 0))
        
        # Titre
        font_titre = pygame.font.SysFont(None, 72)
        titre_text = font_titre.render("GAME OVER", True, ROUGE)
        titre_rect = titre_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100))
        fenetre.blit(titre_text, titre_rect)
        
        # Score
        font_score = pygame.font.SysFont(None, 48)
        score_text = font_score.render(f"Score: {score}", True, BLANC)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30))
        fenetre.blit(score_text, score_rect)
        
        # Record
        record_text = font_score.render(f"Record: {HIGH_SCORE}", True, JAUNE)
        record_rect = record_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10))
        fenetre.blit(record_text, record_rect)
        
        # Boutons
        bouton_rejouer.dessiner(fenetre)
        bouton_reglages.dessiner(fenetre)
        
        pygame.display.flip()
        pygame.time.Clock().tick(30)
    
    return "MENU"

def lancer_jeu(fenetre):
    global SCORE, HIGH_SCORE
    
    # Réinitialiser le score au début du jeu
    SCORE = 0
    
    #Variable du jeu
    snake_pos = [GAME_AREA_X + 50, GAME_AREA_Y + 50]
    snake_body = [[GAME_AREA_X + 50, GAME_AREA_Y + 50],    # Tête du serpent, position initiale
                  [GAME_AREA_X + 40, GAME_AREA_Y + 50],    # Premier segment du corps, 10px derrière la tête
                  [GAME_AREA_X + 30, GAME_AREA_Y + 50],    # Deuxième segment, 10px derrière le premier
                  [GAME_AREA_X + 20, GAME_AREA_Y + 50],    # Troisième segment
                  [GAME_AREA_X + 10, GAME_AREA_Y + 50], 
                  [GAME_AREA_X + 10, GAME_AREA_Y + 50],
                  [GAME_AREA_X, GAME_AREA_Y + 50]]
       
    direction = "RIGHT"
    changer_direction = direction
    
    fruit_position = [GAME_AREA_X + random.randrange(1, (GAME_AREA_WIDTH//10))*10,
                      GAME_AREA_Y + random.randrange(1, (GAME_AREA_HEIGHT//10))*10]

    fruit_spawn = True
    
    # Variable pour gérer la pause
    jeu_en_pause = False

    #Boucle principale du jeu
    jeu_actif = True
    while jeu_actif:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    jeu_en_pause = not jeu_en_pause  # Inverser l'état de pause
                # Gestion des touches directionnelles (seulement si le jeu n'est pas en pause)
                if not jeu_en_pause:
                    if event.key == pygame.K_UP and direction != "DOWN":
                        changer_direction = "UP"
                    if event.key == pygame.K_DOWN and direction != "UP":
                        changer_direction = "DOWN"
                    if event.key == pygame.K_RIGHT and direction != "LEFT":
                        changer_direction = "RIGHT"
                    if event.key == pygame.K_LEFT and direction != "RIGHT":
                        changer_direction = "LEFT"

        # Ne mettre à jour le jeu que s'il n'est pas en pause
        if not jeu_en_pause:
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

            # Vérification des collisions avec les bords de la zone de jeu
            if (snake_pos[0] < GAME_AREA_X or snake_pos[0] >= GAME_AREA_X + GAME_AREA_WIDTH or
                snake_pos[1] < GAME_AREA_Y or snake_pos[1] >= GAME_AREA_Y + GAME_AREA_HEIGHT):
                # Game over si le serpent touche les bords
                action = afficher_fin_partie(fenetre, SCORE)
                if action == "REJOUER":
                    return lancer_jeu(fenetre)
                elif action == "REGLAGES":
                    return reglages(fenetre)
                else:
                    return False

            # Vérification des collisions avec le corps du serpent
            for segment in snake_body[1:]:  # Parcours du corps du serpent (sans la tête)
                if snake_pos[0] == segment[0] and snake_pos[1] == segment[1]:
                    # Game over si le serpent se touche lui-même
                    action = afficher_fin_partie(fenetre, SCORE)
                    if action == "REJOUER":
                        return lancer_jeu(fenetre)
                    elif action == "REGLAGES":
                        return reglages(fenetre)
                    else:
                        return False
            
            # Mise à jour du corps du serpent
            snake_body.insert(0, list(snake_pos))                                         # Ajoute la nouvelle position de la tête au début du corps
            if snake_pos[0] == fruit_position[0] and snake_pos[1] == fruit_position[1]:   # Vérifie si le serpent mange le fruit
                SCORE += 10                                                               # Augmente le score
                # Mettre à jour le record si nécessaire
                if SCORE > HIGH_SCORE:
                    HIGH_SCORE = SCORE
                fruit_spawn = False                                                       # Indique qu'un nouveau fruit doit apparaître
            else:
                snake_body.pop()                                                          # Supprime le dernier segment du corps si pas de fruit mangé
            
            if not fruit_spawn:                                                          # Si le fruit a été mangé
                fruit_position = [GAME_AREA_X + random.randrange(1, (GAME_AREA_WIDTH//10)) * 10,         
                                GAME_AREA_Y + random.randrange(1, (GAME_AREA_HEIGHT//10)) * 10]            
                
            fruit_spawn = True                                                # Indique qu'un fruit est présent sur le terrain
        
        # Affichage (toujours effectué, même en pause)
        fenetre.fill(NOIR)
        
        # Dessiner la zone de jeu avec une bordure
        pygame.draw.rect(fenetre, GRIS, pygame.Rect(GAME_AREA_X - 2, GAME_AREA_Y - 2, 
                                                   GAME_AREA_WIDTH + 4, GAME_AREA_HEIGHT + 4), 2)
        
        # Dessiner l'intérieur de la zone de jeu
        pygame.draw.rect(fenetre, NOIR, pygame.Rect(GAME_AREA_X, GAME_AREA_Y, GAME_AREA_WIDTH, GAME_AREA_HEIGHT))
        
        # Afficher le score
        font = pygame.font.SysFont(None, 30)
        score_text = font.render(f"Score: {SCORE}", True, BLANC)
        fenetre.blit(score_text, (10, 10))
        
        # Afficher le record
        record_text = font.render(f"Record: {HIGH_SCORE}", True, JAUNE)
        record_rect = record_text.get_rect()
        record_rect.centerx = WINDOW_WIDTH // 2
        record_rect.top = 10
        fenetre.blit(record_text, record_rect)
        
        # Afficher la vitesse
        font_vitesse = pygame.font.SysFont(None, 30)
        vitesse_text = font_vitesse.render(f"Vitesse: {SNAKE_SPEED}", True, BLANC)
        vitesse_rect = vitesse_text.get_rect()
        vitesse_rect.right = WINDOW_WIDTH - 10
        vitesse_rect.top = 10
        fenetre.blit(vitesse_text, vitesse_rect)
        
        # Dessiner le serpent
        for pos in snake_body:
            pygame.draw.rect(fenetre, VERT, pygame.Rect(pos[0], pos[1], 10, 10))
        
        # Dessiner le fruit
        pygame.draw.rect(fenetre, BLANC, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))
        
        # Afficher le message de pause si le jeu est en pause
        if jeu_en_pause:
            # Créer un fond semi-transparent pour le message
            pause_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            pause_surface.set_alpha(180)  # Semi-transparent (0-255)
            pause_surface.fill(NOIR)
            fenetre.blit(pause_surface, (0, 0))
            
            # Afficher le message de pause
            font_pause = pygame.font.SysFont(None, 72)
            pause_text = font_pause.render("JEU EN PAUSE", True, BLANC)
            pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            fenetre.blit(pause_text, pause_rect)
            
            # Afficher les instructions
            font_instructions = pygame.font.SysFont(None, 30)
            instructions_text = font_instructions.render("Appuyez sur ÉCHAP pour continuer", True, GRIS)
            instructions_rect = instructions_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
            fenetre.blit(instructions_text, instructions_rect)
        
        pygame.display.flip()

        # Contrôle de la vitesse (toujours actif même en pause pour répondre aux événements)
        pygame.time.Clock().tick(SNAKE_SPEED)

    return False

def reglages(fenetre):
    global SNAKE_SPEED
    
    reglages_actif = True
    vitesse_actuelle = SNAKE_SPEED
    
    # Définir les options de vitesse
    options_vitesse = [
        {"texte": "Lente", "valeur": 10},
        {"texte": "Normale", "valeur": 15},
        {"texte": "Rapide", "valeur": 20},
        {"texte": "Très rapide", "valeur": 30}
    ]
    
    # Trouver l'option correspondant à la vitesse actuelle
    option_selectionnee = 0
    for i, option in enumerate(options_vitesse):
        if option["valeur"] == vitesse_actuelle:
            option_selectionnee = i
            break
    
    # Pour stocker les rectangles des options (pour la détection des clics)
    option_rects = []
    
    while reglages_actif:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
                # Navigation entre les options
                if event.key == pygame.K_UP:
                    option_selectionnee = max(0, option_selectionnee - 1)
                if event.key == pygame.K_DOWN:
                    option_selectionnee = min(len(options_vitesse) - 1, option_selectionnee + 1)
                # Validation du choix
                if event.key == pygame.K_RETURN:
                    SNAKE_SPEED = options_vitesse[option_selectionnee]["valeur"]
                    reglages_actif = False  # Sortir des réglages
            
            # Gestion des clics de souris
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(option_rects):
                    if rect.collidepoint(event.pos):
                        option_selectionnee = i
                        SNAKE_SPEED = options_vitesse[i]["valeur"]
                        reglages_actif = False  # Sortir des réglages
        
        # Affichage
        fenetre.fill(NOIR)
        
        # Titre
        font_titre = pygame.font.SysFont(None, 48)
        titre_text = font_titre.render("Réglages", True, BLANC)
        fenetre.blit(titre_text, (WINDOW_WIDTH // 2 - titre_text.get_width() // 2, 50))
        
        # Instructions
        font_instructions = pygame.font.SysFont(None, 24)
        instructions_text = font_instructions.render("Utilisez les flèches haut/bas pour sélectionner, Entrée pour valider ou cliquez directement", True, GRIS)
        fenetre.blit(instructions_text, (WINDOW_WIDTH // 2 - instructions_text.get_width() // 2, 100))
        
        # Réinitialiser la liste des rectangles
        option_rects = []
        
        # Options de vitesse
        font_option = pygame.font.SysFont(None, 36)
        for i, option in enumerate(options_vitesse):
            # Couleur et style selon la sélection
            couleur = JAUNE if i == option_selectionnee else BLANC
            texte = f"> {option['texte']} <" if i == option_selectionnee else option['texte']
            
            option_text = font_option.render(texte, True, couleur)
            text_pos = (WINDOW_WIDTH // 2 - option_text.get_width() // 2, 180 + i * 50)
            fenetre.blit(option_text, text_pos)
            
            # Stocker le rectangle pour la détection des clics
            rect = option_text.get_rect()
            rect.topleft = text_pos
            option_rects.append(rect)
            
            # Dessiner un rectangle invisible autour de l'option pour élargir la zone cliquable
            zone_cliquable = pygame.Rect(rect.left - 20, rect.top - 5, rect.width + 40, rect.height + 10)
            # Dessiner un contour pour visualiser la zone cliquable (optionnel, à commenter en production)
            # pygame.draw.rect(fenetre, GRIS, zone_cliquable, 1)
            option_rects[i] = zone_cliquable
        
        pygame.display.flip()
        pygame.time.Clock().tick(30)
    
    return True
        