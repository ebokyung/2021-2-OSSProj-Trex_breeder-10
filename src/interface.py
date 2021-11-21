from src.setting import *


class Ground:
    def __init__(self, speed=-5):
        self.image, self.rect = load_image('ground.png', -1, -1, -1)
        self.image1, self.rect1 = load_image('ground.png', -1, -1, -1)
        self.rect.bottom = height
        self.rect1.bottom = height
        self.rect1.left = self.rect.right
        self.speed = speed

    def draw(self):
        screen.blit(self.image, self.rect)
        screen.blit(self.image1, self.rect1)

    def update(self):
        self.rect.left += self.speed
        self.rect1.left += self.speed

        if self.rect.right < 0:
            self.rect.left = self.rect1.right

        if self.rect1.right < 0:
            self.rect1.left = self.rect.right


class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image, self.rect = load_image('cloud.png', int(90*30/42), 30, -1)
        self.speed = 1
        self.rect.left = x
        self.rect.top = y
        self.movement = [-1*self.speed, 0]

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)
        if self.rect.right < 0:
            self.kill()


class Heart:

    def __init__(self, sizex=-1, sizey=-1, x=-1, y=-1):
        self.image, self.rect = load_image("hpbar.png", sizex, sizey)
        
        if x == -1:
            self.rect.left = width * 0.01
        else:
            self.rect.left = x

        if y == -1:
            self.rect.top = height * 0.04
        else:
            self.rect.top = y

    def draw(self):
        screen.blit(self.image, self.rect)


class HeartIndicator:

    def __init__(self, max_life, life, player_num = 0):
        self.player_num = 0 
        if player_num == 0:
            self.heart_size = [20,30]
            self.max_life = max_life
            self.current_life = life
            self.life_set = []
        else:
            self.player_num = 1
            self.heart_size = [20,30]
            self.max_life = max_life
            self.current_life = life
            self.life_set = []

    def draw(self):
        if self.player_num == 0:
            pygame.draw.rect(screen, black, (width * 0.01, height * 0.04, self.heart_size[0]*self.max_life, self.heart_size[1]), 3)
        else:
            pygame.draw.rect(screen, black, (width * 0.01, height * 0.04 * 2, self.heart_size[0]*self.max_life, self.heart_size[1]), 3)
        for life in self.life_set:
            life.draw()

    #아마도 수정필요?
    def update(self, life):
        self.current_life = life
        self.life_set = [Heart(self.heart_size[0], self.heart_size[1], width * 0.01 + i * self.heart_size[0]) for i in range(self.current_life)]


class Scoreboard:

    def __init__(self, x=-1, y=-1):
        self.score = 0
        self.tempimages, self.temprect = load_sprite_sheet('numbers.png', 12, 1, 15, int(15*6/5), -1)
        self.image = pygame.Surface((80, int(15*6/5)))
        self.rect = self.image.get_rect()
        if x == -1:
            self.rect.left = width*0.89
        else:
            self.rect.left = x
        if y == -1:
            self.rect.top = height*0.05
        else:
            self.rect.top = y

    def draw(self):
        screen.blit(self.image, self.rect)

    # 남현 - 211121 현재 stage를 파라미터로 받아옴
    def update(self,score, stage = 1):
        score_digits = extractDigits(score)
        if(stage == 1):
            self.image.fill(background_col)
        elif(stage == 2):
            self.image.fill(background_col2)
        elif(stage == 3):
            self.image.fill(background_col3)

        for s in score_digits:
            self.image.blit(self.tempimages[s], self.temprect)
            self.temprect.left += self.temprect.width
        self.temprect.left = 0
