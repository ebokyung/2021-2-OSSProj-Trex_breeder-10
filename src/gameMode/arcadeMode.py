
from src.dino import *
from src.obstacle import *
from src.item import *
from src.interface import *
from src.gameState import *
from db.db_interface import InterfDB

db = InterfDB("db/score.db")

def gameplay_hard(cur_stage, cur_life, cur_speed, cur_score, player):

    global resized_screen
    global high_score
    global introFlag
    result = db.query_db("select score from user order by score desc;", one=True)
    if result is not None:
        high_score = result['score']

    stage = cur_stage

    #작은익룡이랑 보스 총알 맞으면 감속
    #게임을 실행하면 실제 움직이는 initial gamespeed는 4(4~13)이고, 사용자에게는 가장 낮은 speed인 1(1~10)로 인식하는 값임
    global gamespeed 
    gamespeed = cur_speed
    def gamespeed_down():
        global gamespeed
        if gamespeed > 4:
            gamespeed -= 1

    startMenu = False
    gameOver = False
    gameQuit = False
    introFlag = False

    max_life = 15
    life = cur_life    

    paused = False


    
    # 디노 타입 때문에 변경된 부분
    playerDino = player
    # 
    playerDino.score = cur_score

    new_ground = Ground(-1 * gamespeed)
    scb = Scoreboard()
    highsc = Scoreboard(width * 0.78)
    heart = HeartIndicator(max_life, life)
    speed_indicator = Scoreboard(width * 0.12, height * 0.15)
    counter = 0

    speed_text = font.render("SPEED", True, black)
    if(stage == 2) :
        speed_text = font.render("SPEED", True, white)

    cacti = pygame.sprite.Group()
    fire_cacti = pygame.sprite.Group()
    pteras = pygame.sprite.Group()
    stones = pygame.sprite.Group() #add stones
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
    Stone.containers = stones # add stone containers

    # BUTTON IMG LOAD
    # retbutton_image, retbutton_rect = load_image('replay_button.png', 70, 62, -1)
    gameover_image, gameover_rect = load_image('game_over.png', 380, 22, -1)

    # 스테이지 다 꺠면 축하메시지 출력
    you_won_image, you_won_rect = load_image('you_won.png', 380, 22, -1)
    # 깼는지 안깼는지 확인
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

    # 보스를 죽였는지 아닌지 판단하는 변수
    isBossKilled = False


    # 1. 미사일 발사.
    space_go=False
    m_list=[]
    bk=0
    # 익룡이 격추되었을때
    isDown=False
    boomCount=0
    #

    # 방향키 구현
    goLeft=False
    goRight=False
    #

    # 보스몬스터 변수설정
    isPkingTime=False
    isPkingAlive=True
    pking=PteraKing(cur_stage = stage)
    pm_list = []
    pm_vector = []
    pm_pattern0_count = 0
    pm_pattern1_count = 0

    pking_appearance_time = 20

    #
    jumpingx2 = False

    start_ticks = pygame.time.get_ticks()  # 현재 tick 을 받아옴
    if (stage == 0):
        total_time = 3
    else:
        total_time = 50
    elapsed_time = 0    #elapsed_time을 미리 선언+초기화를 안 하면 보스등장조건에서 사용 불가

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
                            goLeft=True

                        if event.key == pygame.K_RIGHT:
                            # print("right")
                            goRight=True

                        if event.key == pygame.K_ESCAPE:
                            paused = not paused
                            pause_value, return_home_value = pausing()
                            if pause_value != None:
                                paused = pause_value
                            else:
                                introFlag = return_home_value
                                gameQuit = True
                                return introFlag

                        # jumping x2 ( press key s)
                        if event.key == pygame.K_s:
                            jumpingx2=True

                        # 2. a키를 누르면, 미사일이 나갑니다.
                        if event.key == pygame.K_a:
                            space_go=True
                            bk=0
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
                            goLeft=False

                        if event.key == pygame.K_RIGHT:
                            goRight=False
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
                if (space_go==True) and (int(bk%15)==0):
                    # print(bk)
                    mm=obj()

                    # 디노의 종류에 따라 다른 총알이 나가도록 합니다.
                    if playerDino.type == 'RED':
                        mm.put_img("./sprites/black_bullet.png")
                        mm.change_size(10,10)
                    elif playerDino.type == 'YELLOW':
                        mm.put_img("./sprites/blue_bullet.png")
                        mm.change_size(10,10)
                    elif playerDino.type == 'ORANGE':
                        mm.put_img("./sprites/blue_bullet.png")
                        mm.change_size(10,10)
                    elif playerDino.type == 'PURPLE':
                        mm.put_img("./sprites/pink_bullet.png")
                        mm.change_size(15,5)
                    elif playerDino.type == 'PINK':
                        mm.put_img("./sprites/heart_bullet.png")
                        mm.change_size(10,10)
                    else:                    
                        mm.put_img("./sprites/red_bullet.png")
                        mm.change_size(10,10)
                    # 
                    
                    if playerDino.isDucking ==False:
                        mm.x = round(playerDino.rect.centerx)
                        mm.y = round(playerDino.rect.top*1.035)
                    if playerDino.isDucking ==True:
                        mm.x = round(playerDino.rect.centerx)
                        mm.y = round(playerDino.rect.centery*1.01)
                    mm.move = 15
                    m_list.append(mm)
                bk=bk+1
                d_list=[]

                for i in range(len(m_list)):
                    m=m_list[i]
                    m.x +=m.move
                    if m.x>width:
                        d_list.append(i)

                d_list.reverse()
                for d in d_list:
                    del m_list[d]
                #

                if jumpingx2 :
                    if  playerDino.rect.bottom == int(height * 0.98):
                        playerDino.isJumping = True
                        playerDino.movement[1] = -1 * playerDino.superJumpSpeed

                # 보스 총알쏘는 패턴0(위에서 가만히 있을때): 보스 익룡이 쏘는 미사일(pm)
                # 패턴0일때 미사일 쏘는 주기
                if (stage == 1):
                    cycle0 = 75
                elif(stage ==2):
                    cycle0 = 20
                elif (stage ==3):
                    cycle0 = 15

                if (isPkingTime) and (pking.pattern_idx == 0) and (int(pm_pattern0_count % cycle0) == 0):
                    pm=obj()
                    pm.put_img("./sprites/pking bullet.png")
                    pm.change_size(15,15)
                    pm.x = round(pking.rect.centerx)
                    pm.y = round(pking.rect.centery)


                    if (stage == 1):
                        pm.xmove = random.randint(3, 5)
                        pm.ymove = 0
                    else:
                        pm.xmove = random.randint(0, 15)
                        pm.ymove = random.randint(1, 5)

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

                # 보스 총알쏘는 패턴1(좌우로 왔다갔다 할때)
                # 패턴1일때 미사일 쏘는 주기
                if (stage == 1):     
                    cycle1 = 70
                elif (stage ==2) or (stage==3):
                    cycle1 = 20

                if (isPkingTime) and (pking.pattern_idx == 1) and (int(pm_pattern1_count % cycle1) == 0):
                    # print(pm_list)
                    pm=obj()
                    pm.put_img("./sprites/pking bullet.png")
                    pm.change_size(15,15)
                    pm.x = round(pking.rect.centerx)
                    pm.y = round(pking.rect.centery)
                    if (stage == 1):
                        pm.xmove = random.randint(3, 5)
                        pm.ymove = 0
                    elif (stage ==2):
                        pm.xmove = 0
                        pm.ymove = 7    
                    elif (stage ==3):
                        pm.xmove = random.randint(0,7) 
                        pm.ymove = random.randint(1,5)
                    
                    pm_list.append(pm)
                pm_pattern1_count += 1
                pd_list = []

                for i in range(len(pm_list)):
                    pm=pm_list[i]
                    pm.x -= pm.xmove
                    pm.y += pm.move
                    if pm.y>height or pm.x < 0:
                        pd_list.append(i)

                pd_list.reverse()
                for d in pd_list:
                    del pm_list[d]
                #
                global collision_time
                global item_time

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

                    # 7. 익룡이 미사일에 맞으면 익룡과 미사일 모두 사라집니다.

                    if (len(m_list)==0):
                        pass
                    else:
                        if (m.x>=p.rect.left)and(m.x<=p.rect.right)and(m.y>p.rect.top)and(m.y<p.rect.bottom):
                            print("격추 성공")
                            isDown=True
                            boom=obj()
                            boom.put_img("./sprites/boom.png")
                            boom.change_size(200,100)
                            boom.x=p.rect.centerx-round(p.rect.width)*2.5
                            boom.y=p.rect.centery-round(p.rect.height)*1.5
                            playerDino.score+=30
                            p.kill()
                            m_list.remove(m)

                    #

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
                        if life < max_life:
                            life += 1
                        if (stage == 0):    #보너스 스테이지에서만 포인트도 증가
                            playerDino.score += 10                            
                        l.kill()
                    elif l.rect.right < 0:
                        l.kill()

                for k in slow_items:
                    k.movement[0] = -1 * gamespeed
                    if pygame.sprite.collide_mask(playerDino, k):
                        if pygame.mixer.get_init() is not None:
                            checkPoint_sound.play()
                        gamespeed_down()
                        new_ground.speed += 1
                        k.kill()
                    elif k.rect.right < 0:
                        k.kill()


                STONE_INTERVAL = 100
                CACTUS_INTERVAL = 50
                # 익룡을 더 자주 등장시키기 위해 12로 수정했습니다. (원래값은 300)
                PTERA_INTERVAL = 12
                #
                CLOUD_INTERVAL = 300
                SHIELD_INTERVAL = 400
                LIFE_INTERVAL = 1000
                SLOW_INTERVAL = 1000

                OBJECT_REFRESH_LINE = width * 0.8
                MAGIC_NUM = 10

                #보너스 스테이지가 아니면 보스 등장
                if (stage != 0) and (isPkingAlive) and (elapsed_time > pking_appearance_time):
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

                    if (len(m_list)==0):
                        pass
                    else:
                        if (m.x>=pking.rect.left)and(m.x<=pking.rect.right)and(m.y>pking.rect.top)and(m.y<pking.rect.bottom):
                            isDown=True
                            boom=obj()
                            boom.put_img("./sprites/boom.png")
                            boom.change_size(200,100)
                            boom.x=pking.rect.centerx-round(pking.rect.width)
                            boom.y=pking.rect.centery-round(pking.rect.height/2)
                            pking.get_damage(1)
                            m_list.remove(m)

                            if pking.current_health == 0:
                                pking.kill()
                                isPkingAlive=False
                                isBossKilled = True

                    #
                    if (len(pm_list)==0):
                        pass
                    else:
                        for pm in pm_list:
                            if (pm.x>=playerDino.rect.left)and(pm.x<=playerDino.rect.right)and(pm.y>playerDino.rect.top)and(pm.y<playerDino.rect.bottom):
                                print("공격에 맞음.")
                                playerDino.collision_immune = True
                                life -= 2
                                gamespeed_down()
                                
                                # 보스의 총알에 맞으면 사운드 추가
                                die_sound.play()
                                collision_time = pygame.time.get_ticks()
                                if life <= 0:
                                    playerDino.isDead = True
                                pm_list.remove(pm)
                else:   #보스 등장아니고
                    if (stage ==0): #보너스 스테이지면 구름이랑 life아이템만 나옴
                        if len(clouds) < 5 and random.randrange(CLOUD_INTERVAL) == MAGIC_NUM:
                            Cloud(width, random.randrange(height / 5, height / 2))

                        if len(life_items) == 0:
                            last_obstacle.empty()
                            last_obstacle.add(LifeItem(gamespeed, object_size[0], object_size[1]))
                        else:
                            for l in last_obstacle:
                                if l.rect.right < OBJECT_REFRESH_LINE:
                                    last_obstacle.empty()
                                    last_obstacle.add(LifeItem(gamespeed, object_size[0], object_size[1]))
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

                playerDino.update()
                cacti.update()
                clouds.update()
                life_items.update()
                if (stage != 0):
                    fire_cacti.update()
                    stones.update()
                    pteras.update()
                    shield_items.update()
                    slow_items.update()

                new_ground.update()
                scb.update(playerDino.score, stage)
                highsc.update(high_score, stage)
                speed_indicator.update(gamespeed - 3, stage)
                heart.update(life)

                # 보스몬스터 타임이면,
                if isPkingTime:
                    pking.update()
                #
                if pygame.display.get_surface() != None:

                    if(stage == 1) or (stage ==0):
                        screen.fill(background_col)
                    elif(stage == 2):
                        screen.fill(background_col2)
                    elif(stage == 3):
                        screen.fill(background_col3)
                    new_ground.draw()
                    clouds.draw(screen)
                    scb.draw()
                    speed_indicator.draw()
                    screen.blit(speed_text, (width * 0.01, height * 0.13))

                    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000   # 경과 시간(ms)을 1000으로 나누어서 초(s) 단위로 표시

                    if(stage == 2):
                        timer = pygame.font.Font(None, 40).render(str(int(total_time - elapsed_time)), True, (255, 255, 255))
                    else:
                        timer = pygame.font.Font(None, 40).render(str(int(total_time - elapsed_time)), True, (0, 0, 0))
                    screen.blit(timer, (width * 0.01, height * 0.2))

                    if elapsed_time <= 3:
                        if (stage == 0):
                            # 출력할 글자, True, 글자 색상
                            stage_info = pygame.font.Font(None, 100).render(str("BONUS STAGE"), True, (0, 0, 0))
                            screen.blit(stage_info, (width * 0.20, height * 0.4))
                        elif (stage == 1):
                            stage_info = pygame.font.Font(None, 120).render(str("STAGE 1"), True, (0, 0, 0)) 
                            screen.blit(stage_info, (width * 0.275, height * 0.4))
                        elif (stage == 2):
                            stage_info = pygame.font.Font(None, 120).render(str("STAGE 2"), True, (255, 255, 255))
                            screen.blit(stage_info, (width * 0.275, height * 0.4))
                        elif (stage == 3):
                            stage_info = pygame.font.Font(None, 120).render(str("STAGE 3"), True, (0, 0, 0))
                            screen.blit(stage_info, (width * 0.275, height * 0.4))

                    heart.draw()
                    if high_score != 0:
                        highsc.draw()
                        screen.blit(HI_image, HI_rect)

                    life_items.draw(screen)
                    if (stage!=0):
                        cacti.draw(screen)
                        fire_cacti.draw(screen)
                        stones.draw(screen)
                        pteras.draw(screen)
                        shield_items.draw(screen)
                        slow_items.draw(screen)


                        # pkingtime이면, 보스몬스터를 보여줘라.
                        if isPkingTime:
                            # print(pking.pattern_idx)
                            pking.draw()
                            pking.bos_health()

                            # 보스 익룡이 쏘는 미사일을 보여준다.
                            for pm in pm_list:
                                pm.show()
                        #
                    #

                    # 5. 미사일 배열에 저장된 미사일들을 게임 스크린에 그려줍니다.
                    for m in m_list:
                        m.show()
                        # print(type(mm.x))
                    if isDown :
                        boom.show()
                        boomCount+=1
                        # boomCount가 5가 될 때까지 boom이미지를 계속 보여준다.
                        if boomCount>10:
                            boomCount=0
                            isDown=False
                    #

                    playerDino.draw()
                    resized_screen.blit(
                        pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                        resized_screen_centerpos)

                    # 만약 시간이 0 이하이면 게임 종료
                    if total_time - elapsed_time <= 0:
                        print("타임아웃")
                        
                        # 보스를 죽이면 다음 스테이지로 넘어감, 보너스 스테이지에서는 그냥 넘어감
                        if (isBossKilled == False) and (stage!=0):
                            gameOver = True
                        else: 
                            if (stage == 1):
                                pygame.time.wait(500)
                                gameplay_hard( stage+1, life, gamespeed, playerDino.score, player )
                                return True
                            elif (stage == 2):
                                pygame.time.wait(500)
                                gameplay_hard( stage-2, life, gamespeed, playerDino.score, player )
                                return True
                            elif (stage == 0):
                                gameplay_hard( stage+3, life, gamespeed, playerDino.score, player )
                                return True
                            elif (stage == 3):
                                print("모든 스테이지 클리어")
                                pygame.time.wait(500)

                                you_won = True
                                gameOver = True

                    if pygame.display.get_surface() != None:
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

                    checkPoint_sound.play()#속도 증가 시 체크포인트 소리

                counter = (counter + 1)
                

            highsc.update(high_score, stage)

        while gameOver:
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                gameQuit = True
                gameOver = False
            else:
                if high_score != 0:
                    highsc.draw()
                    screen.blit(HI_image, HI_rect)
                if (you_won == True) :
                    disp_gameOver_msg(you_won_image)
                else :
                    disp_gameOver_msg(gameover_image)
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
                            name = typescore(playerDino.score)
                            if not db.is_limit_data(playerDino.score):
                                db.query_db(
                                    f"insert into user(username, score) values ('{name}', '{playerDino.score}');")
                                db.commit()
                                introFlag = board()
                                return introFlag
                            else:
                                introFlag = board()
                                return introFlag
            if gameQuit:
                break


            if pygame.display.get_surface() != None:
                resized_screen.blit(
                    pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                    resized_screen_centerpos)
                pygame.display.update()
            clock.tick(FPS)