from src.setting import *


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
