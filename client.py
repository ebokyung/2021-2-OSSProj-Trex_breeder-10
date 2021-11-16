import pygame
from src.game import *
from network import Network
from src.setting import *


dino_type = ['ORIGINAL','RED','ORANGE','YELLOW','GREEN','PURPLE','BLACK','PINK']
#Player class를 기존에 있던 Dino class를 활용#

#TODO: set different starting positions for dinos per player

class Dino():
    def __init__(self, sizex=-1, sizey=-1,type = None):
        
        # 디노의 타입을 결정합니다. 
        self.type = type

        if type == 'ORIGINAL':
            self.images, self.rect = load_sprite_sheet('dino.png', 6, 1, sizex, sizey, -1)
            # self.images, self.rect = load_sprite_sheet('pinkdino.png', 6, 1, sizex, sizey, -1)
            self.images1, self.rect1 = load_sprite_sheet('dino_ducking.png', 2, 1, 59, sizey, -1)
            # self.images1, self.rect1 = load_sprite_sheet('pinkdino_ducking.png', 2, 1, 59, sizey, -1)
        elif type == 'PINK':
            self.images, self.rect = load_sprite_sheet('pink_dino.png', 6, 1, sizex, sizey, -1)
            self.images1, self.rect1 = load_sprite_sheet('pink_dino_ducking.png', 2, 1, 59, sizey, -1)
        elif type == 'RED':
            self.images, self.rect = load_sprite_sheet('red_dino.png', 6, 1, sizex, sizey, -1)
            self.images1, self.rect1 = load_sprite_sheet('red_dino_ducking.png', 2, 1, 59, sizey, -1)    
        elif type == 'ORANGE':
            self.images, self.rect = load_sprite_sheet('orange_dino.png', 6, 1, sizex, sizey, -1)
            self.images1, self.rect1 = load_sprite_sheet('orange_dino_ducking.png', 2, 1, 59, sizey, -1) 
        elif type == 'YELLOW':
            self.images, self.rect = load_sprite_sheet('yellow_dino.png', 6, 1, sizex, sizey, -1)
            self.images1, self.rect1 = load_sprite_sheet('yellow_dino_ducking.png', 2, 1, 59, sizey, -1)
        elif type == 'GREEN':
            self.images, self.rect = load_sprite_sheet('green_dino.png', 6, 1, sizex, sizey, -1)
            self.images1, self.rect1 = load_sprite_sheet('green_dino_ducking.png', 2, 1, 59, sizey, -1)
        elif type == 'PURPLE':
            self.images, self.rect = load_sprite_sheet('purple_dino.png', 6, 1, sizex, sizey, -1)
            self.images1, self.rect1 = load_sprite_sheet('purple_dino_ducking.png', 2, 1, 59, sizey, -1)  
        elif type == 'BLACK':
            self.images, self.rect = load_sprite_sheet('black_dino.png', 6, 1, sizex, sizey, -1)
            self.images1, self.rect1 = load_sprite_sheet('black_dino_ducking.png', 2, 1, 59, sizey, -1)    
        else: 
            self.images, self.rect = load_sprite_sheet('dino.png', 6, 1, sizex, sizey, -1)
            self.images1, self.rect1 = load_sprite_sheet('dino_ducking.png', 2, 1, 59, sizey, -1)
        # 

        self.rect.bottom = int(0.98*height)
        self.rect.left = width/15
        self.image = self.images[0]
        self.index = 0
        self.counter = 0
        self.score = 0
        self.isJumping = False
        self.isDead = False
        self.isDucking = False
        self.isBlinking = False
        self.movement = [0, 0]
        self.jumpSpeed = 11.5
        self.superJumpSpeed = self.jumpSpeed * 1.3
        self.collision_immune = False
        self.isSuper = False

        self.stand_pos_width = self.rect.width
        self.duck_pos_width = self.rect1.width

    def draw(self):
        screen.blit(self.image,self.rect)

    ## 충돌 판단 ##
    def checkbounds(self):
        if self.rect.bottom > int(0.98*height):
            self.rect.bottom = int(0.98*height)
            self.isJumping = False

    def update(self):
        if self.isJumping:
            self.movement[1] = self.movement[1] + gravity

        if self.isJumping:
            self.index = 0
        elif self.isBlinking:
            if self.index == 0:
                if self.counter % 400 == 399:
                    self.index = (self.index + 1)%2
            else:
                if self.counter % 20 == 19:
                    self.index = (self.index + 1)%2

        elif self.isDucking:
            if self.counter % 5 == 0:
                self.index = (self.index + 1)%2
        else:
            if self.counter % 5 == 0:
                self.index = (self.index + 1)%2 + 2

        if self.isDead:
            self.index = 4

        if self.collision_immune:
            if self.counter % 10 == 0:
                self.index = 5

        if not self.isDucking:
            self.image = self.images[self.index]
            self.rect.width = self.stand_pos_width
        else:
            self.image = self.images1[self.index % 2]
            if self.collision_immune is True:
                if self.counter % 5 == 0:
                    self.image = self.images[5]
            self.rect.width = self.duck_pos_width

        self.rect = self.rect.move(self.movement)
        self.checkbounds()

        if not self.isDead and self.counter % 7 == 6 and self.isBlinking == False:
            self.score += 1
            if self.score % 100 == 0 and self.score != 0:
                if pygame.mixer.get_init() != None:
                    checkPoint_sound.play()

        self.counter = (self.counter + 1)

