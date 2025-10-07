import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = True
posPlayer1 = [15, 270]
posPlayer2 = [780, 270]
posBall = [400, 300]

dirname="/Users/fosebad/Desktop/repositories/com-grafica/pong/"
width = 800
velPlayer = 500

velBallX = 5
velBallY = 5

pointsPlayer1 = 0
pointsPlayer2 = 0

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    #Linea Superior
    lineaSup = pygame.draw.line(screen, "white", [0, 0], [800, 0], 10)
    #Linea izquierda
    lineaIzq = pygame.draw.line(screen, "white", [0, 0], [0, 600], 10)
    #Linea derecha
    lineaDer = pygame.draw.line(screen, "white", [800, 0], [800, 600], 10)
    #Linea inferior
    lineaInf = pygame.draw.line(screen, "white", [0, 600], [800, 600], 10)
    #Linea central
    lineaCentr = pygame.draw.aaline(screen, "white", [400, 0], [400, 600], 10)

    player1 = pygame.draw.rect(screen, "white", [posPlayer1[0], posPlayer1[1], 10, 60])
    player2 = pygame.draw.rect(screen, "white", [posPlayer2[0], posPlayer2[1], 10, 60])
    ball = pygame.draw.circle(screen, "white", posBall, 10)

    # draw scores
    font = pygame.font.SysFont("monospace", 100)
    text = font.render( str(pointsPlayer2), True, "white")
    screen.blit(text, [(width/2)-200, 100])

    # draw scores
    font = pygame.font.SysFont("monospace", 100)
    text = font.render( str(pointsPlayer1), True, "white")
    screen.blit(text, [(width/2)+200, 100])

    # RENDER YOUR GAME HERE
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        posPlayer1[1] -= velPlayer * dt
    if keys[pygame.K_s]:
        posPlayer1[1] += velPlayer * dt
    if keys[pygame.K_a]:
        posPlayer1[0] -= velPlayer * dt
    if keys[pygame.K_d]:
        posPlayer1[0] += velPlayer * dt
    if keys[pygame.K_UP]:
        posPlayer2[1] -= velPlayer * dt
    if keys[pygame.K_DOWN]:
        posPlayer2[1] += velPlayer * dt
    if keys[pygame.K_LEFT]:
        posPlayer2[0] -= velPlayer * dt
    if keys[pygame.K_RIGHT]:
        posPlayer2[0] += velPlayer * dt

    posBall[0] += velBallX
    posBall[1] += velBallY
    if ball.colliderect(player1):
        velBallX = -velBallX
        pygame.mixer.Sound(dirname + "Raqueta.mp3").play()
        posBall[0] = posPlayer1[0] + 33
    if ball.colliderect(player2):
        velBallX = -velBallX
        pygame.mixer.Sound(dirname + "Raqueta.mp3").play()
        posBall[0] = posPlayer2[0] - 40

    if ball.colliderect(lineaSup):
        velBallY = -velBallY
        posBall[1] = 26
        pygame.mixer.Sound(dirname + "Rebote.mp3").play()
    
    if ball.colliderect(lineaInf):
        velBallY = -velBallY
        posBall[1] = 574


    if (posBall[0] < 0): 
         posBall = [400, 300]
         pointsPlayer1 += 1
         pygame.mixer.Sound(dirname + "Gol.mp3").play()
    elif (posBall[0] > 800):
         posBall = [400, 300]
         pygame.mixer.Sound(dirname + "Gol.mp3").play()
         pointsPlayer2 += 1

    # flip() the display to put your work on screen
    pygame.display.flip()

    if player1.colliderect(lineaSup):
        posPlayer1[1] = 6
    if player2.colliderect(lineaSup):
        posPlayer2[1] = 6
    if player1.colliderect(lineaInf):
        posPlayer1[1] = 536
    if player2.colliderect(lineaInf):
        posPlayer2[1] = 536
    if player1.colliderect(lineaIzq):
        posPlayer1[0] = 6
    if player2.colliderect(lineaCentr):
        posPlayer2[0] = 406
    if player2.colliderect(lineaDer):
        posPlayer2[0] = 786
    if player1.colliderect(lineaCentr):
        posPlayer1[0] = 386

    dt = clock.tick(60) / 1000  # limits FPS to 60 and returns delta time in seconds

pygame.quit()