from src.dino import *
from src.obstacle import *
from src.item import *
from src.interface import *
from src.gameMode.callGame import *
from db.db_interface import InterfDB
from src.gameState import *

db = InterfDB("db/score.db")


## 시작 화면 ##
def introscreen():
    global resized_screen

    # temp_dino를 전역변수로 설정합니다.
    global temp_dino
    global type_idx
    global dino_type
    dino_type = ['ORIGINAL','RED','ORANGE','YELLOW','GREEN','PURPLE','BLACK','PINK']
    type_idx = 0
    click_count = 0
    #
    temp_dino = Dino(temp_dino_size[0], temp_dino_size[1])
    temp_dino.isBlinking = True
    gameStart = False

    ###이미지 로드###
    # 배경 이미지
    Background, Background_rect = load_image('intro_bg.png', width, height, None)
    # 버튼 이미지
    r_btn_gamestart, r_btn_gamestart_rect = load_image(*resize('btn_start.png', 130, 45, -1))
    btn_gamestart, btn_gamestart_rect = load_image('btn_start.png', 130, 45, -1)
    r_btn_board, r_btn_board_rect = load_image(*resize('btn_board.png', 130, 45, -1))
    btn_board, btn_board_rect = load_image('btn_board.png',130, 45, -1)
    r_btn_option, r_btn_option_rect = load_image(*resize('btn_option.png',130, 45, -1))
    btn_option, btn_option_rect = load_image('btn_option.png',130, 45, -1)
    # DINO IMAGE
    
    btn_gamestart_rect.center = (width * 0.8, height * 0.55)
    btn_board_rect.center = (width * 0.8, height * 0.7)
    btn_option_rect.center = (width * 0.8, height * 0.85)


    while not gameStart:
        if pygame.display.get_surface() == None:
            print("Couldn't load display surface")
            return True
        else:
            for event in pygame.event.get():
                # 이두용이 작성1 시작:
                if event.type == pygame.VIDEORESIZE and not full_screen:
                    # r_btn_gamestart, r_btn_gamestart_rect = load_image(*resize('btn_start.png', 150, 50, -1))
                    # btn_gamestart, btn_gamestart_rect = load_image('btn_start.png', 150, 50, -1)
                    # r_btn_board, r_btn_board_rect = load_image(*resize('btn_board.png', 150, 50, -1))
                    # btn_board, btn_board_rect = load_image('btn_board.png', 150, 50, -1)
                    # r_btn_option, r_btn_option_rect = load_image(*resize('btn_option.png', 150, 50, -1))
                    # btn_option, btn_option_rect = load_image('btn_option.png', 150, 50, -1)

                    ###IMGPOS###
                    #BACKGROUND IMG POS
                    Background_rect.bottomleft = (width*0, height)
                    #이두용이 작성1 끝.

                if event.type == pygame.QUIT:
                    return True

                # 버튼 클릭했을 때 event
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed() == (1, 0, 0):
                        x, y = event.pos
                        #game button
                        if r_btn_gamestart_rect.collidepoint(x, y):
                            temp_dino.isJumping = True
                            temp_dino.isBlinking = False
                            temp_dino.movement[1] = -1 * temp_dino.jumpSpeed

                        #board button
                        if r_btn_board_rect.collidepoint(x, y):
                            gameStart = True
                            introFlag = board()
                            if introFlag == True:
                                introscreen()
                            
                        # option button         
                        if r_btn_option_rect.collidepoint(x, y):
                            gameStart = True
                            option()

                        # temp_dino를 누르는 경우: 
                        if temp_dino.rect.collidepoint(x, y):
                            click_count += 1 
                            type_idx = click_count % len(dino_type)
                            temp_dino = Dino(temp_dino_size[0], temp_dino_size[1],type = dino_type[type_idx])
                            temp_dino.isBlinking = True

        temp_dino.update()

        # interface draw
        if pygame.display.get_surface() != None:

            r_btn_gamestart_rect.centerx, r_btn_board_rect.centerx, r_btn_option_rect.centerx = resized_screen.get_width() * 0.8, resized_screen.get_width() * 0.8, resized_screen.get_width() * 0.8
            r_btn_gamestart_rect.centery, r_btn_board_rect.centery, r_btn_option_rect.centery = resized_screen.get_height() * 0.55, resized_screen.get_height() * 0.7, resized_screen.get_height() * 0.85
            
            screen.blit(Background, Background_rect)
            #disp_intro_buttons(btn_gamestart, btn_board, btn_option)
            screen.blit(btn_gamestart, btn_gamestart_rect)
            screen.blit(btn_board, btn_board_rect)
            screen.blit(btn_option, btn_option_rect)

            temp_dino.draw()
            resized_screen.blit(
                pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())), resized_screen_centerpos)

            pygame.display.update()

        clock.tick(FPS)

        if temp_dino.isJumping == False and temp_dino.isBlinking == False:
            gameStart = True
            selectMode()

    pygame.quit()
    quit()


