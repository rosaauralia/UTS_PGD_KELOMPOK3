import pygame, random, sys, time
from pygame.locals import *
import pygame_menu

#start menu

#set up some variables
WINDOWWIDTH = 1024
WINDOWHEIGHT = 600
FPS = 60

MAXGOTTENPASS = 10
MOUSESIZE = 70 #includes newKindMOUSEs
ADDNEWMOUSERATE = 30
ADDNEWKINDMOUSE = ADDNEWMOUSERATE

NORMALMOUSESPEED = 2
NEWKINDMOUSESPEED = NORMALMOUSESPEED / 2

PLAYERMOVERATE = 15
BULLETSPEED = 10
ADDNEWBULLETRATE = 15


TEXTCOLOR = (255, 255, 255)
RED = (255, 0, 0)

def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # pressing escape quits
                    terminate()
                if event.key == K_RETURN:
                    return

def playerHasHitMOUSE(playerRect, MOUSEs):
    for z in MOUSEs:
        if playerRect.colliderect(z['rect']):
            return True
    return False

def bulletHasHitMOUSE(bullets, MOUSEs):
    for b in bullets:
        if b['rect'].colliderect(z['rect']):
            bullets.remove(b)
            return True
    return False

def bulletHasHitCrawler(bullets, newKindMOUSEs):
    for b in bullets:
        if b['rect'].colliderect(c['rect']):
            bullets.remove(b)
            return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# set up pygame, the window, and the mouse cursor
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))#, pygame.FULLSCREEN)
pygame.display.set_caption('Mouse Defence')
pygame.mouse.set_visible(False)

# set up fonts
font = pygame.font.SysFont(None, 48)

# set up sounds
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('grasswalk.mp3')

# set up images
playerImage = pygame.image.load('Petani_3-.png')
playerRect = playerImage.get_rect()

bulletImage = pygame.image.load('Anak Panah1.png')
bulletRect = bulletImage.get_rect()

MOUSEImage = pygame.image.load('Tikus 1.png')
newKindMOUSEImage = pygame.image.load('badguy3.png')

backgroundImage = pygame.image.load('background.png')
rescaledBackground = pygame.transform.scale(backgroundImage, (WINDOWWIDTH, WINDOWHEIGHT))