def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


def redrawWindow(win,player, player2):
    win.fill((255,255,255))
    player.draw(win)
    player2.draw(win)
    pygame.display.update()


def main():
    run = True
    n = Network()
    #startPos = read_pos(n.getPos())
    
    player1 = Dino(dino_size[0], dino_size[1], type=dino_type[1])
    player2 = Dino(dino_size[0], dino_size[1], type=dino_type[0])
    #TODO: health of dinos, speed of dinos, item effect to dinos..
    #OPINION: I'm guessing it should be classified in Dino class 
    #but this issue needs further discussion w/ members on how to handle this

    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        global resized_screen
        global high_score
        result = db.query_db("select score from user order by score desc;", one=True)
        if result is not None:
            high_score = result['score']
        #    if bgm_on:
        #       pygame.mixer.music.play(-1) # 배경음악 실행
        gamespeed = 4
        startMenu = False
        gameOver = False
        gameQuit = False
        ###
        life = 7
        ###
        paused = False

        new_ground = Ground(-1 * gamespeed)
        scb = Scoreboard()
        highsc = Scoreboard(width * 0.78)
        heart = HeartIndicator(life)
        speed_indicator = Scoreboard(width * 0.12, height * 0.15)
        counter = 0

        speed_text = font.render("SPEED", True, black)

        cacti = pygame.sprite.Group()
        fire_cacti = pygame.sprite.Group()
        pteras = pygame.sprite.Group()
        clouds = pygame.sprite.Group()
        # add stones
        stones = pygame.sprite.Group()

        last_obstacle = pygame.sprite.Group()
        shield_items = pygame.sprite.Group()
        life_items = pygame.sprite.Group()
        slow_items = pygame.sprite.Group()
        # highjump_items = pygame.sprite.Group()

        Stone.containers = stones

        Cactus.containers = cacti
        fire_Cactus.containers = fire_cacti
        Ptera.containers = pteras
        Cloud.containers = clouds
        ShieldItem.containers = shield_items
        LifeItem.containers = life_items
        SlowItem.containers = slow_items
        # HighJumpItem.containers = highjump_items

        # BUTTON IMG LOAD
        # retbutton_image, retbutton_rect = load_image('replay_button.png', 70, 62, -1)
        gameover_image, gameover_rect = load_image('game_over.png', 380, 22, -1)

        temp_images, temp_rect = load_sprite_sheet('numbers.png', 12, 1, 11, int(15 * 6 / 5), -1)
        HI_image = pygame.Surface((30, int(15 * 6 / 5)))
        HI_rect = HI_image.get_rect()
        HI_image.fill(background_col)
        HI_image.blit(temp_images[10], temp_rect)
        temp_rect.left += temp_rect.width
        HI_image.blit(temp_images[11], temp_rect)
        HI_rect.top = height * 0.05
        HI_rect.left = width * 0.73

        while not gameQuit:
            while startMenu:
                pass
            while not gameOver:
                if pygame.display.get_surface() == None:
                    print("Couldn't load display surface")
                    gameQuit = True
                    gameOver = True


                else:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:  # 종료
                            gameQuit = True
                            gameOver = True

                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:  # 스페이스 누르는 시점에 공룡이 땅에 닿아있으면 점프한다.
                                if player1.rect.bottom == int(0.98 * height):
                                    player1.isJumping = True
                                    if pygame.mixer.get_init() != None:
                                        jump_sound.play()
                                    player1.movement[1] = -1 * player1.jumpSpeed

                            if event.key == pygame.K_DOWN:  # 아래방향키를 누르는 시점에 공룡이 점프중이지 않으면 숙인다.
                                if not (player1.isJumping and player1.isDead):
                                    player1.isDucking = True

                            if event.key == pygame.K_ESCAPE:
                                paused = not paused
                                paused = pausing()

                        if event.type == pygame.KEYUP:
                            if event.key == pygame.K_DOWN:
                                player1.isDucking = False

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if pygame.mouse.get_pressed() == (1, 0, 0) and player1.rect.bottom == int(0.98 * height):
                                # (mouse left button, wheel button, mouse right button)
                                player1.isJumping = True
                                if pygame.mixer.get_init() != None:
                                    jump_sound.play()
                                player1.movement[1] = -1 * player1.jumpSpeed

                            if pygame.mouse.get_pressed() == (0, 0, 1):
                                # (mouse left button, wheel button, mouse right button)
                                if not (player1.isJumping and player1.isDead):
                                    player1.isDucking = True

                        if event.type == pygame.MOUSEBUTTONUP:
                            player1.isDucking = False

                        if event.type == pygame.VIDEORESIZE:
                            checkscrsize(event.w, event.h)

                if not paused:

                    for s in stones:
                        s.movement[0] = -1 * gamespeed
                        if not player1.collision_immune:
                            if pygame.sprite.collide_mask(player1, s):
                                player1.collision_immune = True
                                life -= 1
                                collision_time = pygame.time.get_ticks()
                                if life == 0:
                                    player1.isDead = True
                                if pygame.mixer.get_init() is not None:
                                    die_sound.play()

                    for c in cacti:
                        c.movement[0] = -1 * gamespeed
                        if not player1.collision_immune:
                            if pygame.sprite.collide_mask(player1, c):
                                player1.collision_immune = True
                                life -= 1
                                collision_time = pygame.time.get_ticks()
                                if life == 0:
                                    player1.isDead = True
                                if pygame.mixer.get_init() is not None:
                                    die_sound.play()

                        elif not player1.isSuper:
                            immune_time = pygame.time.get_ticks()
                            if immune_time - collision_time > collision_immune_time:
                                player1.collision_immune = False

                    for f in fire_cacti:
                        f.movement[0] = -1 * gamespeed
                        if not player1.collision_immune:
                            if pygame.sprite.collide_mask(player1, f):
                                player1.collision_immune = True
                                life -= 1
                                collision_time = pygame.time.get_ticks()
                                if life == 0:
                                    player1.isDead = True
                                if pygame.mixer.get_init() is not None:
                                    die_sound.play()

                        elif not player1.isSuper:
                            immune_time = pygame.time.get_ticks()
                            if immune_time - collision_time > collision_immune_time:
                                player1.collision_immune = False

                    for p in pteras:
                        p.movement[0] = -1 * gamespeed
                        if not player1.collision_immune:
                            if pygame.sprite.collide_mask(player1, p):
                                player1.collision_immune = True
                                life -= 1
                                collision_time = pygame.time.get_ticks()
                                if life == 0:
                                    player1.isDead = True
                                if pygame.mixer.get_init() is not None:
                                    die_sound.play()

                        elif not player1.isSuper:
                            immune_time = pygame.time.get_ticks()
                            if immune_time - collision_time > collision_immune_time:
                                player1.collision_immune = False


                        elif not player1.isSuper:
                            immune_time = pygame.time.get_ticks()
                            if immune_time - collision_time > collision_immune_time:
                                player1.collision_immune = False

                    if not player1.isSuper:
                        for s in shield_items:
                            s.movement[0] = -1 * gamespeed
                            if pygame.sprite.collide_mask(player1, s):
                                if pygame.mixer.get_init() is not None:
                                    checkPoint_sound.play()
                                player1.collision_immune = True
                                player1.isSuper = True
                                s.kill()
                                item_time = pygame.time.get_ticks()
                            elif s.rect.right < 0:
                                s.kill()

                    STONE_INTERVAL = 50

                    CACTUS_INTERVAL = 50
                    PTERA_INTERVAL = 300
                    CLOUD_INTERVAL = 300
                    SHIELD_INTERVAL = 500
                    LIFE_INTERVAL = 1000
                    SLOW_INTERVAL = 1000
                    HIGHJUMP_INTERVAL = 300
                    OBJECT_REFRESH_LINE = width * 0.8
                    MAGIC_NUM = 10

                    #TODO: fix random appearance of obstacle 
                    #REASON: obstacles are shown differently to clients - looks like they are not in the same map

                    if len(cacti) < 2:
                        if len(cacti) == 0:
                            last_obstacle.empty()
                            last_obstacle.add(Cactus(gamespeed, object_size[0], object_size[1]))
                        else:
                            for l in last_obstacle:
                                if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(CACTUS_INTERVAL) == MAGIC_NUM:
                                    last_obstacle.empty()
                                    last_obstacle.add(Cactus(gamespeed, object_size[0], object_size[1]))

                    if len(fire_cacti) < 2:
                        for l in last_obstacle:
                            if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(CACTUS_INTERVAL * 5) == MAGIC_NUM:
                                last_obstacle.empty()
                                last_obstacle.add(fire_Cactus(gamespeed, object_size[0], object_size[1]))

                    if len(stones) < 2:
                        for l in last_obstacle:
                            if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(STONE_INTERVAL * 3) == MAGIC_NUM:
                                last_obstacle.empty()
                                last_obstacle.add(Stone(gamespeed, object_size[0], object_size[1]))

                    if len(pteras) == 0 and random.randrange(PTERA_INTERVAL) == MAGIC_NUM and counter > PTERA_INTERVAL:
                        for l in last_obstacle:
                            if l.rect.right < OBJECT_REFRESH_LINE:
                                last_obstacle.empty()
                                last_obstacle.add(Ptera(gamespeed, ptera_size[0], ptera_size[1]))

                    if len(clouds) < 5 and random.randrange(CLOUD_INTERVAL) == MAGIC_NUM:
                        Cloud(width, random.randrange(height / 5, height / 2))
                    
                    # 여기선 x,y가 아닌 Dino객체에서 바뀌는 bottom과 left를 넘겨준다
                    p2Pos = read_pos(n.send(make_pos((player1.rect.bottom, player1.rect.left))))
                    player2.rect.bottom = p2Pos[0]
                    player2.rect.left = p2Pos[1]
                    print(p2Pos)

                    cacti.update()
                    fire_cacti.update()
                    pteras.update()
                    clouds.update()
                    shield_items.update()
                    life_items.update()
                            # highjump_items.update()
                    new_ground.update()
                    scb.update(player1.score)
                    highsc.update(high_score)
                    speed_indicator.update(gamespeed - 3)
                    heart.update(life)
                    slow_items.update()
                    stones.update()
                    player1.update()
                    player2.update()
                    if pygame.display.get_surface() != None:
                        screen.fill(background_col)
                        new_ground.draw()
                        clouds.draw(screen)
                        scb.draw()
                        speed_indicator.draw()
                        screen.blit(speed_text, (width * 0.01, height * 0.13))
                        heart.draw()
                        if high_score != 0:
                            highsc.draw()
                            screen.blit(HI_image, HI_rect)
                        cacti.draw(screen)
                        stones.draw(screen)
                        fire_cacti.draw(screen)
                        pteras.draw(screen)
                        shield_items.draw(screen)
                        life_items.draw(screen)
                        slow_items.draw(screen)
                        # highjump_items.draw(screen)
                        player1.draw()
                        player2.draw()
                        resized_screen.blit(
                            pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                            resized_screen_centerpos)
                        pygame.display.update()

main()