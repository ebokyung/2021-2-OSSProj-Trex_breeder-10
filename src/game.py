from src.dino import *
from src.obstacle import *
from src.item import *
from src.interface import *
from db.db_interface import InterfDB


db = InterfDB("db/score.db")


## 시작 화면 ##
def introscreen():
    global on_pushtime;
    global off_pushtime
    global bgm_on
    global resized_screen, full_screen
    global high_score
    pygame.mixer.music.stop()
    temp_dino = Dino(dino_size[0], dino_size[1])
    temp_dino.isBlinking = True
    gameStart = False
    btnpush_interval = 500  # ms
    introscreen_txt_size1 = 15

    full_screen_txt = textsize(introscreen_txt_size1).render("FULL SCREEN", True, white)
    full_screen_txt_rect = full_screen_txt.get_rect()
    full_screen_txt_rect.bottomleft = (width * 0.87, height * 0.05)

    ###IMGLOAD###
    # BACKGROUND IMG LOAD
    temp_ground, temp_ground_rect = load_sprite_sheet('ground.png', 10, 1, -1, -1, -1)
    logo, logo_rect = load_image('logo.png', 360, 60, -1)
    Background, Background_rect = load_image('introscreenBG.png', width, height, -1)
    Background_rect.left = width * 0
    Background_rect.bottom = height

    r_btn_gamestart, r_btn_gamestart_rect = load_image(*resize('btn_start.png', 240, 60, -1))
    btn_gamestart, btn_gamestart_rect = load_image('btn_start.png', 240, 60, -1)
    r_btn_board, r_btn_board_rect = load_image(*resize('btn_board.png', 240, 60, -1))
    btn_board, btn_board_rect = load_image('btn_board.png', 240, 60, -1)
    r_btn_credit, r_btn_credit_rect = load_image(*resize('btn_credit.png', 240, 60, -1))
    btn_credit, btn_credit_rect = load_image('btn_credit.png', 240, 60, -1)
    # init_btn&bgm_btn
    btn_bgm_on, btn_bgm_on_rect = load_image('btn_bgm_on.png', 60, 60, -1);
    btn_bgm_off, btn_bgm_off_rect = load_image('btn_bgm_off.png', 60, 60, -1)
    r_btn_bgm_on, r_btn_bgm_on_rect = load_image(*resize('btn_bgm_on.png', 60, 60, -1))
    init_btn_image, init_btn_rect = load_image('scorereset.png', 60, 60, -1)
    r_init_btn_image, r_init_btn_rect = load_image(*resize('scorereset.png', 60, 60, -1))

    full_screen_on, full_screen_on_rect = load_image('full_screen_on.png', 120, 40, -1)
    full_screen_off, full_screen_off_rect = load_image('full_screen_off.png', 120, 40, -1)
    r_full_screen_on, r_full_screen_on_rect = load_image(*resize('full_screen_on.png', 120, 30, -1))
    r_full_screen_off, r_full_screen_off_rect = load_image(*resize('full_screen_off.png', 120, 30, -1))

    ###IMGPOS###
    # BACKGROUND IMG POS
    temp_ground_rect.bottomleft = (width / 20, height)
    logo_rect.center = (width * 0.22, height * 0.3)
    Background_rect.bottomleft = (width * 0, height)
    # BUTTONPOS
    btn_bgm_on_rect.center = (width * 0.3, height * (0.33 + 2 * button_offset))
    init_btn_rect.center = (width * 0.4, height * (0.33 + 2 * button_offset))
    full_screen_on_rect.bottomleft = (width * 0.85, height * 0.15)

    while not gameStart:
        if pygame.display.get_surface() == None:
            print("Couldn't load display surface")
            return True
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed() == (1, 0, 0):
                        x, y = event.pos
                        if r_btn_gamestart_rect.collidepoint(x, y):
                            temp_dino.isJumping = True
                            temp_dino.isBlinking = False
                            temp_dino.movement[1] = -1 * temp_dino.jumpSpeed

                        if r_btn_board_rect.collidepoint(x, y):
                            board()

                        if r_btn_credit_rect.collidepoint(x, y):
                            credit()

                        if r_full_screen_on_rect.collidepoint(x, y):
                            full_screen = not full_screen
                            if full_screen:
                                resized_screen = pygame.display.set_mode((monitor_size), pygame.FULLSCREEN)
                            else:
                                full_screen_issue()

                        if r_btn_bgm_on_rect.collidepoint(x, y) and bgm_on:
                            off_pushtime = pygame.time.get_ticks()
                            if off_pushtime - on_pushtime > btnpush_interval:
                                bgm_on = False

                        if r_btn_bgm_on_rect.collidepoint(x, y) and not bgm_on:
                            on_pushtime = pygame.time.get_ticks()
                            if on_pushtime - off_pushtime > btnpush_interval:
                                bgm_on = True

                        if r_init_btn_rect.collidepoint(x, y):
                            db.query_db("delete from user;")
                            db.commit()
                            high_score = 0

                if event.type == pygame.VIDEORESIZE and not full_screen:
                    checkscrsize(event.w, event.h)

        temp_dino.update()

        if pygame.display.get_surface() != None:

            screen.fill(background_col)
            screen.blit(temp_ground[0], temp_ground_rect)
            r_btn_gamestart_rect.centerx, r_btn_board_rect.centerx, r_btn_credit_rect.centerx = resized_screen.get_width() * 0.72, resized_screen.get_width() * 0.72, resized_screen.get_width() * 0.72
            r_btn_gamestart_rect.centery, r_btn_board_rect.centery, r_btn_credit_rect.centery = resized_screen.get_height() * 0.33, resized_screen.get_height() * (
                        0.33 + button_offset), resized_screen.get_height() * (0.33 + 2 * button_offset)
            r_init_btn_rect.centerx, r_init_btn_rect.centery = resized_screen.get_width() * 0.4, r_btn_credit_rect.centery
            screen.blit(Background, Background_rect)
            disp_intro_buttons(btn_gamestart, btn_board, btn_credit)
            screen.blit(init_btn_image, init_btn_rect)
            # fullscreen btn
            if full_screen:
                screen.blit(full_screen_on, full_screen_on_rect)
                r_full_screen_on_rect.bottomleft = (
                resized_screen.get_width() * 0.85, resized_screen.get_height() * 0.15)
                screen.blit(full_screen_txt, full_screen_txt_rect.bottomleft)
            if not full_screen:
                screen.blit(full_screen_off, full_screen_on_rect)
                r_full_screen_on_rect.bottomleft = (
                resized_screen.get_width() * 0.85, resized_screen.get_height() * 0.15)
                screen.blit(full_screen_txt, full_screen_txt_rect.bottomleft)
            # bgm on/off btn
            if bgm_on:
                screen.blit(btn_bgm_on, btn_bgm_on_rect)
                r_btn_bgm_on_rect.centerx, r_btn_bgm_on_rect.centery = resized_screen.get_width() * 0.3, r_btn_credit_rect.centery
            if not bgm_on:
                screen.blit(btn_bgm_off, btn_bgm_on_rect)
                r_btn_bgm_on_rect.centerx, r_btn_bgm_on_rect.centery = resized_screen.get_width() * 0.3, r_btn_credit_rect.centery
            if temp_dino.isBlinking:
                screen.blit(logo, logo_rect)
                # screen.blit(callout, callout_rect)
            temp_dino.draw()
            resized_screen.blit(
                pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                resized_screen_centerpos)
            pygame.display.update()

        clock.tick(FPS)
        if temp_dino.isJumping == False and temp_dino.isBlinking == False:
            gameStart = True
            gameplay()

    pygame.quit()
    quit()

