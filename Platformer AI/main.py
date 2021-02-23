import pygame, os, neat
from imports import *
from background import Background
from platform import Platform, StartPlatform, update
from player import *
pygame.init()
SPAWNPLAT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWNPLAT, 1500)
WALK = pygame.USEREVENT + 2
pygame.time.set_timer(WALK, 200)
STAT_FONT = pygame.font.SysFont("comicsans", 50)

BGCOLOR = (255, 255, 255)
SCREENWIDTH = 800
SCREENHEIGHT = 800
FPS = 120
gen = 0
score = 0
highscore = 0
platforms = []
startPlatforms = []
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.flip()
pygame.display.set_caption("Wow What a NEAT Platformer!")

def collide(player, isJump, top, jumping, i):
    plat = Platform()
    for s in startPlatforms:
        if abs(s.x - player.x) < abs(plat.x - player.x):
            plat = s
    for p in platforms:
        if abs(p.x - player.x) < abs(plat.x - player.x):
            plat = p
    platRect = PLATFORMIMG.get_rect(topleft=(plat.x, plat.y))
    if player.getRect().colliderect(platRect):
        player.y = plat.y - PLAYERIMG.get_height()
        top[i] = False
        jumping[i] = False
    else:
        if isJump[i] == False:
            jumping[i] = True
            player.fall()
    return player.y, top, jumping, plat

def end():
    pygame.quit()
    quit()
    run = False

def main(genomes, config):
    '''
    Declare vars for both neat-python and game
    '''
    global gen
    global platforms
    global startPlatforms
    global score
    global highscore
    score = 0
    gen += 1
    bg = Background()
    for i in range(7):
        startPlatforms.append(StartPlatform(i))
    nets = []
    ge = []
    players = []
    isJump = []
    top = []
    jumping = []
    limits = []
    playNums = 0
    plat = Platform()
    for _, g in genomes:
        playNums += 1
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        players.append(Player())
        g.fitness = 0
        ge.append(g)
        isJump.append(False)
        top.append(False)
        jumping.append(False)
        limits.append(players[playNums - 1].y - players[playNums - 1].jumpHeight)

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    end()
            if event.type == SPAWNPLAT:
                platforms.append(Platform())
                score += 1
                if highscore < score:
                    highscore = score
            if event.type == WALK:
                for player in players:
                    player.update()

        '''
        Loop through player list and pass needed variables into activate function
        '''
        for x, player in enumerate(players):
            player.draw(screen)
            ge[x].fitness += .2

            output = nets[x].activate((player.x, player.y, plat.x, plat.y, PLATFORMIMG.get_width()))

            if output[0] > 0.5:
                if jumping[x] == False:
                    isJump[x] = True
                    jumping[x] = True
                    limits[x] = player.y - player.jumpHeight
            else:
                isJump[x] = False

        bg.move(screen)
        update(platforms, screen, startPlatforms)

        '''
        Check for collisions between player and platform
        '''
        for i, player in enumerate(players):
            player.y, top, jumping, plat = collide(player, isJump, top, jumping, i)

        '''
        Add or subtract fitness from each player depending on what they do i.e if a player dies subtract from his fitness
        '''
        for i, player in enumerate(players):
            if player.y <= limits[i]:
                top[i] = True
            if top[i] == True:
                isJump[i] = False
            if player.y >= 810 or player.y <= -100:
                ge[i].fitness -= 10
                nets.pop(i)
                ge.pop(i)
                players.pop(i)
            if len(players) <= 0:
                run = False
                platforms.clear()
                startPlatforms.clear()
            player.jump(isJump, top, i)
            player.draw(screen)

        '''
        Display info such as generation and score on screen
        '''
        text = STAT_FONT.render("Gen: " + str(gen), 1, (0, 0, 0))
        screen.blit(text, (SCREENWIDTH - 10 - text.get_width(), 10))
        text = STAT_FONT.render("Score: " + str(score), 1, (0, 0, 0))
        screen.blit(text, (0, 10))
        text = STAT_FONT.render("Highscore: " + str(highscore), 1, (0, 0, 0))
        screen.blit(text, ((SCREENWIDTH //2) - (text.get_width()//2), 10))
        pygame.display.update()
        
def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, 
                        neat.DefaultSpeciesSet, neat.DefaultStagnation, 
                        config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main,50)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)