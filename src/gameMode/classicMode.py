from src.dino import *
from src.obstacle import *
from src.item import *
from src.interface import *
from src.gameState import *
from db.db_interface import InterfDB

db = InterfDB("db/score.db")

## 게임 작동 ##
def gameplay_easy(player):
    global resized_screen
    global high_score
    global introFlag
    result = db.query_db("select score from user order by score desc;", one=True)
    if result is not None:
        high_score = result['score']
    #    if bgm_on:
    #       pygame.mixer.music.play(-1) # 배경음악 실행
    #보경 - 작은익룡 맞으면 감속
    #게임을 실행하면 실제 움직이는 initial gamespeed는 4(4~13)이고, 사용자에게는 가장 낮은 speed인 1(1~10)로 인식하는 값임
    global gamespeed 
    gamespeed= 4
    def gamespeed_down():
        global gamespeed
        if gamespeed > 4:
            gamespeed -= 1

    startMenu = False
    gameOver = False
    gameQuit = False
    ###
    life = 10
    max_life = 10
    ###
    paused = False

    playerDino = player

    new_ground = Ground(-1 * gamespeed)
    scb = Scoreboard()
    highsc = Scoreboard(width * 0.78)
    heart = HeartIndicator(max_life, life)
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
                            if playerDino.rect.bottom == int(0.98 * height):
                                playerDino.isJumping = True
                                if pygame.mixer.get_init() != None:
                                    jump_sound.play()
                                playerDino.movement[1] = -1 * playerDino.jumpSpeed

                        if event.key == pygame.K_DOWN:  # 아래방향키를 누르는 시점에 공룡이 점프중이지 않으면 숙인다.
                            if not (playerDino.isJumping and playerDino.isDead):
                                playerDino.isDucking = True

                        if event.key == pygame.K_ESCAPE:
                            paused = not paused
                            pause_value, return_home_value = pausing()
                            if pause_value != None:
                                paused = pause_value
                            else:
                                introFlag = return_home_value
                                return introFlag

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_DOWN:
                            playerDino.isDucking = False

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pygame.mouse.get_pressed() == (1, 0, 0) and playerDino.rect.bottom == int(0.98 * height):
                            # (mouse left button, wheel button, mouse right button)
                            playerDino.isJumping = True
                            if pygame.mixer.get_init() != None:
                                jump_sound.play()
                            playerDino.movement[1] = -1 * playerDino.jumpSpeed

                        if pygame.mouse.get_pressed() == (0, 0, 1):
                            # (mouse left button, wheel button, mouse right button)
                            if not (playerDino.isJumping and playerDino.isDead):
                                playerDino.isDucking = True

                    if event.type == pygame.MOUSEBUTTONUP:
                        playerDino.isDucking = False

                    if event.type == pygame.VIDEORESIZE:
                        checkscrsize(event.w, event.h)

            if not paused:

                for s in stones:
                    s.movement[0] = -1 * gamespeed
                    if not playerDino.collision_immune:
                        if pygame.sprite.collide_mask(playerDino, s):
                            playerDino.collision_immune = True
                            life -= 1
                            collision_time = pygame.time.get_ticks()
                            if life <= 0:
                                playerDino.isDead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                for c in cacti:
                    c.movement[0] = -1 * gamespeed
                    if not playerDino.collision_immune:
                        if pygame.sprite.collide_mask(playerDino, c):
                            playerDino.collision_immune = True
                            life -= 1
                            collision_time = pygame.time.get_ticks()
                            if life <= 0:
                                playerDino.isDead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                    elif not playerDino.isSuper:
                        immune_time = pygame.time.get_ticks()
                        if immune_time - collision_time > collision_immune_time:
                            playerDino.collision_immune = False

                for f in fire_cacti:
                    f.movement[0] = -1 * gamespeed
                    if not playerDino.collision_immune:
                        if pygame.sprite.collide_mask(playerDino, f):
                            playerDino.collision_immune = True
                            life -= 1
                            collision_time = pygame.time.get_ticks()
                            if life <= 0:
                                playerDino.isDead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                    elif not playerDino.isSuper:
                        immune_time = pygame.time.get_ticks()
                        if immune_time - collision_time > collision_immune_time:
                            playerDino.collision_immune = False

                for p in pteras:
                    p.movement[0] = -1 * gamespeed
                    if not playerDino.collision_immune:
                        if pygame.sprite.collide_mask(playerDino, p):
                            playerDino.collision_immune = True
                            life -= 1
                            gamespeed_down()
                            collision_time = pygame.time.get_ticks()
                            if life <= 0:
                                playerDino.isDead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                    elif not playerDino.isSuper:
                        immune_time = pygame.time.get_ticks()
                        if immune_time - collision_time > collision_immune_time:
                            playerDino.collision_immune = False


                    elif not playerDino.isSuper:
                        immune_time = pygame.time.get_ticks()
                        if immune_time - collision_time > collision_immune_time:
                            playerDino.collision_immune = False

                if not playerDino.isSuper:
                    for s in shield_items:
                        s.movement[0] = -1 * gamespeed
                        if pygame.sprite.collide_mask(playerDino, s):
                            if pygame.mixer.get_init() is not None:
                                checkPoint_sound.play()
                            playerDino.collision_immune = True
                            playerDino.isSuper = True
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

                playerDino.update()
                cacti.update()
                fire_cacti.update()
                pteras.update()
                clouds.update()
                shield_items.update()
                life_items.update()
                # highjump_items.update()
                new_ground.update()
                scb.update(playerDino.score)
                highsc.update(high_score)
                speed_indicator.update(gamespeed - 3)
                heart.update(life)
                slow_items.update()

                stones.update()

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
                    playerDino.draw()
                    resized_screen.blit(
                        pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                        resized_screen_centerpos)
                    pygame.display.update()
                clock.tick(FPS)

                if playerDino.isDead:
                    gameOver = True
                    pygame.mixer.music.stop()  # 죽으면 배경음악 멈춤
                    if playerDino.score > high_score:
                        high_score = playerDino.score

                if counter % speed_up_limit_count == speed_up_limit_count - 1:
                    new_ground.speed -= 1
                    if gamespeed < 13:
                        gamespeed += 1

                counter = (counter + 1)

        if gameQuit:
            break

        while gameOver:
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                gameQuit = True
                gameOver = False
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameQuit = True
                        gameOver = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            gameQuit = True
                            gameOver = False

                        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            gameOver = False
                            gameQuit = True
                            gamername = typescore(playerDino.score)
                            if not db.is_limit_data(playerDino.score):
                                db.query_db(
                                    f"insert into user(username, score) values ('{gamername}', '{playerDino.score}');")
                                db.commit()
                                introFlag = board()
                            else:
                                introFlag = board()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        gameOver = False
                        gameQuit = True
                        typescore(playerDino.score)
                        if not db.is_limit_data(playerDino.score):
                            db.query_db(
                                f"insert into user(username, score) values ('{gamername}', '{playerDino.score}');")
                            db.commit()
                            board()
                        else:
                            board()

                    if event.type == pygame.VIDEORESIZE:
                        checkscrsize(event.w, event.h)

            highsc.update(high_score)
            if pygame.display.get_surface() != None:
                disp_gameOver_msg(gameover_image)
                if high_score != 0:
                    highsc.draw()
                    screen.blit(HI_image, HI_rect)
                resized_screen.blit(
                    pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                    resized_screen_centerpos)
                pygame.display.update()
            clock.tick(FPS)
    return introFlag
    pygame.quit()
    quit()
