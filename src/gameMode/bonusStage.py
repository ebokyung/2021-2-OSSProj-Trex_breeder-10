

from src.dino import *
from src.obstacle import *
from src.item import *
from src.interface import *
from db.db_interface import InterfDB

db = InterfDB("db/score.db")

def gameplay_bonus(cur_stage, cur_life, cur_speed, cur_score):
    global resized_screen
    global high_score
    result = db.query_db("select score from user order by score desc;", one=True)
    if result is not None:
        high_score = result['score']

    # 남현 - 211104 스테이지 변수 추가
    stage = cur_stage

    # HERE: REMOVE SOUND!!
    # if bgm_on:
    #     pygame.mixer.music.play(-1)  # 배경음악 실행

    # 남현 - 211104 이전 스테이지에서 게임 스피드 변수 받기
    gamespeed = cur_speed  # 원래 기본값 : 4

    startMenu = False
    gameOver = False
    gameQuit = False
    ###

    #

    # 남현 - 211104 이전 스테이지에서 게임 life 변수 받기
    life = cur_life
    max_life = 15

    ###
    paused = False

    # 디노 타입 때문에 변경된 부분
    playerDino = Dino(dino_size[0], dino_size[1], type=dino_type[type_idx])
    #

    # 남현 - 211104 전 스테이지의 스코어 유지
    playerDino.score = cur_score;

    new_ground = Ground(-1 * gamespeed)
    scb = Scoreboard()
    highsc = Scoreboard(width * 0.78)
    heart = HeartIndicator(max_life, life)
    speed_indicator = Scoreboard(width * 0.12, height * 0.15)
    counter = 0

    # 남현 - 211104 스테이지에 맞춰 SPEED 글씨 색상 변경
    speed_text = font.render("SPEED", True, black)

    cacti = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    last_obstacle = pygame.sprite.Group()
    life_items = pygame.sprite.Group()

    Cactus.containers = cacti
    Cloud.containers = clouds
    LifeItem.containers = life_items


    # BUTTON IMG LOAD
    # retbutton_image, retbutton_rect = load_image('replay_button.png', 70, 62, -1)
    gameover_image, gameover_rect = load_image('game_over.png', 380, 22, -1)



    temp_images, temp_rect = load_sprite_sheet('numbers.png', 12, 1, 11, int(15 * 6 / 5), -1)
    HI_image = pygame.Surface((30, int(15 * 6 / 5)))
    HI_rect = HI_image.get_rect()

    # 남현 - 211104 스테이지에 맞게 배경색 설정
    # 남현 - 211109 보너스 스테이지 이미지는 기본 이미지
    HI_image.fill(background_col)

    HI_image.blit(temp_images[10], temp_rect)
    temp_rect.left += temp_rect.width
    HI_image.blit(temp_images[11], temp_rect)
    HI_rect.top = height * 0.05
    HI_rect.left = width * 0.73

    # 1. 미사일 발사.
    space_go = False
    m_list = []
    bk = 0


    # 방향키 구현
    goLeft = False
    goRight = False
    #


    jumpingx2 = False

    # 남현 - 211030 타이머기능 추가
    # 시작 시간 정보
    start_ticks = pygame.time.get_ticks()  # 현재 tick 을 받아옴
    # total time
    total_time = 20
    elapsed_time = 0  # elapsed_time을 미리 선언+초기화를 안 하면 보스등장조건에서 사용 불가

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

                        if event.key == pygame.K_LEFT:
                            # print("left")
                            goLeft = True

                        if event.key == pygame.K_RIGHT:
                            # print("right")
                            goRight = True

                        if event.key == pygame.K_ESCAPE:
                            paused = not paused
                            paused = pausing()

                        # jumping x2 ( press key s)
                        if event.key == pygame.K_s:
                            jumpingx2 = True

                        # 2. a키를 누르면, 미사일이 나갑니다.
                        if event.key == pygame.K_a:
                            space_go = True
                            bk = 0
                        #

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_DOWN:
                            playerDino.isDucking = False

                        # 3.a키에서 손을 떼면, 미사일이 발사 되지 않습니다.
                        if event.key == pygame.K_a:
                            space_go = False
                        #

                        # 방향키 추가
                        if event.key == pygame.K_LEFT:
                            goLeft = False

                        if event.key == pygame.K_RIGHT:
                            goRight = False
                        #

                        ## jumgpingx2
                        if event.key == pygame.K_s:
                            jumpingx2 = False

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

                # 방향키
                if goLeft:
                    if playerDino.rect.left <= 0:
                        playerDino.rect.left =0
                    else:
                        playerDino.rect.left = playerDino.rect.left -(gamespeed)

                if goRight:
                    if playerDino.rect.right >= width:
                        playerDino.rect.right = width
                    else:
                        playerDino.rect.right = playerDino.rect.right +(gamespeed)
                #

                # 4. space_go가 True이고, 일정 시간이 지나면, 미사일을 만들고, 이를 미사일 배열에 넣습니다.
                if (space_go == True) and (int(bk % 15) == 0):
                    # print(bk)
                    mm = obj()

                    # 디노의 종류에 따라 다른 총알이 나가도록 합니다.
                    if playerDino.type == 'RED':
                        mm.put_img("./sprites/black_bullet.png")
                        mm.change_size(10, 10)
                    elif playerDino.type == 'YELLOW':
                        mm.put_img("./sprites/blue_bullet.png")
                        mm.change_size(10, 10)
                    elif playerDino.type == 'ORANGE':
                        mm.put_img("./sprites/blue_bullet.png")
                        mm.change_size(10, 10)
                    elif playerDino.type == 'PURPLE':
                        mm.put_img("./sprites/pink_bullet.png")
                        mm.change_size(15, 5)
                    elif playerDino.type == 'PINK':
                        mm.put_img("./sprites/heart_bullet.png")
                        mm.change_size(10, 10)
                    else:
                        mm.put_img("./sprites/red_bullet.png")
                        mm.change_size(10, 10)
                    #

                    if playerDino.isDucking == False:
                        mm.x = round(playerDino.rect.centerx)
                        mm.y = round(playerDino.rect.top * 1.035)
                    if playerDino.isDucking == True:
                        mm.x = round(playerDino.rect.centerx)
                        mm.y = round(playerDino.rect.centery * 1.01)
                    mm.move = 15
                    m_list.append(mm)
                bk = bk + 1
                d_list = []

                for i in range(len(m_list)):
                    m = m_list[i]
                    m.x += m.move
                    if m.x > width:
                        d_list.append(i)

                d_list.reverse()
                for d in d_list:
                    del m_list[d]
                #

                if jumpingx2:
                    if playerDino.rect.bottom == int(height * 0.98):
                        playerDino.isJumping = True
                        playerDino.movement[1] = -1 * playerDino.superJumpSpeed


                # 남현 - 211112 cati(선인장)을 아예 안 나오게 하면 하트 아이템도 안나옴
                # => 아예 안나오게는 못하니 life 를 깎지 않는걸로?
                for c in cacti:
                    c.movement[0] = -1 * gamespeed
                    if not playerDino.collision_immune:
                        if pygame.sprite.collide_mask(playerDino, c):
                            # playerDino.collision_immune = True
                            # life -= 1
                            # collision_time = pygame.time.get_ticks()
                            if life <= 0:
                                playerDino.isDead = True
                            # if pygame.mixer.get_init() is not None:
                            #     die_sound.play()

                    elif not playerDino.isSuper:
                        immune_time = pygame.time.get_ticks()
                        # if immune_time - collision_time > collision_immune_time:
                        #     playerDino.collision_immune = False

                # 211113 보너스 아이템이 등장하지 않으므로 기존 하트 아이템에 보너스 점수 추가
                for l in life_items:
                    l.movement[0] = -1 * gamespeed
                    if pygame.sprite.collide_mask(playerDino, l):
                        if pygame.mixer.get_init() is not None:
                            checkPoint_sound.play()
                        if life < max_life: # 보경
                            life += 1
                        playerDino.score += 10
                        l.kill()
                    elif l.rect.right < 0:
                        l.kill()


                CACTUS_INTERVAL = 50
                
                # 남현 - 211109 구름도 test를 위해 인터벌 변경
                CLOUD_INTERVAL = 11


                OBJECT_REFRESH_LINE = width * 0.8
                MAGIC_NUM = 10


                # 남현 - 211112 cati(선인장)을 아예 안 나오게 하면 하트 아이템도 안나옴

                if len(cacti) < 2:
                    if len(cacti) == 0:
                        last_obstacle.empty()
                        last_obstacle.add(Cactus(gamespeed, object_size[0], object_size[1]))
                    else:
                        for l in last_obstacle:
                            if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(
                                    CACTUS_INTERVAL) == MAGIC_NUM:
                                last_obstacle.empty()
                                last_obstacle.add(Cactus(gamespeed, object_size[0], object_size[1]))


                # 남현 - 211112 구름 등장 조건 수정
                # if len(clouds) < 5 and random.randrange(CLOUD_INTERVAL) == MAGIC_NUM:
                if len(clouds) < 5 and random.randrange(CLOUD_INTERVAL) == MAGIC_NUM:
                    Cloud(width, random.randrange(height / 5, height / 2))

                # 남현 - 211109 life_items 등장조건 수정
                # if len(life_items) == 0 and random.randrange(LIFE_INTERVAL) == MAGIC_NUM and counter > LIFE_INTERVAL * 2:
                if True:
                    for l in last_obstacle:
                        if l.rect.right < OBJECT_REFRESH_LINE:
                            last_obstacle.empty()
                            last_obstacle.add(LifeItem(gamespeed, object_size[0], object_size[1]))



                playerDino.update()
                cacti.update()

                clouds.update()

                life_items.update()
                # 남현 - 211113 보너스 아이템 추가

                new_ground.update()
                scb.update(playerDino.score)
                highsc.update(high_score)
                speed_indicator.update(gamespeed - 3)
                heart.update(life)


                if pygame.display.get_surface() != None:

                    # 남현 - 211104 스테이지에 맞춰 배경색 변경
                    # 남현 - 211109 보너스 스테이지는 기본 배경
                    screen.fill(background_col)

                    new_ground.draw()
                    clouds.draw(screen)
                    scb.draw()
                    speed_indicator.draw()
                    screen.blit(speed_text, (width * 0.01, height * 0.13))

                    # 남현 - 211030 타이머 추가
                    # 타이머 집어 넣기
                    # 경과 시간 계산
                    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
                    # 경과 시간(ms)을 1000으로 나누어서 초(s) 단위로 표시
                    timer = pygame.font.Font(None, 40).render(str(int(total_time - elapsed_time)), True, (0, 0, 0))
                    # # 남현 - 211104 - 스테이지 별 타이머 글씨체 다르게 설정
                    # if (stage == 2):
                    #     timer = pygame.font.Font(None, 40).render(str(int(total_time - elapsed_time)), True,
                    #                                               (255, 255, 255))
                    # 출력할 글자, True, 글자 색상
                    screen.blit(timer, (width * 0.01, height * 0.2))

                    # 남현 - 211031 게임시작 시 스테이지 글자 표시
                    # 남현 - 211104 게임시작 시 스테이지 별 글자 표시하도록 함
                    if elapsed_time <= 3:
                        # 남현 - 211109 보너스 스테이지 시작 시 글자표시
                        stage_info = pygame.font.Font(None, 100).render(str("BONUS STAGE"), True, (0, 0, 0))
                        # 출력할 글자, True, 글자 색상
                        screen.blit(stage_info, (width * 0.20, height * 0.4))

                    heart.draw()
                    if high_score != 0:
                        highsc.draw()
                        screen.blit(HI_image, HI_rect)
                    life_items.draw(screen)


                    # 5. 미사일 배열에 저장된 미사일들을 게임 스크린에 그려줍니다.
                    for m in m_list:
                        m.show()
                        # print(type(mm.x))


                    playerDino.draw()
                    resized_screen.blit(
                        pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                        resized_screen_centerpos)

                    # 남현 - 211030 타이머 추가
                    # 만약 시간이 0 이하이면 게임 종료
                    if total_time - elapsed_time <= 0:
                        print("BONUS STAGE 타임아웃")
                        pygame.time.wait(500)
                        gameplay_hard(stage + 1, life, gamespeed, playerDino.score)

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