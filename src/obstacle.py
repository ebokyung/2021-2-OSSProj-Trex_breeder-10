from src.setting import *


class Cactus(pygame.sprite.Sprite):
    def __init__(self, speed=5, sizex=-1, sizey=-1):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.images, self.rect = load_sprite_sheet('cacti-small.png', 3, 1, sizex, sizey, -1)
        self.rect.bottom = int(0.98*height)
        self.rect.left = width + self.rect.width
        self.image = self.images[random.randrange(0,3)]
        self.movement = [-1*speed, 0]

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)

        if self.rect.right < 0:
            self.kill()


class fire_Cactus(pygame.sprite.Sprite):
    def __init__(self, speed=5, sizex=-1, sizey=-1):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.images, self.rect = load_sprite_sheet('fire_cacti6.png', 3, 1, sizex, sizey, -1)
        self.rect.bottom = int(0.98*height)
        self.rect.left = width + self.rect.width
        self.image = self.images[random.randrange(0,3)]
        self.movement = [-1*speed, 0]

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)

        if self.rect.right < 0:
            self.kill()

# pteraking 클래스
class PteraKing(pygame.sprite.Sprite):
    
    def __init__(self, speed=0, sizex=-1, sizey=-1):
        pygame.sprite.Sprite.__init__(self)
        self.images, self.rect = load_sprite_sheet('pteraking.png', 2, 1, sizex, sizey, -1)
        # self.ptera_height = [height*0.82, height*0.75, height*0.60]
        self.ptera_height=height*0.3
        # self.rect.centery = self.ptera_height[random.randrange(0, 3)]
        self.rect.centery = self.ptera_height
        self.rect.left = width - self.rect.width -50
        self.image = self.images[0]
        self.movement = [-1*speed, 0]
        # 
        self.down_speed=2
        self.down_movement=[0,self.down_speed]
        self.up_speed=2
        self.up_movement=[0,-self.up_speed]

        self.stop_movement = [0,0]
        # 
        self.index = 0
        self.counter = 1
        # 새로운 정의.
        self.isAlive=True
        self.pattern_idx=0
        self.goleft=True
        self.reached_leftmost=False
        self.reached_rightmost=False
        self.pattern0_time=200
        self.pattern0_counter=0

        self.pattern1_time=200
        self.pattern1_counter=0
        self.pattern1_speed=15
        self.pattern1_lastmove=False

        self.pattern2_counter=0
        self.godown=True
        self.bottommost=height*0.6
        self.topmost = height * 0.3
        # 보스가 내려가서 머무르는 시간
        self.pattern2_bottommost_time = 200

        self.stop=False

        self.goup=False
        self.topmost=height*0.3
        # 
        self.hp = 15

    def draw(self):
        screen.blit(self.image, self.rect)
        # 총알 그리기

    def pattern0(self):

        self.pattern1_lastmove=False
        self.pattern0_counter+=1
        self.movement[0]=0
        if self.counter %10==0:
            self.index = (self.index+1) % 2
        self.image = self.images[self.index]
        self.rect = self.rect.move(self.movement)
        if self.pattern0_counter % self.pattern0_time == 0:
            self.pattern_idx = 1

    def pattern1(self):

        self.pattern1_counter+=1

        if self.counter % 10 == 0:
            self.index = (self.index+1) % 2
        self.image = self.images[self.index]

        if (self.goleft == True) and (self.reached_leftmost == False):
            self.movement[0] = -1 * self.pattern1_speed
            self.rect = self.rect.move(self.movement)

            if self.rect.left < 0:
                self.goleft = False
                self.reached_leftmost = True
                self.reached_rightmost = False
        
        else:
            self.movement[0] = self.pattern1_speed
            self.rect = self.rect.move(self.movement)

            if self.pattern1_lastmove:
                if self.rect.left > width - self.rect.width -50:
                        self.goleft = True
                        self.reached_rightmost = True
                        self.reached_leftmost = False

                        self.pattern_idx = 2
            else:
                if self.rect.left > width - self.rect.width -50:
                        self.goleft = True
                        self.reached_rightmost = True
                        self.reached_leftmost = False
            
            if self.pattern1_counter % self.pattern1_time == 0:
                self.pattern1_lastmove=True

        # 총알발사.

    def pattern2(self):

        if self.counter % 10 ==0:
            self.index = (self.index+1) % 2
        self.image = self.images[self.index]
        
        if self.godown:
            self.rect = self.rect.move(self.down_movement)
            if self.rect.centery > self.bottommost:
                self.godown = False
                self.goup =  False
                self.stop = True
        
        if self.stop:
            self.pattern2_counter +=1
            self.rect = self.rect.move(self.stop_movement)
            if self.pattern2_counter % self.pattern2_bottommost_time == 0:
                self.godown = False
                self.goup = True
                self.stop = False
        
        if self.goup:
            self.rect = self.rect.move(self.up_movement)
            if self.rect.centery < self.topmost:
                self.godown = True
                self.goup = False
                self.stop = False
                self.pattern_idx = 0

    def update(self):

        self.counter=self.counter+1
     
        # 패턴0
        if self.pattern_idx==0:
            # self.pattern0_counter=0
            self.pattern0()

        # 패턴1 
        elif self.pattern_idx==1:
            # self.pattern1_counter = 0
            self.pattern1()
           
        # 패턴2
        else: 
            # self.pattern2_counter = 0 
            self.pattern2()

# 





class Ptera(pygame.sprite.Sprite):

    def __init__(self, speed=5, sizex=-1, sizey=-1):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.images, self.rect = load_sprite_sheet('ptera.png', 2, 1, sizex, sizey, -1)
        self.ptera_height = [height*0.82, height*0.75, height*0.60]
        self.rect.centery = self.ptera_height[random.randrange(0, 3)]
        self.rect.left = width + self.rect.width
        self.image = self.images[0]
        self.movement = [-1*speed, 0]
        self.index = 0
        self.counter = 0

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        if self.counter % 10 == 0:
            self.index = (self.index+1) % 2
        self.image = self.images[self.index]
        self.rect = self.rect.move(self.movement)
        self.counter = (self.counter + 1)
        if self.rect.right < 0:
            self.kill()

class Stone(pygame.sprite.Sprite):
    def __init__(self, speed=5, sizex=-1, sizey=-1):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.images, self.rect = load_sprite_sheet('stone.png', 1, 1, sizex, sizey, -1)
        self.rect.top = height *0.9
        self.rect.bottom = int(0.98*height)
        self.rect.left = width + self.rect.width

        #self.ptera_height = height * 0.3
        ## self.rect.centery = self.ptera_height[random.randrange(0, 3)]
        #self.rect.centery = self.ptera_height
        #self.rect.left = width - self.rect.width - 50




        self.image = self.images[0]
        self.movement = [-1*speed, 0]

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)

        if self.rect.right < 0:
            self.kill()

