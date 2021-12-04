import pygame

from src.dino import *
from src.obstacle import *
from src.item import *
from src.interface import *
from src.gameState import *
from db.db_interface import InterfDB

db = InterfDB("db/score.db")


def gameplay_multi(cur_stage, p1_cur_life, p2_cur_life, cur_speed, score, p1, p2):
    ####speed는 통합
    
    global resized_screen
    global players_score 
    global high_score
    global introFlag
    global playerDead

    dino_type = ['ORIGINAL','RED','ORANGE','YELLOW','GREEN','PURPLE','BLACK','PINK']
    result = db.query_db("select score from user order by score desc;", one=True)
    if result is not None:
        high_score = result['score']

    stage = cur_stage

    global gamespeed 
    gamespeed = cur_speed
    players_score = 0
    #작은익룡이랑 보스 총알 맞으면 감속
    #게임을 실행하면 실제 움직이는 initial gamespeed는 4(4~13)이고, 사용자에게는 가장 낮은 speed인 1(1~10)로 인식하는 값임
    def gamespeed_down():
        global gamespeed
        if gamespeed > 4:
            gamespeed -= 1
        
    startMenu = False
    gameOver = False
    gameQuit = False
    introFlag = False

    max_life = 15

    p1_life = p1_cur_life    
    p2_life = p2_cur_life  

    paused = False

    player1 = p1
    player2 = p2
    

    new_ground = Ground(-1 * gamespeed)
    scb = Scoreboard()
    highsc = Scoreboard(width * 0.78)
    p1_heart = HeartIndicator(max_life, p1_life)
    p2_heart = HeartIndicator(max_life, p2_life, player_num = 1)

    #SPEED TEXT(width * 0.75, height * 0.05) 
    #TODO: 숫자 settings로 옮기기
    speed_indicator = Scoreboard(width * 0.88, height * 0.15)
    counter = 0


    #스테이지에 맞춰 SPEED 글씨 색상 변경
    speed_text = font.render("SPEED", True, black)
    if(stage == 2) :
        speed_text = font.render("SPEED", True, white)

    cacti = pygame.sprite.Group()
    fire_cacti = pygame.sprite.Group()
    pteras = pygame.sprite.Group()
    stones = pygame.sprite.Group() 
    clouds = pygame.sprite.Group()
    last_obstacle = pygame.sprite.Group()
    shield_items = pygame.sprite.Group()
    life_items = pygame.sprite.Group()
    slow_items = pygame.sprite.Group()


    Cactus.containers = cacti
    fire_Cactus.containers = fire_cacti
    Ptera.containers = pteras
    Cloud.containers = clouds
    ShieldItem.containers = shield_items
    LifeItem.containers = life_items
    SlowItem.containers = slow_items
    Stone.containers = stones 

    temp_images, temp_rect = load_sprite_sheet('numbers.png', 12, 1, 11, int(15 * 6 / 5), -1)
    HI_image = pygame.Surface((30, int(15 * 6 / 5)))
    HI_rect = HI_image.get_rect()
    HI_image.fill(background_col)
    HI_image.blit(temp_images[10], temp_rect)
    temp_rect.left += temp_rect.width
    HI_image.blit(temp_images[11], temp_rect)
    HI_rect.top = height * 0.05
    HI_rect.left = width * 0.73

    # BUTTON IMG LOAD
    gameover_image, gameover_rect = load_image('game_over.png', 380, 22, -1)

    # 스테이지 다 꺠면 축하메시지 출력
    you_won_image, you_won_rect = load_image('you_won.png', 380, 22, -1)
    you_won = False


    temp_images, temp_rect = load_sprite_sheet('numbers.png', 12, 1, 11, int(15 * 6 / 5), -1)
    HI_image = pygame.Surface((30, int(15 * 6 / 5)))
    HI_rect = HI_image.get_rect()
    
    
    if (stage == 1) or (stage ==0):
        HI_image.fill(background_col)
    elif (stage == 2):
        HI_image.fill(background_col2)
    elif (stage == 3):
        HI_image.fill(background_col3)
    HI_image.blit(temp_images[10], temp_rect)
    temp_rect.left += temp_rect.width
    HI_image.blit(temp_images[11], temp_rect)
    HI_rect.top = height * 0.05
    HI_rect.left = width * 0.73

    isBossKilled = False


    # 1. 미사일 발사.
    p1_space_go=False
    p1_m_list=[]
    p1_bk=0
    
    p2_space_go=False
    p2_m_list=[]
    p2_bk=0

    # 익룡이 격추되었을때
    isDown=False
    boomCount=0
    #

    # 방향키 구현
    p1_goLeft=False
    p1_goRight=False
    
    p2_goLeft=False
    p2_goRight=False
    #

    p1_jumpingx2 = False
    p2_jumpingx2 = False

    # 보스몬스터 변수설정
    isPkingTime=False
    isPkingAlive=True
    pking=PteraKing(cur_stage = stage)
    pm_list = []
    pm_vector = []
    pm_pattern0_count = 0
    pm_pattern1_count = 0

    # 보스 등장 시기를 점수(100점)가 아닌 시간으로
    pking_appearance_time = 10
    #

    # 타이머기능 추가
    start_ticks = pygame.time.get_ticks()  
    

    total_time = 30


    #elapsed_time을 미리 선언+초기화를 안 하면 보스등장조건에서 사용 불가
    elapsed_time = 0    

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
                        #p1
                        if event.key == pygame.K_SPACE or event.key == pygame.K_UP:  # 스페이스 누르는 시점에 공룡이 땅에 닿아있으면 점프한다.
                            if player1.rect.bottom == int(0.98 * height):
                                player1.isJumping = True
                                if pygame.mixer.get_init() != None and player1.isDead == False:
                                    jump_sound.play()
                                player1.movement[1] = -1 * player1.jumpSpeed

                        if event.key == pygame.K_DOWN:  # 아래방향키를 누르는 시점에 공룡이 점프중이지 않으면 숙인다.
                            if not (player1.isJumping and player1.isDead):
                                player1.isDucking = True

                        if event.key == pygame.K_LEFT:
                            p1_goLeft=True

                        if event.key == pygame.K_RIGHT:
                            p1_goRight=True

                        if event.key == pygame.K_SLASH:
                            p1_space_go = True
                            p1_bk = 0

                        if event.key == pygame.K_RSHIFT:
                            p1_jumpingx2=True

                        #p2
                        if event.key == pygame.K_w:
                            # 스페이스 누르는 시점에 공룡이 땅에 닿아있으면 점프한다.
                            if player2.rect.bottom == int(0.98 * height):
                                player2.isJumping = True

                                if pygame.mixer.get_init() != None and player2.isDead == False:
                                    jump_sound.play()
                                player2.movement[1] = -1 * player2.jumpSpeed

                        if event.key == pygame.K_s:
                            # 아래방향키를 누르는 시점에 공룡이 점프중이지 않으면 숙인다.
                            if not (player2.isJumping and player2.isDead):
                                player2.isDucking = True

                        if event.key == pygame.K_a:
                            p2_goLeft = True

                        if event.key == pygame.K_d:
                            p2_goRight = True

                        if event.key == pygame.K_LCTRL:
                            p2_space_go = True
                            p2_bk = 0
      
                        if event.key == pygame.K_LSHIFT:
                            p2_jumpingx2=True

                        if event.key == pygame.K_ESCAPE:
                            paused = not paused
                            pause_value, return_home_value = pausing()
                            if pause_value != None:
                                paused = pause_value
                            else:
                                introFlag = return_home_value
                                gameQuit = True
                                return introFlag

                    if event.type == pygame.KEYUP:
                        #p1
                        if event.key == pygame.K_DOWN:
                            player1.isDucking = False

                        # 키에서 손을 떼면, 미사일이 발사 되지 않습니다.
                        if event.key == pygame.K_SLASH:
                            p1_space_go = False

                        # 방향키 추가
                        if event.key == pygame.K_LEFT:
                            p1_goLeft=False

                        if event.key == pygame.K_RIGHT:
                            p1_goRight=False
                        
                        #p2
                        if event.key == pygame.K_s:
                            player2.isDucking = False

                        # 키에서 손을 떼면, 미사일이 발사 되지 않습니다.
                        if event.key == pygame.K_LCTRL:
                            p2_space_go = False

                        # 방향키 추가
                        if event.key == pygame.K_a:
                            p2_goLeft=False

                        if event.key == pygame.K_d:
                            p2_goRight=False
                        
                        if event.key == pygame.K_LSHIFT:
                            p2_jumpingx2 = False
                        if event.key == pygame.K_RSHIFT:
                            p1_jumpingx2 = False


                    if event.type == pygame.VIDEORESIZE:
                        checkscrsize(event.w, event.h)

            if not paused:

                # 방향키 추가 (현재 여기 근데 수정더):
                if p1_goLeft:
                    player1.rect.left= player1.rect.left -(gamespeed)

                if p1_goRight:
                    player1.rect.left = player1.rect.left + gamespeed
                
                if p2_goLeft:
                    player2.rect.left= player2.rect.left -(gamespeed)

                if p2_goRight:
                    player2.rect.left = player2.rect.left + gamespeed

                # 4. space_go가 True이고, 일정 시간이 지나면, 미사일을 만들고, 이를 미사일 배열에 넣습니다.
                # p1
                if (p1_space_go==True) and (int(p1_bk%15)==0):
                    p1_mm=obj()

                    # 디노의 종류에 따라 다른 총알이 나가도록 합니다.
                    if player1.type == 'RED':
                        p1_mm.put_img("./sprites/black_bullet.png")
                        p1_mm.change_size(10,10)
                    elif player1.type == 'YELLOW':
                        p1_mm.put_img("./sprites/blue_bullet.png")
                        p1_mm.change_size(10,10)
                    elif player1.type == 'ORANGE':
                        p1_mm.put_img("./sprites/blue_bullet.png")
                        p1_mm.change_size(10,10)
                    elif player1.type == 'PURPLE':
                        p1_mm.put_img("./sprites/pink_bullet.png")
                        p1_mm.change_size(15,5)
                    elif player1.type == 'PINK':
                        p1_mm.put_img("./sprites/heart_bullet.png")
                        p1_mm.change_size(10,10)
                    else:                    
                        p1_mm.put_img("./sprites/red_bullet.png")
                        p1_mm.change_size(10,10)
                    
                    if player1.isDucking ==False:
                        p1_mm.x = round(player1.rect.centerx)
                        p1_mm.y = round(player1.rect.top*1.035)

                    if player1.isDucking ==True:
                        p1_mm.x = round(player1.rect.centerx)
                        p1_mm.y = round(player1.rect.centery*1.01)
                    p1_mm.move = 15
                    p1_m_list.append(p1_mm)

                p1_bk = p1_bk+1
                p1_d_list=[]
                for i in range(len(p1_m_list)):
                    p1_m = p1_m_list[i]
                    p1_m.x += p1_m.move
                    if p1_m.x>width:
                        p1_d_list.append(i)

                p1_d_list.reverse()
                for d in p1_d_list:
                     del p1_m_list[d]
                
                if p1_jumpingx2:
                    if player1.rect.bottom == int(height * 0.98):
                        player1.isJumping = True
                        player1.movement[1] = -1 * player1.superJumpSpeed


                #p2
                if (p2_space_go==True) and (int(p2_bk%15)==0):
                    # print(bk)
                    p2_mm=obj()

                    # 디노의 종류에 따라 다른 총알이 나가도록 합니다.
                    if player2.type == 'RED':
                        p2_mm.put_img("./sprites/black_bullet.png")
                        p2_mm.change_size(10,10)
                    elif player2.type == 'YELLOW':
                        p2_mm.put_img("./sprites/blue_bullet.png")
                        p2_mm.change_size(10,10)
                    elif player2.type == 'ORANGE':
                        p2_mm.put_img("./sprites/blue_bullet.png")
                        p2_mm.change_size(10,10)
                    elif player2.type == 'PURPLE':
                        p2_mm.put_img("./sprites/pink_bullet.png")
                        p2_mm.change_size(15,5)
                    elif player2.type == 'PINK':
                        p2_mm.put_img("./sprites/heart_bullet.png")
                        p2_mm.change_size(10,10)
                    else:                    
                        p2_mm.put_img("./sprites/red_bullet.png")
                        p2_mm.change_size(10,10)
                    # 
                    
                    if player2.isDucking ==False:
                        p2_mm.x = round(player2.rect.centerx)
                        p2_mm.y = round(player2.rect.top*1.035)

                    if player2.isDucking ==True:
                        p2_mm.x = round(player2.rect.centerx)
                        p2_mm.y = round(player2.rect.centery*1.01)
                    p2_mm.move = 15
                    p2_m_list.append(p2_mm)

                p2_bk = p2_bk+1
                p2_d_list=[]

                for i in range(len(p2_m_list)):
                    p2_m=p2_m_list[i]
                    p2_m.x +=p2_m.move
                    if p2_m.x>width:
                        p2_d_list.append(i)

                p2_d_list.reverse()
                # for d in p2_d_list:
                #     del p2_m_list[d]

                # 보스 몬스터 패턴0(위에서 가만히 있는 패턴): 보스 익룡이 쏘는 미사일.
                if (isPkingTime) and (pking.pattern_idx == 0) and (int(pm_pattern0_count % 20) == 0):
                    pm=obj()
                    pm.put_img("./sprites/pking bullet.png")
                    pm.change_size(15,15)
                    pm.x = round(pking.rect.centerx)
                    pm.y = round(pking.rect.centery)
                    pm.xmove = random.randint(0,15)
                    pm.ymove = random.randint(1,3)

                    pm_list.append(pm)
                pm_pattern0_count += 1
                pd_list = []

                for i in range(len(pm_list)):
                    pm = pm_list[i]
                    pm.x -= pm.xmove
                    pm.y += pm.ymove
                    if pm.y > height or pm.x < 0:
                        pd_list.append(i)
                pd_list.reverse()
                for d in pd_list:
                    del pm_list[d]

                if p2_jumpingx2:
                    if player2.rect.bottom == int(height * 0.98):
                        player2.isJumping = True
                        player2.movement[1] = -1 * player2.superJumpSpeed

                # 보스 몬스터 패턴1(좌우로 왔다갔다 하는 패턴): 보스 익룡이 쏘는 미사일.
                if (isPkingTime) and (pking.pattern_idx == 1) and (int(pm_pattern1_count % 20) == 0):
                    pm=obj()
                    pm.put_img("./sprites/pking bullet.png")
                    pm.change_size(15,15)
                    pm.x = round(pking.rect.centerx)
                    pm.y = round(pking.rect.centery)
                    pm.move = 3
                    pm_list.append(pm)
                pm_pattern1_count += 1
                pd_list = []

                for i in range(len(pm_list)):
                    pm=pm_list[i]
                    pm.y +=pm.move
                    if pm.y>height or pm.x < 0:
                        pd_list.append(i)

                pd_list.reverse()
                for d in pd_list:
                    del pm_list[d]
                #
                global p1_collision_time
                global p2_collision_time
                global item_time

                for c in cacti:
                    c.movement[0] = -1 * gamespeed
                    #p1
                    if not player1.collision_immune:
                        if pygame.sprite.collide_mask(player1, c):
                            player1.collision_immune = True
                            p1_life -= 1
                            p1_collision_time = pygame.time.get_ticks()
                            if p1_life <= 0:
                                player1.isDead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()
                    elif not player1.isSuper:
                        p1_immune_time = pygame.time.get_ticks()
                        if p1_immune_time - p1_collision_time > collision_immune_time:
                            player1.collision_immune = False
                    #p2
                    if not player2.collision_immune:
                        if pygame.sprite.collide_mask(player2, c):
                            player2.collision_immune = True
                            p2_life -= 1
                            p2_collision_time = pygame.time.get_ticks()
                            if p2_life <= 0:
                                player2.isDead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()
                    elif not player2.isSuper:
                        p2_immune_time = pygame.time.get_ticks()
                        if p2_immune_time - p2_collision_time > collision_immune_time:
                            player2.collision_immune = False


                for f in fire_cacti:
                    f.movement[0] = -1 * gamespeed
                    #p1
                    if not player1.collision_immune:
                        if pygame.sprite.collide_mask(player1, f):
                            player1.collision_immune = True
                            p1_life -= 1
                            p1_collision_time = pygame.time.get_ticks()
                            if p1_life <= 0:
                                player1.isDead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()
                    elif not player1.isSuper:
                        p1_immune_time = pygame.time.get_ticks()
                        if p1_immune_time - p1_collision_time > collision_immune_time:
                            player1.collision_immune = False
                    #p2
                    if not player2.collision_immune:
                        if pygame.sprite.collide_mask(player2, f):
                            player2.collision_immune = True
                            p2_life -= 1
                            p2_collision_time = pygame.time.get_ticks()
                            if p2_life <= 0:
                                player2.isDead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()
                    elif not player2.isSuper:
                        p2_immune_time = pygame.time.get_ticks()
                        if p2_immune_time - p2_collision_time > collision_immune_time:
                            player2.collision_immune = False

                for p in pteras:
                    p.movement[0] = -1 * gamespeed

                    # 7. 익룡이 미사일에 맞으면 익룡과 미사일 모두 사라집니다.

                    if (len(p1_m_list)==0 and len(p2_m_list)==0):
                        pass
                    else:
                        #p1
                        ptera_hit = False
                        
                        if len(p1_m_list)!= 0:
                            if (p1_m.x>=p.rect.left)and(p1_m.x<=p.rect.right)and(p1_m.y>p.rect.top)and(p1_m.y<p.rect.bottom):
                                ptera_hit = True
                                p1_m_list.remove(p1_m)
                        #p2
                        if len(p2_m_list)!= 0:
                            if (p2_m.x>=p.rect.left)and(p2_m.x<=p.rect.right)and(p2_m.y>p.rect.top)and(p2_m.y<p.rect.bottom):
                                ptera_hit = True
                                p2_m_list.remove(p2_m)


                        if ptera_hit == True:
                            print("격추 성공")
                            isDown=True
                            boom=obj()
                            boom.put_img("./sprites/boom.png")
                            boom.change_size(200,100)
                            boom.x=p.rect.centerx-round(p.rect.width)*2.5
                            boom.y=p.rect.centery-round(p.rect.height)*1.5
                            player1.score += 30 #임의로 1플레이어에게 배당
                            p.kill()

                    
                    #p1
                    if not player1.collision_immune:
                        if pygame.sprite.collide_mask(player1, p):
                            player1.collision_immune = True
                            p1_life -= 1
                            gamespeed_down()
                            p1_collision_time = pygame.time.get_ticks()
                            if p1_life <= 0:
                                player1.isDead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                    elif not player1.isSuper:
                        p1_immune_time = pygame.time.get_ticks()
                        if p1_immune_time - p1_collision_time > collision_immune_time:
                            player1.collision_immune = False
                    #p2
                    if not player2.collision_immune:
                        if pygame.sprite.collide_mask(player2, p):
                            player2.collision_immune = True
                            p2_life -= 1
                            gamespeed_down()
                            p2_collision_time = pygame.time.get_ticks()
                            if p2_life <= 0:
                                player2.isDead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                    elif not player2.isSuper:
                        p2_immune_time = pygame.time.get_ticks()
                        if p2_immune_time - p2_collision_time > collision_immune_time:
                            player2.collision_immune = False

                for s in stones:
                    s.movement[0] = -1 * gamespeed
                    #p1
                    if not player1.collision_immune:
                        if pygame.sprite.collide_mask(player1, s):
                            player1.collision_immune = True
                            p1_life -= 1
                            p1_collision_time = pygame.time.get_ticks()
                            if p1_life <= 0:
                                player1.isDead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()
                    #p2
                    if not player2.collision_immune:
                        if pygame.sprite.collide_mask(player2, s):
                            player2.collision_immune = True
                            p2_life -= 1
                            p2_collision_time = pygame.time.get_ticks()
                            if p2_life <= 0:
                                player2.isDead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()
                #p1
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
                else:
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

                    if pygame.time.get_ticks() - item_time > shield_time:
                        player1.collision_immune = False
                        player1.isSuper = False

                for l in life_items:
                    l.movement[0] = -1 * gamespeed
                    if pygame.sprite.collide_mask(player1, l):
                        if pygame.mixer.get_init() is not None:
                            checkPoint_sound.play()
                        if p1_life < max_life:
                            p1_life += 1
                        l.kill()
                    elif l.rect.right < 0:
                        l.kill()

                for k in slow_items:
                    k.movement[0] = -1 * gamespeed
                    if pygame.sprite.collide_mask(player1, k):
                        if pygame.mixer.get_init() is not None:
                            checkPoint_sound.play()
                        gamespeed_down()
                        new_ground.speed += 1

                        k.kill()
                    elif k.rect.right < 0:
                        k.kill()
                #p2
                if not player2.isSuper:
                    for s in shield_items:
                        s.movement[0] = -1 * gamespeed
                        if pygame.sprite.collide_mask(player2, s):
                            if pygame.mixer.get_init() is not None:
                                checkPoint_sound.play()
                            player2.collision_immune = True
                            player2.isSuper = True
                            s.kill()
                            item_time = pygame.time.get_ticks()
                        elif s.rect.right < 0:
                            s.kill()
                else:
                    for s in shield_items:
                        s.movement[0] = -1 * gamespeed
                        if pygame.sprite.collide_mask(player2, s):
                            if pygame.mixer.get_init() is not None:
                                checkPoint_sound.play()
                            player2.collision_immune = True
                            player2.isSuper = True
                            s.kill()
                            item_time = pygame.time.get_ticks()
                        elif s.rect.right < 0:
                            s.kill()

                    if pygame.time.get_ticks() - item_time > shield_time:
                        player2.collision_immune = False
                        player2.isSuper = False

                for l in life_items:
                    l.movement[0] = -1 * gamespeed
                    if pygame.sprite.collide_mask(player2, l):
                        if pygame.mixer.get_init() is not None:
                            checkPoint_sound.play()
                        if p2_life < max_life:
                            p2_life += 1
                        l.kill()
                    elif l.rect.right < 0:
                        l.kill()

                for k in slow_items:
                    k.movement[0] = -1 * gamespeed
                    if pygame.sprite.collide_mask(player2, k):
                        if pygame.mixer.get_init() is not None:
                            checkPoint_sound.play()
                        gamespeed_down()
                        new_ground.speed += 1
                        k.kill()
                    elif k.rect.right < 0:
                        k.kill()
                

                ###removed all items

                STONE_INTERVAL = 100
                CACTUS_INTERVAL = 50
                PTERA_INTERVAL = 12
                CLOUD_INTERVAL = 300
                SHIELD_INTERVAL = 50
                LIFE_INTERVAL = 50
                SLOW_INTERVAL = 50

                OBJECT_REFRESH_LINE = width * 0.8
                MAGIC_NUM = 10

                # 보스 등장 조건: 경과된시간>보스등장시간
                if (isPkingAlive) and (elapsed_time > pking_appearance_time):
                    isPkingTime=True
                else:
                    isPkingTime = False

                if isPkingTime:
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
                            if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(CACTUS_INTERVAL*5) == MAGIC_NUM:
                                last_obstacle.empty()
                                last_obstacle.add(fire_Cactus(gamespeed, object_size[0], object_size[1]))

                    if len(clouds) < 5 and random.randrange(CLOUD_INTERVAL) == MAGIC_NUM:
                        Cloud(width, random.randrange(height / 5, height / 2))

                    if (len(p1_m_list)==0 and len(p2_m_list)==0):
                        pass
                    else:
                        Ptera_king_hit = False
                        if len(p1_m_list) != 0:
                            if (p1_m.x>=pking.rect.left)and(p1_m.x<=pking.rect.right)and(p1_m.y>pking.rect.top)and(p1_m.y<pking.rect.bottom):
                                p1_m_list.remove(p1_mm)
                                Ptera_king_hit = True
                        if len(p2_m_list)!=0:
                            if (p2_m.x>=pking.rect.left)and(p2_m.x<=pking.rect.right)and(p2_m.y>pking.rect.top)and(p2_m.y<pking.rect.bottom):
                                p2_m_list.remove(p2_mm)
                                Ptera_king_hit = True

                        if Ptera_king_hit == True:
                            isDown=True
                            boom=obj()
                            boom.put_img("./sprites/boom.png")
                            boom.change_size(200,100)
                            boom.x=pking.rect.centerx-round(pking.rect.width)
                            boom.y=pking.rect.centery-round(pking.rect.height/2)
                            player1.score += 100
                            pking.get_damage(1)

                            if pking.current_health == 0:
                                pking.kill()
                                isPkingAlive=False
                                isBossKilled = True
                        else:
                            pass


                    #
                    pm_bullet_dissolve = False
                    if (len(pm_list)==0):
                        pass
                    else:
                        for pm in pm_list:
                            #p1
                            if (pm.x>=player1.rect.left)and(pm.x<=player1.rect.right)and(pm.y>player1.rect.top)and(pm.y<player1.rect.bottom):
                                print("공격에 맞음.")
                                player1.collision_immune = True
                                p1_life -= 2
                                gamespeed_down()
                                
                                die_sound.play()
                                p1_collision_time = pygame.time.get_ticks()
                                if p1_life <= 0:
                                    player1.isDead = True
                                pm_bullet_dissolve = True
                                
                            #p2
                            if (pm.x>=player2.rect.left)and(pm.x<=player2.rect.right)and(pm.y>player2.rect.top)and(pm.y<player2.rect.bottom):
                                print("공격에 맞음.")
                                player2.collision_immune = True
                                p2_life -= 2
                                gamespeed_down()
                                
                                die_sound.play()
                                p2_collision_time = pygame.time.get_ticks()
                                if p2_life <= 0:
                                    player2.isDead = True
                                pm_bullet_dissolve = True
                            
                            if pm_bullet_dissolve == True:    
                                pm_list.remove(pm)
                else:
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
                            if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(STONE_INTERVAL * 5) == MAGIC_NUM:
                                last_obstacle.empty()
                                last_obstacle.add(Stone(gamespeed, object_size[0], object_size[1]))


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

                if (player1.isDead == True) and (player2.isDead == False) :
                    player2.update()
                    player1.rect.left = player1.rect.left - resized_screen.get_width()
                elif (player1.isDead == False) and (player2.isDead == True) :
                    player1.update()
                    player2.rect.left = player1.rect.left - resized_screen.get_width()
                else :
                    player1.update()
                    player2.update()


                cacti.update()
                fire_cacti.update()
                stones.update()
                pteras.update()
                clouds.update()
                shield_items.update()
                life_items.update()

                new_ground.update()
                players_score = int((player1.score + player2.score)/2) + score
                scb.update(players_score, stage)
                highsc.update(high_score, stage)
                speed_indicator.update(gamespeed - 3, stage)

                p1_heart.update(p1_life)
                p2_heart.update(p2_life)
                slow_items.update()

                if isPkingTime:
                    pking.update()
                #

                if pygame.display.get_surface() != None:
                    
                    if(stage == 1):
                        screen.fill(background_col)
                    elif(stage == 2):
                        screen.fill(background_col2)
                    elif(stage == 3):
                        screen.fill(background_col3)
                    new_ground.draw()
                    clouds.draw(screen)
                    scb.draw()
                    speed_indicator.draw()
                    screen.blit(speed_text, (width * 0.75, height * 0.13))

                    # 경과 시간 계산
                    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
                    # 경과 시간(ms)을 1000으로 나누어서 초(s) 단위로 표시
                    timer = pygame.font.Font(None, 40).render(str(int(total_time - elapsed_time)), True, (0, 0, 0))
                    # 스테이지 별 타이머 글씨체 다르게 설정
                    if(stage == 2):
                        timer = pygame.font.Font(None, 40).render(str(int(total_time - elapsed_time)), True, (255, 255, 255))
                    # 출력할 글자, True, 글자 색상
                    screen.blit(timer, (width * 0.01, height * 0.2))

                    # 게임시작 시 스테이지별 글자 표시

                    if elapsed_time <= 3:
                        if (stage == 1):
                            stage_info = pygame.font.Font(None, 120).render(str("STAGE 1"), True, (0, 0, 0))
                            # 출력할 글자, True, 글자 색상
                            screen.blit(stage_info, (width * 0.275, height * 0.4))
                        elif (stage == 2):
                            stage_info = pygame.font.Font(None, 120).render(str("STAGE 2"), True, (255, 255, 255))
                            # 출력할 글자, True, 글자 색상
                            screen.blit(stage_info, (width * 0.275, height * 0.4))
                        elif (stage == 3):
                            stage_info = pygame.font.Font(None, 120).render(str("STAGE 3"), True, (0, 0, 0))
                            # 출력할 글자, True, 글자 색상
                            screen.blit(stage_info, (width * 0.275, height * 0.4))



                    p1_heart.draw()
                    p2_heart.draw()
                    if high_score != 0:
                        highsc.draw()
                        screen.blit(HI_image, HI_rect)
                    cacti.draw(screen)
                    fire_cacti.draw(screen)
                    stones.draw(screen)
                    pteras.draw(screen)
                    shield_items.draw(screen)
                    life_items.draw(screen)
                    slow_items.draw(screen)

                    # pkingtime이면, 보스몬스터를 보여줘라.
                    if isPkingTime:
                        pking.draw()
                        pking.bos_health()

                        # 보스 익룡이 쏘는 미사일을 보여준다.
                        for pm in pm_list:
                            pm.show()
                    #

                    # 5. 미사일 배열에 저장된 미사일들을 게임 스크린에 그려줍니다.
                    for p1_m in p1_m_list:
                        p1_m.show()

                    for p2_m in p2_m_list:
                        p2_m.show()

                    if isDown :
                        boom.show()
                        boomCount+=1
                        # boomCount가 5가 될 때까지 boom이미지를 계속 보여준다.
                        if boomCount>10:
                            boomCount=0
                            isDown=False
                    #
                    player1.draw()
                    player2.draw()

                    resized_screen.blit(
                        pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                        resized_screen_centerpos)

                    # 만약 시간이 0 이하이면 게임 종료
                    if total_time - elapsed_time <= 0:
                        print("타임아웃")
                        
                        # 보스를 죽였을때만 다음 스테이지로 넘어가도록
                        if isBossKilled == False :
                            gameOver = True
                        else: 
                            if (stage == 1 or stage == 2):
                                pygame.time.wait(500)
                                gameplay_multi(stage + 1, p1_life, p2_life, gamespeed, players_score, player1, player2)


                            elif (stage == 3):
                                print("모든 스테이지 클리어")
                                pygame.time.wait(500)
                                
                                # 그냥 게임오버가 아니라 스테이지를 다 깬거면 you_won = True로
                                you_won = True

                                gameOver = True

                    pygame.display.update()
                clock.tick(FPS)



                if player1.isDead and player2.isDead:
                    gameOver = True
                    pygame.mixer.music.stop()  # 죽으면 배경음악 멈춤

                if counter % speed_up_limit_count == speed_up_limit_count - 1:

                    new_ground.speed -= 1
                    if gamespeed < 13:
                        gamespeed += 1
                    checkPoint_sound.play()

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
                            name = typescore(players_score)
                            if not db.is_limit_data(players_score):
                                db.query_db(
                                    f"insert into user(username, score) values ('{name}', '{players_score}');")
                                db.commit()
                                introFlag = board()
                                gameQuit = True
                            else:
                                introFlag = board()
                                gameQuit = True

                    if event.type == pygame.VIDEORESIZE:
                        checkscrsize(event.w, event.h)

            highsc.update(high_score)

            resized_screen.blit(
                pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                resized_screen_centerpos)
            pygame.display.update()
            clock.tick(FPS)
    return introFlag
    pygame.quit()
    quit()