## 게임 작동 ##
def gameplay():
    global resized_screen
    global high_score
    result = db.query_db("select score from user order by score desc;", one=True)
    if result is not None:
        high_score = result['score']
    if bgm_on:
        pygame.mixer.music.play(-1)  # 배경음악 실행
    gamespeed = 4
    startMenu = False
    gameOver = False
    gameQuit = False
    ###
    life = 3
    ###
    paused = False
    playerDino = Dino(dino_size[0], dino_size[1])
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
    last_obstacle = pygame.sprite.Group()
    shield_items = pygame.sprite.Group()
    life_items = pygame.sprite.Group()
    slow_items = pygame.sprite.Group()
    highjump_items = pygame.sprite.Group()

    Cactus.containers = cacti
    fire_Cactus.containers = fire_cacti
    Ptera.containers = pteras
    Cloud.containers = clouds
    ShieldItem.containers = shield_items
    LifeItem.containers = life_items
    SlowItem.containers = slow_items
    HighJumpItem.containers = highjump_items

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
                    if event.type == pygame.QUIT:
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
                            paused = pausing()

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
                for c in cacti:
                    c.movement[0] = -1 * gamespeed
                    if not playerDino.collision_immune:
                        if pygame.sprite.collide_mask(playerDino, c):
                            playerDino.collision_immune = True
                            life -= 1
                            collision_time = pygame.time.get_ticks()
                            if life == 0:
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
                            if life == 0:
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
                            collision_time = pygame.time.get_ticks()
                            if life == 0:
                                playerDino.isDead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

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
                else:
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

                    if pygame.time.get_ticks() - item_time > shield_time:
                        playerDino.collision_immune = False
                        playerDino.isSuper = False

                for l in life_items:
                    l.movement[0] = -1 * gamespeed
                    if pygame.sprite.collide_mask(playerDino, l):
                        if pygame.mixer.get_init() is not None:
                            checkPoint_sound.play()
                        life += 1
                        l.kill()
                    elif l.rect.right < 0:
                        l.kill()

                for k in slow_items:
                    k.movement[0] = -1 * gamespeed
                    if pygame.sprite.collide_mask(playerDino, k):
                        if pygame.mixer.get_init() is not None:
                            checkPoint_sound.play()
                        gamespeed -= 1
                        new_ground.speed += 1
                        k.kill()
                    elif k.rect.right < 0:
                        k.kill()

                for h in highjump_items:
                    h.movement[0] = -1 * gamespeed
                    if pygame.sprite.collide_mask(playerDino, h) and playerDino.rect.bottom != int(height * 0.98):
                        if pygame.mixer.get_init() is not None:
                            jump_sound.play()
                        playerDino.isJumping = True
                        playerDino.movement[1] = -1 * playerDino.superJumpSpeed
                    if h.rect.right < 0:
                        h.kill()

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

                if len(pteras) == 0 and random.randrange(PTERA_INTERVAL) == MAGIC_NUM and counter > PTERA_INTERVAL:
                    for l in last_obstacle:
                        if l.rect.right < OBJECT_REFRESH_LINE:
                            last_obstacle.empty()
                            last_obstacle.add(Ptera(gamespeed, ptera_size[0], ptera_size[1]))

                if len(clouds) < 5 and random.randrange(CLOUD_INTERVAL) == MAGIC_NUM:
                    Cloud(width, random.randrange(height / 5, height / 2))

                if len(shield_items) == 0 and random.randrange(
                        SHIELD_INTERVAL) == MAGIC_NUM and counter > SHIELD_INTERVAL:
                    for l in last_obstacle:
                        if l.rect.right < OBJECT_REFRESH_LINE:
                            last_obstacle.empty()
                            last_obstacle.add(ShieldItem(gamespeed, object_size[0], object_size[1]))

                if len(life_items) == 0 and random.randrange(
                        LIFE_INTERVAL) == MAGIC_NUM and counter > LIFE_INTERVAL * 2:
                    for l in last_obstacle:
                        if l.rect.right < OBJECT_REFRESH_LINE:
                            last_obstacle.empty()
                            last_obstacle.add(LifeItem(gamespeed, object_size[0], object_size[1]))

                if len(slow_items) == 0 and random.randrange(SLOW_INTERVAL) == MAGIC_NUM and counter > SLOW_INTERVAL:
                    for l in last_obstacle:
                        if l.rect.right < OBJECT_REFRESH_LINE:
                            last_obstacle.empty()
                            last_obstacle.add(SlowItem(gamespeed, object_size[0], object_size[1]))

                if len(highjump_items) == 0 and random.randrange(
                        HIGHJUMP_INTERVAL) == MAGIC_NUM and counter > HIGHJUMP_INTERVAL:
                    for l in last_obstacle:
                        if l.rect.right < OBJECT_REFRESH_LINE:
                            last_obstacle.empty()
                            last_obstacle.add(HighJumpItem(gamespeed, object_size[0], int(object_size[1] / 2)))

                            last_obstacle.empty()
                            last_obstacle.add(Cactus(gamespeed, int(object_size[0] * 2.5), int(object_size[1] * 1.5)))

                playerDino.update()
                cacti.update()
                fire_cacti.update()
                pteras.update()
                clouds.update()
                shield_items.update()
                life_items.update()
                highjump_items.update()
                new_ground.update()
                scb.update(playerDino.score)
                highsc.update(high_score)
                speed_indicator.update(gamespeed - 3)
                heart.update(life)
                slow_items.update()

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
                    fire_cacti.draw(screen)
                    pteras.draw(screen)
                    shield_items.draw(screen)
                    life_items.draw(screen)
                    slow_items.draw(screen)
                    highjump_items.draw(screen)
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
                            typescore(playerDino.score)
                            if not db.is_limit_data(playerDino.score):
                                db.query_db(
                                    f"insert into user(username, score) values ('{gamername}', '{playerDino.score}');")
                                db.commit()
                                board()
                            else:
                                board()

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

    pygame.quit()
    quit()