# show the "Start" screen
windowSurface.blit(rescaledBackground, (0, 0))
windowSurface.blit(playerImage, (WINDOWWIDTH / 2, WINDOWHEIGHT - 70))
drawText('Press Enter to start', font, windowSurface, (WINDOWWIDTH / 3) - 10, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()
while True:
    # set up the start of the game

    MOUSEs = []
    newKindMOUSEs = []
    bullets = []

    MOUSEsGottenPast = 0
    score = 0

    playerRect.topleft = (50, WINDOWHEIGHT /2)
    moveLeft = moveRight = False
    moveUp=moveDown = False
    shoot = False

    MOUSEAddCounter = 0
    newKindMOUSEAddCounter = 0
    bulletAddCounter = 40
    pygame.mixer.music.play(-1, 0.0)

    while True: # the game loop runs while the game part is playing
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True

                if event.key == K_SPACE:
                    shoot = True

            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                        terminate()

                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False
                
                if event.key == K_SPACE:
                    shoot = False

        # Add new MOUSEs at the top of the screen, if needed.
        MOUSEAddCounter += 1
        if MOUSEAddCounter == ADDNEWKINDMOUSE:
            MOUSEAddCounter = 0
            MOUSESize = MOUSESIZE       
            newMOUSE = {'rect': pygame.Rect(WINDOWWIDTH, random.randint(10,WINDOWHEIGHT-MOUSESize-10), MOUSESize, MOUSESize),
                        'surface':pygame.transform.scale(MOUSEImage, (MOUSESize, MOUSESize)),
                        }

            MOUSEs.append(newMOUSE)

        # Add new newKindMOUSEs at the top of the screen, if needed.
        newKindMOUSEAddCounter += 1
        if newKindMOUSEAddCounter == ADDNEWMOUSERATE:
            newKindMOUSEAddCounter = 0
            newKindMOUSEsize = MOUSESIZE
            newCrawler = {'rect': pygame.Rect(WINDOWWIDTH, random.randint(10,WINDOWHEIGHT-newKindMOUSEsize-10), newKindMOUSEsize, newKindMOUSEsize),
                        'surface':pygame.transform.scale(newKindMOUSEImage, (newKindMOUSEsize, newKindMOUSEsize)),
                        }
            newKindMOUSEs.append(newCrawler)

        # add new bullet
        bulletAddCounter += 1
        if bulletAddCounter >= ADDNEWBULLETRATE and shoot == True:
            bulletAddCounter = 0
            newBullet = {'rect':pygame.Rect(playerRect.centerx+10, playerRect.centery-25, bulletRect.width, bulletRect.height),
						 'surface':pygame.transform.scale(bulletImage, (bulletRect.width, bulletRect.height)),
						}
            bullets.append(newBullet)

        # Move the player around.
        if moveUp and playerRect.top > 30:
            playerRect.move_ip(0,-1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT-10:
            playerRect.move_ip(0,PLAYERMOVERATE)

        # Move the MOUSEs down.
        for z in MOUSEs:
            z['rect'].move_ip(-1*NORMALMOUSESPEED, 0)

        # Move the newKindMOUSEs down.
        for c in newKindMOUSEs:
            c['rect'].move_ip(-1*NEWKINDMOUSESPEED,0)

        # move the bullet
        for b in bullets:
            b['rect'].move_ip(1 * BULLETSPEED, 0)

        # Delete MOUSEs that have fallen past the bottom.
        for z in MOUSEs[:]:
            if z['rect'].left < 0:
                MOUSEs.remove(z)
                MOUSEsGottenPast += 1

        # Delete newKindMOUSEs that have fallen past the bottom.
        for c in newKindMOUSEs[:]:
            if c['rect'].left <0:
                newKindMOUSEs.remove(c)
                MOUSEsGottenPast += 1
		
        for b in bullets[:]:
            if b['rect'].right>WINDOWWIDTH:
                bullets.remove(b)
                
                # check if the bullet has hit the MOUSE
        for z in MOUSEs:
            if bulletHasHitMOUSE(bullets, MOUSEs):
                score += 1
                MOUSEs.remove(z)
    
        for c in newKindMOUSEs:
            if bulletHasHitCrawler(bullets, newKindMOUSEs):
                score += 1
                newKindMOUSEs.remove(c)      

        # Draw the game world on the window.
        windowSurface.blit(rescaledBackground, (0, 0))

        # Draw the player's rectangle, rails
        windowSurface.blit(playerImage, playerRect)

        # Draw each baddie
        for z in MOUSEs:
            windowSurface.blit(z['surface'], z['rect'])

        for c in newKindMOUSEs:
            windowSurface.blit(c['surface'], c['rect'])

        # draw each bullet
        for b in bullets:
            windowSurface.blit(b['surface'], b['rect'])

        # Draw the score and how many MOUSEs got past
        drawText('Mouse gotten past: %s' % (MOUSEsGottenPast), font, windowSurface, 10, 20)
        drawText('score: %s' % (score), font, windowSurface, 10, 50)

        # update the display
        pygame.display.update()
            
        # Check if any of the MOUSEs has hit the player.
        if playerHasHitMOUSE(playerRect, MOUSEs):
            break
        if playerHasHitMOUSE(playerRect, newKindMOUSEs):
           break
        
        # check if score is over MAXGOTTENPASS which means game over
        if MOUSEsGottenPast >= MAXGOTTENPASS:
            break

        mainClock.tick(FPS)

    # Stop the game and show the "Game Over" screen.
    pygame.mixer.music.stop()
    gameOverSound.play()
    time.sleep(1)
    if MOUSEsGottenPast >= MAXGOTTENPASS:
        windowSurface.blit(rescaledBackground, (0, 0))
        windowSurface.blit(playerImage, (WINDOWWIDTH / 2, WINDOWHEIGHT - 70))
        drawText('score: %s' % (score), font, windowSurface, 10, 30)
        drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
        drawText('YOUR COUNTRY HAS BEEN DESTROIED', font, windowSurface, (WINDOWWIDTH / 4)- 80, (WINDOWHEIGHT / 3) + 100)
        drawText('Press enter to play again or escape to exit', font, windowSurface, (WINDOWWIDTH / 4) - 80, (WINDOWHEIGHT / 3) + 150)
        pygame.display.update()
        waitForPlayerToPressKey()
    if playerHasHitMOUSE(playerRect, MOUSEs):
        windowSurface.blit(rescaledBackground, (0, 0))
        windowSurface.blit(playerImage, (WINDOWWIDTH / 2, WINDOWHEIGHT - 70))
        drawText('score: %s' % (score), font, windowSurface, 10, 30)
        drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
        drawText('YOU HAVE BEEN KISSED BY THE MOUSE', font, windowSurface, (WINDOWWIDTH / 4) - 80, (WINDOWHEIGHT / 3) +100)
        drawText('Press enter to play again or escape to exit', font, windowSurface, (WINDOWWIDTH / 4) - 80, (WINDOWHEIGHT / 3) + 150)
        pygame.display.update()
        waitForPlayerToPressKey()
    gameOverSound.stop()
