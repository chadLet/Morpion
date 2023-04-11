# Import des librairies
import pygame
import sys

pygame.init()

# Création de la fenêtre
width, height = 2560, 1440
screen = pygame.display.set_mode((width, height))

size = 300

x = width / 2 - 450
y = height / 2 - 450

# Sert à savoir à quel tour nous sommes
turn = 0

# Créations des couleurs
black = 39, 48, 48
grey = 113, 120, 119
white = 255, 255, 255

screen.fill((149, 191, 187))

# Affichage de la grille
pygame.draw.rect(screen, black, [x - 50, y - 50, 1000, 1000], 200)

# Créations de listes pour stocker les positions des croix et des ronds
positions = []
takenPositions = []
circlePos = []
crossPos = []

taken = False

# Création de la police d'écriture
myfont = pygame.font.SysFont("Arial", 100)

# Création des scores et des positions de diagonales
scoreR = 0
scoreC = 0
diag1 = [(1580.0, 1020.0), (1280.0, 720.0), (980.0, 420.0)]
diag2 = [(1580.0, 420.0), (1280.0, 720.0), (980.0, 1020.0)]


# Réinitialise la fenêtre
def clear():
    x = width / 2 - 450
    y = height / 2 - 450
    colorChooser = 0
    for i in range(0, 3):
        for j in range(0, 3):
            if colorChooser % 2 == 0:
                pygame.draw.rect(screen, white, [x, y, size, size])
                positions.append((x + 150, y + 150))
            else:
                pygame.draw.rect(screen, grey, [x, y, size, size])
                positions.append((x + 150, y + 150))
            y += 300
            colorChooser += 1
        y = height / 2 - 450
        x += 300


# Algorithme de victoire (Bof...)
def check(pos):
    try:
        for i in range(0, len(pos)):
            pos.sort(key=lambda tup: abs(tup[0]), reverse=True)
            if pos[i][0] == pos[i + 1][0] == pos[i + 2][0]:
                return True
            elif (pos[i] == diag1[0] and pos[i + 1] == diag1[1] and pos[i + 2] == diag1[2]) \
                    or (pos[i] == diag1[0] and pos[i + 1] == diag1[1] and pos[i + 3] == diag1[2]):
                return True
            elif (pos[i] == diag2[0] and pos[i + 1] == diag2[1] and pos[i + 2] == diag2[2]) \
                    or (pos[i] == diag2[0] and pos[i + 1] == diag2[1] and pos[i + 3] == diag2[2]):
                return True
            else:
                pos.sort(key=lambda tup: abs(tup[1]))
                if pos[i][1] == pos[i + 1][1] == pos[i + 2][1]:
                    return True
        return False
    except:
        pass


# Update du score
def update():
    offset = 0
    text = ['Score;', f'Ronds: {scoreR}', f'Croix: {scoreC}']
    for i in text:
        score = myfont.render(i, True, black)
        screen.blit(score, (50, height * 0.35 + offset))
        offset += 150


update()
clear()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        # Affiche une croix ou un rond sur la case cliquée en fonction du tour
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not check(circlePos) and not check(crossPos):
                mousePos = []
                cx, cy = pygame.mouse.get_pos()
                for i in range(0, len(positions)):
                    mousePos.append((positions[i][0] - cx, positions[i][1] - cy))
                sortedL = mousePos
                sortedL.sort(key=lambda tup: abs(tup[0]))
                L = [sortedL[0], sortedL[1], sortedL[2]]
                L.sort(key=lambda tup: abs(tup[1]))
                L = L[0][0], L[0][1]
                cx, cy = L[0] + cx, L[1] + cy
                if cx - x < 0 or cx + x > width or cy - y < 0 or cy + y > height:
                    pass
                else:
                    if turn % 2 == 0:
                        for i in takenPositions:
                            if i == (cx, cy):
                                taken = True
                        if not taken:
                            pygame.draw.ellipse(screen, black, [cx - 125, cy - 125, 250, 250], 20)
                            takenPositions.append((cx, cy))
                            circlePos.append((cx, cy))
                            turn += 1
                            if check(circlePos):
                                label = myfont.render("Les ronds ont gagnés!", True, black)
                                screen.blit(label, (width / 2 - 400, 50))
                                scoreR += 1
                                pygame.draw.rect(screen, (149, 191, 187), [50, height * 0.35, 500, 500])
                                update()
                            else:
                                pass
                        else:
                            taken = False
                    else:
                        for i in takenPositions:
                            if i == (cx, cy):
                                taken = True
                        if not taken:
                            pygame.draw.line(screen, black, [cx - 125, cy - 125], [cx + 125, cy + 125], 30)
                            pygame.draw.line(screen, black, [cx - 125, cy + 125], [cx + 125, cy - 125], 30)
                            takenPositions.append((cx, cy))
                            crossPos.append((cx, cy))
                            turn += 1
                            if check(crossPos):
                                label = myfont.render("Les croix ont gagnées!", True, black)
                                screen.blit(label, (width / 2 - 400, 50))
                                scoreC += 1
                                pygame.draw.rect(screen, (149, 191, 187), [50, height * 0.35, 500, 500])
                                update()
                            else:
                                pass
                        else:
                            taken = False
            else:
                pass

        if event.type == pygame.KEYDOWN:
            # Réinitialise la fenêtre avec la touche echap
            if event.key == pygame.K_ESCAPE:
                screen.fill((149, 191, 187))
                pygame.draw.rect(screen, black, [x - 50, y - 50, 1000, 1000], 200)
                update()
                clear()
                turn = 0
                takenPositions = []
                circlePos = []
                crossPos = []

    # Update la fenêtre
    pygame.display.update()