def option():
    global on_pushtime;
    global off_pushtime
    global bgm_on
    global high_score
    global resized_screen

    btnpush_interval = 500  # ms
    pygame.mixer.music.stop()
    done = False
    db_init = False

    largeText = pygame.font.Font('freesansbold.ttf', 60)
    TextSurf, TextRect = text_objects("[ OPTION ]", largeText)
    btn_bgm_on, btn_bgm_on_rect = load_image('btn_bgm_on.png', 60, 60, -1);
    btn_bgm_off, btn_bgm_off_rect = load_image('btn_bgm_off.png', 60, 60, -1)
    
    r_btn_bgm_on, r_btn_bgm_on_rect = load_image(*resize('btn_bgm_on.png', 60, 60, -1))
    init_btn_image, init_btn_rect = load_image('scorereset.png', 60, 60, -1)
    r_init_btn_image, r_init_btn_rect = load_image(*resize('scorereset.png', 60, 60, -1))
    btn_gamerule, btn_gamerule_rect = load_image('btn_gamerule.png', 60, 60, -1)
    r_btn_gamerule, r_btn_gamerule_rect = load_image(*resize('btn_gamerule.png', 60, 60, -1))
    btn_home, btn_home_rect = load_image('main_button.png', 70, 62, -1)
    r_btn_home, r_btn_home_rect = load_image(*resize('main_button.png', 70, 62, -1))
    btn_credit, btn_credit_rect = load_image('btn_credit.png', 150, 50, -1)
    r_btn_credit, r_btn_credit_rect = load_image(*resize('btn_credit.png', 150, 50, -1))

    TextRect.center = (width * 0.5, height * 0.2)
    btn_bgm_on_rect.center = (width * 0.25, height * 0.5)
    init_btn_rect.center = (width * 0.5, height * 0.5)
    btn_gamerule_rect.center = (width * 0.75, height * 0.5)
    btn_home_rect.center = (width * 0.9, height * 0.15)
    btn_credit_rect.center = (width * 0.9, height * 0.85)

    while not done:
        for event in pygame.event.get():

            # CHANGE SIZE START
            if event.type == pygame.VIDEORESIZE and not full_screen:
                # r_btn_gamestart, r_btn_gamestart_rect = load_image(*resize('btn_start.png', 150, 50, -1))
                # btn_gamestart, btn_gamestart_rect = load_image('btn_start.png', 150, 50, -1)
                # r_btn_board, r_btn_board_rect = load_image(*resize('btn_board.png', 150, 50, -1))
                # btn_board, btn_board_rect = load_image('btn_board.png', 150, 50, -1)
                # r_btn_option, r_btn_option_rect = load_image(*resize('btn_option.png', 150, 50, -1))
                # btn_option, btn_option_rect = load_image('btn_option.png', 150, 50, -1)
                pass
                ###IMGPOS###
                #BACKGROUND IMG POS
                # Background_rect.bottomleft = (width*0, height)
            
            # CHANGE SIZE END

            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed() == (1, 0, 0):
                    x, y = event.pos
                    if r_btn_home_rect.collidepoint(x, y):
                        done = True
                        introscreen()

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
                        db_init = True

                    if r_btn_gamerule_rect.collidepoint(x, y):
                        done = True
                        optionFlag = gamerule()
                        if optionFlag:
                            option()

                    if r_btn_credit_rect.collidepoint(x, y):
                        done = True
                        credit()
                        
            # if event.type == pygame.VIDEORESIZE:
            #     checkscrsize(event.w, event.h)

        r_init_btn_rect.centerx, r_init_btn_rect.centery = resized_screen.get_width() * 0.5, resized_screen.get_height() * 0.5
        r_btn_gamerule_rect.centerx, r_btn_gamerule_rect.centery = resized_screen.get_width() * 0.75, resized_screen.get_height() * 0.5
        r_btn_home_rect.centerx, r_btn_home_rect.centery = resized_screen.get_width() * 0.9, resized_screen.get_height() * 0.15
        r_btn_credit_rect.centerx, r_btn_credit_rect.centery = resized_screen.get_width() * 0.9, resized_screen.get_height() * 0.85

        screen.fill(background_col)
        screen.blit(TextSurf, TextRect)
        screen.blit(init_btn_image, init_btn_rect)
        screen.blit(btn_gamerule, btn_gamerule_rect)
        screen.blit(btn_home, btn_home_rect)
        screen.blit(btn_credit, btn_credit_rect)

        if bgm_on:
            screen.blit(btn_bgm_on, btn_bgm_on_rect)
            r_btn_bgm_on_rect.centerx, r_btn_bgm_on_rect.centery = resized_screen.get_width() * 0.25, resized_screen.get_height() * 0.5
        if not bgm_on:
            screen.blit(btn_bgm_off, btn_bgm_on_rect)
            r_btn_bgm_on_rect.centerx, r_btn_bgm_on_rect.centery = resized_screen.get_width() * 0.25, resized_screen.get_height() * 0.5
        if db_init:
            draw_text("Scoreboard cleared", font, screen, 400, 300, black)

        resized_screen.blit(
            pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())), resized_screen_centerpos)
        pygame.display.update()

        clock.tick(FPS)
    pygame.quit()
    quit()



