from src.setting import *
from db.db_interface import InterfDB

db = InterfDB("db/score.db")

def board():
    global resized_screen
    gameQuit = False
    scroll_y=0
    # 10
    max_per_screen = 10
    results = db.query_db("select username, score from user order by score desc;")
    screen_board_height = resized_screen.get_height()+(len(results)//max_per_screen)*resized_screen.get_height()
    screen_board = pygame.surface.Surface((
        resized_screen.get_width(),
        screen_board_height
        ))

    title_image, title_rect = load_image("ranking.png", 360, 75, -1)
    title_rect.centerx = width * 0.5
    title_rect.centery = height * 0.2

    while not gameQuit:
        introFlag = False
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
                screen_board.blit(txt_surface, (width*0.4, height * (0.55 + 0.1 * i)))
                screen_board.blit(score_surface, (width * 0.6, height * (0.55 + 0.1 * i)))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameQuit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        gameQuit = True
                        introFlag = True
                    if event.key == pygame.K_UP: scroll_y = min(scroll_y + 15, 0)
                    if event.key == pygame.K_DOWN: scroll_y = max(scroll_y - 15, -(len(results)//max_per_screen)*scr_size[1])
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4: scroll_y = min(scroll_y + 15, 0)
                    if event.button == 5: scroll_y = max(scroll_y - 15, -(len(results)//max_per_screen)*scr_size[1])
                    if event.button == 1:
                        gameQuit = True
                        introFlag = True
                if event.type == pygame.VIDEORESIZE:
                    checkscrsize(event.w, event.h)

            screen.blit(screen_board, (0, scroll_y))
            resized_screen.blit(
                pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())), resized_screen_centerpos)
            pygame.display.update()
        clock.tick(FPS)
    return introFlag
    pygame.quit()
    quit()

# 남현 - 211126 gamerule함수의 파라미터를 조정해 재귀호출 형식으로 튜토리얼 페이지 추가
def gamerule(page = 1):
    global resized_screen
    gameQuit = False
    max_per_screen = 10
    screen_board_height = resized_screen.get_height()
    screen_board = pygame.surface.Surface((
        resized_screen.get_width(),
        screen_board_height
        ))

    # 남현 - 211124 튜토리얼 이미지 변경
    # gamerule_image, gamerule_rect= load_image("gamerule.png",800,300,-1)
    gamerule_image, gamerule_rect = load_image("Tutorial_ppt.png", 800, 400, -1)
    if(page == 2) :
        gamerule_image, gamerule_rect = load_image("Tutorial_ppt_2.png", 800, 400, -1)
    
    # 남현 - 211126 튜토리얼 넘어가는 버튼 추가
    r_btn_nexttutorial, r_btn_nexttutorial_rect = load_image(*resize('next_button.png', 50, 50, -1))
    r_btn_nexttutorial_rect.center = (width * 0.95, height * 0.9)

    gamerule_rect.centerx=width*0.5
    gamerule_rect.centery=height*0.5

    while not gameQuit:
        if pygame.display.get_surface() is None:
            gameQuit = True
        else:
            screen_board.fill(background_col)
            screen_board.blit(gamerule_image,gamerule_rect)

            # 남현 - 211126 버튼 추가
            screen_board.blit(r_btn_nexttutorial, r_btn_nexttutorial_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameQuit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        gameQuit = True
                        return True
                if event.type == pygame.MOUSEBUTTONDOWN:

                    if pygame.mouse.get_pressed() == (1, 0, 0):
                        x, y = event.pos
                        if r_btn_nexttutorial_rect.collidepoint(x, y):
                            if (page == 1):
                                gamerule(2)
                            else:
                                return True

                    if event.button == 1:
                        gameQuit = True
                        return True
                if event.type == pygame.VIDEORESIZE:
                    checkscrsize(event.w, event.h)


            screen.blit(screen_board, (0,0))
            resized_screen.blit(
                pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())), resized_screen_centerpos)



            pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()

def pausing():
    global resized_screen
    introFlag = False
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
                        #첫번째 return 값은 pause상태, 두번째는 introFlag
                        return False, introFlag

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed() == (1, 0, 0):
                        x, y = event.pos
                        if resized_retbutton_rect.collidepoint(x, y):
                            introFlag = True
                            gameQuit = True
                            return None, introFlag

                        if resized_resume_rect.collidepoint(x, y):
                            pygame.mixer.music.unpause()  # pausing상태에서 오른쪽의 아이콘 클릭하면 배경음악 일시정지 해제
                            return False, introFlag

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
                introFlag = True
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
    
    return gamername

def credit():
    global resized_screen
    done = False

    # 남현 - 211127 credit 이미지 수정
    creditimg, creditimg_rect = load_image('credit_T-Rex_Breeder.png', width, height, -1)


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