def board():
    global resized_screen
    gameQuit = False
    scroll_y = 0
    max_per_screen = 10
    results = db.query_db("select username, score from user order by score desc;")
    screen_board_height = resized_screen.get_height() + (len(results) // max_per_screen) * resized_screen.get_height()
    screen_board = pygame.surface.Surface((
        resized_screen.get_width(),
        screen_board_height
    ))

    title_image, title_rect = load_image("ranking.png", 360, 75, -1)
    title_rect.centerx = width * 0.5
    title_rect.centery = height * 0.2

    while not gameQuit:
        if pygame.display.get_surface() is None:
            gameQuit = True
        else:
            screen_board.fill(background_col)
            screen_board.blit(title_image, title_rect)
            for i, result in enumerate(results):
                top_i_surface = font.render(f"TOP {i + 1}", True, black)
                name_inform_surface = font.render("Name", True, black)
                score_inform_surface = font.render("Score", True, black)
                score_surface = font.render(str(result['score']), True, black)
                txt_surface = font.render(result['username'], True, black)

                screen_board.blit(top_i_surface, (width * 0.25, height * (0.55 + 0.1 * i)))
                screen_board.blit(name_inform_surface, (width * 0.4, height * 0.40))
                screen_board.blit(score_inform_surface, (width * 0.6, height * 0.40))
                screen_board.blit(txt_surface, (width * 0.4, height * (0.55 + 0.1 * i)))
                screen_board.blit(score_surface, (width * 0.6, height * (0.55 + 0.1 * i)))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameQuit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        gameQuit = True
                        introscreen()
                    if event.key == pygame.K_UP: scroll_y = min(scroll_y + 15, 0)
                    if event.key == pygame.K_DOWN: scroll_y = max(scroll_y - 15,
                                                                  -(len(results) // max_per_screen) * scr_size[1])
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4: scroll_y = min(scroll_y + 15, 0)
                    if event.button == 5: scroll_y = max(scroll_y - 15, -(len(results) // max_per_screen) * scr_size[1])
                    if event.button == 1:
                        gameQuit = True
                        introscreen()
                if event.type == pygame.VIDEORESIZE:
                    checkscrsize(event.w, event.h)

            screen.blit(screen_board, (0, scroll_y))
            resized_screen.blit(
                pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                resized_screen_centerpos)
            pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()


def pausing():
    global resized_screen
    gameQuit = False
    pause_pic, pause_pic_rect = load_image('paused.png', 360, 75, -1)
    pause_pic_rect.centerx = width * 0.5
    pause_pic_rect.centery = height * 0.2

    pygame.mixer.music.pause()  # 일시정지상태가 되면 배경음악도 일시정지

    # BUTTON IMG LOAD
    retbutton_image, retbutton_rect = load_image('main_button.png', 70, 62, -1)
    resume_image, resume_rect = load_image('continue_button.png', 70, 62, -1)

    resized_retbutton_image, resized_retbutton_rect = load_image(*resize('main_button.png', 70, 62, -1))
    resized_resume_image, resized_resume_rect = load_image(*resize('continue_button.png', 70, 62, -1))

    # BUTTONPOS
    retbutton_rect.centerx = width * 0.4;
    retbutton_rect.top = height * 0.52
    resume_rect.centerx = width * 0.6;
    resume_rect.top = height * 0.52

    resized_retbutton_rect.centerx = resized_screen.get_width() * 0.4
    resized_retbutton_rect.top = resized_screen.get_height() * 0.52
    resized_resume_rect.centerx = resized_screen.get_width() * 0.6
    resized_resume_rect.top = resized_screen.get_height() * 0.52

    while not gameQuit:
        if pygame.display.get_surface() is None:
            print("Couldn't load display surface")
            gameQuit = True
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameQuit = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.unpause()  # pausing상태에서 다시 esc누르면 배경음악 일시정지 해제
                        return False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed() == (1, 0, 0):
                        x, y = event.pos
                        if resized_retbutton_rect.collidepoint(x, y):
                            introscreen()

                        if resized_resume_rect.collidepoint(x, y):
                            pygame.mixer.music.unpause()  # pausing상태에서 오른쪽의 아이콘 클릭하면 배경음악 일시정지 해제

                            return False

                if event.type == pygame.VIDEORESIZE:
                    checkscrsize(event.w, event.h)

            screen.fill(white)
            screen.blit(pause_pic, pause_pic_rect)
            screen.blit(retbutton_image, retbutton_rect)
            screen.blit(resume_image, resume_rect)
            resized_screen.blit(
                pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                resized_screen_centerpos)
            pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()


def typescore(score):
    global resized_screen
    global gamername
    global width, height
    done = False
    active = True

    message_pos = (width * 0.25, height * 0.3)
    score_pos = (width * 0.35, height * 0.4)
    inputbox_pos = (width * 0.43, height * 0.5)
    typebox_size = 100
    letternum_restriction = 3
    input_box = pygame.Rect(inputbox_pos[0], inputbox_pos[1], 500, 50)
    color = pygame.Color('dodgerblue2')

    text = ''
    text2 = font.render("플레이어 이름을 입력해주세요", True, black)
    text3 = font.render(f"CURRENT SCORE: {score}", True, black)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                introscreen()
            if event.type == pygame.KEYDOWN:
                # if active:
                if event.key == pygame.K_RETURN:
                    gamername = text.upper()
                    done = True
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    if event.unicode.isalpha() == True:
                        if len(text) < letternum_restriction:
                            text += event.unicode

            if event.type == pygame.VIDEORESIZE:
                checkscrsize(event.w, event.h)

        screen.fill(white)
        txt_surface = textsize(50).render(text.upper(), True, color)
        input_box.w = typebox_size
        screen.blit(txt_surface, (input_box.centerx - len(text) * 11 - 5, input_box.y))
        screen.blit(text2, message_pos)
        screen.blit(text3, score_pos)
        pygame.draw.rect(screen, color, input_box, 2)
        resized_screen.blit(
            pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
            resized_screen_centerpos)

        pygame.display.flip()
        clock.tick(FPS)


def credit():
    global resized_screen
    done = False
    creditimg, creditimg_rect = load_image('credit.png', width, height, -1)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                return False
            if event.type == pygame.VIDEORESIZE:
                checkscrsize(event.w, event.h)
        screen.fill(white)
        screen.blit(creditimg, creditimg_rect)
        resized_screen.blit(
            pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
            resized_screen_centerpos)
        pygame.display.update()

        clock.tick(FPS)

    pygame.quit()
    quit()