def selectMode():
    global resized_screen
    gameStart = False
    btnpush_interval = 500

    # 배경 이미지
    Background, Background_rect = load_image('intro_bg.png', width, height, -1)
    # 홈으로 돌아가기
    btn_home_image, btn_home_rect = load_image('main_button.png', 70, 62, -1)
    r_btn_home_image, r_btn_home_rect = load_image(*resize('main_button.png', 70, 62, -1))

    # 버튼 이미지
    # classic button
    btn_classicmode_image, btn_classicmode_rect = load_image('btn_classic.png', 135, 45, -1)
    r_btn_classicmode_image, r_btn_classicmode_rect = load_image(*resize('btn_classic.png', 135, 45, -1))
    # arcade button
    btn_arcademode_image, btn_arcademode_rect = load_image('btn_arcade.png', 135, 45, -1)
    r_btn_arcademode_image, r_btn_arcademode_rect = load_image(*resize('btn_arcade.png', 135, 45, -1))
    # multi button
    btn_multimode_image, btn_multimode_rect = load_image('btn_multi.png', 135, 45, -1)
    r_btn_multimode_image, r_btn_multimode_rect = load_image(*resize('btn_multi.png', 135, 45, -1))

    #버튼 위치
    btn_classicmode_rect.center = (width * 0.3, height * 0.7)
    btn_arcademode_rect.center = (width * 0.5, height * 0.7)
    btn_multimode_rect.center = (width * 0.7, height * 0.7)
    btn_home_rect.center = (width * 0.9, height * 0.15)


    while not gameStart:
        gameReset = False
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                gameStart = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed() == (1, 0, 0):
                    x, y = event.pos

                    if r_btn_home_rect.collidepoint(x, y):
                        gameStart = True
                        introscreen()

                    if r_btn_classicmode_rect.collidepoint(x, y):
                        gameStart = True
                        gameReset = call_game("classic")
                        if gameReset == True:
                            gameStart = True
                            introscreen()

                    if r_btn_arcademode_rect.collidepoint(x, y):
                        gameStart = True
                        gameReset = call_game("arcade")
                        if gameReset == True:
                            gameStart = True
                            introscreen()

                    if r_btn_multimode_rect.collidepoint(x, y):
                        gameStart = True
                        gameReset = call_game("multi")
                        if gameReset == True:
                            gameStart = True
                            introscreen()

        r_btn_classicmode_rect.centerx, r_btn_classicmode_rect.centery = resized_screen.get_width() * 0.3, resized_screen.get_height() * 0.7
        r_btn_arcademode_rect.centerx, r_btn_arcademode_rect.centery = resized_screen.get_width() * 0.5, resized_screen.get_height()*0.7
        r_btn_multimode_rect.centerx, r_btn_multimode_rect.centery = resized_screen.get_width() * 0.7, resized_screen.get_height()*0.7
        r_btn_home_rect.centerx, r_btn_home_rect.centery = resized_screen.get_width() * 0.9, resized_screen.get_height() * 0.15

        screen.blit(Background, Background_rect)
        screen.blit(btn_classicmode_image, btn_classicmode_rect)
        screen.blit(btn_arcademode_image, btn_arcademode_rect)
        screen.blit(btn_multimode_image, btn_multimode_rect)
        screen.blit(btn_home_image, btn_home_rect)


        resized_screen.blit(
            pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
            resized_screen_centerpos)
        pygame.display.update()

        clock.tick(FPS)
    pygame.quit()
    quit()