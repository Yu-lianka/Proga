import math
import random
import pygame
import sys



FPS = 30
MyGREEN=(58,107,56)
DRED=(127,24,13)
RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600
POINTS = 0
LIFE=5

def hit():
    """Попадание шарика в цель."""
    global POINTS
    POINTS += 1

def live():
    """Счётчик жизней пушки"""
    global LIFE
    LIFE-=1
    
    
def draw_score():
    """Выводит счёт на экран"""
    text = 'Your score is {score:n}'
    font = pygame.font.SysFont(None,24)
    img=font.render(text.format(score=POINTS),True,BLUE)
    screen.blit(img,(20,20))
    
def draw_live():
    """Выводит кол-во жизней пушки на экран"""
    text = 'Your lifes are {score:n}'
    font = pygame.font.SysFont(None,24)
    img=font.render(text.format(score=LIFE),True,BLUE)
    screen.blit(img,(20,40))

class triangle:

    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ НЕ ТРЕУГОЛЬНИКИ. Конструктор класса triangle

        Args:
        x - начальное положение снарядов по горизонтали
        y - начальное положение снарядов по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = random.choice(GAME_COLORS)
        self.live = 3


    def move_t(self):
        """Движение triangle c учётом гравитации.
            Умирает при столкновении со стеной.
            Запускются правой кнопкой мыши.
            Выпускается очередь снарядов при движении мыши"""
        
        g=2
        self.x+=self.vx
        self.y+=self.vy
        self.vy+=g

        if self.x+self.r>=WIDTH-2 or self.x-self.r<=0 or self.y+self.r>=HEIGHT-2 or self.y-self.r<=0+5:
            self.live-=1
            
        if self.live<=0:
            self.x=-1000

    def draw_t(self):
        """Рисует снаряд"""
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )


    def hittest_t(self, obj):
        
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x-obj.x)**2+(self.y-obj.y)**2<(self.r+obj.r)**2 :
            return True
        else:
            return False
    def hite(self,obj):
        '''проверка столкновения с новой целью'''
        if obj.x+obj.l > self.x-self.r and \
   obj.x < self.x+self.r and \
   obj.y+obj.l > self.y-self.r and \
   obj.y < self.y+self.r:
            return True
        else:
            return False

class Ball:
    def __init__(self, screen: pygame.Surface, x=100, y=540):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = random.choice(GAME_COLORS)
        self.live = 3

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        g=2
        self.x+=self.vx
        self.y+=self.vy
        self.vy+=g

        
        if self.x+self.r>=WIDTH-2:
            self.vx*=-0.8
            self.x=WIDTH-self.r-3
            

        elif self.x-self.r<=0:
            
            self.vx*=-0.8
            self.x=self.r+1
        elif self.y+self.r>=HEIGHT-2:
            self.live-=1
            
            self.vy*=-0.8
            self.y-=self.r+1

        elif self.y-self.r<=0+5:
            self.vy*=-0.8
            self.y=self.r+6
        if self.live<=0:
            self.x=-1000
        
    
    def draw(self):
        """Рисует снаряд"""
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x-obj.x)**2+(self.y-obj.y)**2<(self.r+obj.r)**2 :
            return True
        else:
            return False
        
    def hite(self,obj):
        """проверка столкновения с новой целью"""
        if obj.x+obj.l > self.x-self.r and \
   obj.x < self.x+self.r and \
   obj.y+obj.l > self.y-self.r and \
   obj.y < self.y+self.r:
            return True
        else:
            return False
    


class Gun:
    def __init__(self, screen: pygame.Surface):
        """Конструктор пушки"""
        self.screen = screen
        self.vx=10
        self.f2_power = 10
        self.f_power = 20
        self.f2_on = 0
        self.f_on=0
        self.an=0
        self.an = 1
        self.color = GREY
        self.x=0
        self.y=540
        self.points=0
        self.time=0
        self.l=60
        self.live=5

    def mover(self):

        """Движение вправо при нажатии (d) """

        self.x+=self.vx
        
    def movel(self):
        
        """Движение влево при нажатии (a)"""
        
        self.x-=self.vx
        

    def fire_start(self, event):
        """Флажок для начала огня triangle """
        self.f_on = 1


    def fire_do(self, event):
        """Выстрел triangle.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global triangles, rocket
        if self.f_on == 1:
            self.time += 1
        
        if self.time > 1:
            rocket+=1
            new_triangle = triangle(self.screen, self.x+self.l, self.y)
            new_triangle.r += 5
            self.an=math.atan2((event.pos[1]-new_triangle.y), (event.pos[0]-new_triangle.x))
            new_triangle.vx = 2*self.f_power * math.cos(self.an)
            new_triangle.vy = 2*self.f_power * math.sin(self.an)
            triangles.append(new_triangle)
            self.time=0



    def fire_end(self,event):
        """Конец огня triangle"""
        self.f_on=0

    def fire2_start(self, event):
        """Флажок для начала огня мячом """
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen, self.x+self.l, self.y)
        new_ball.r += 20
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10
        
    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = 1*math.atan((event.pos[1]-450) / (abs(event.pos[0]-20)+0.000001))
            
        if self.f2_on or self.f_on:
            self.color = GREEN
        else:
            self.color = GREY


    def draw(self):
        """Рисуем пушку и дуло"""
        L=self.f2_power

        if pygame.mouse.get_pos()[0]-self.x>0:
            x = self.x-0.1+self.l + math.sin(self.an)+L*math.cos(self.an)
            y = self.y+0.1 - math.cos(self.an)+ L*math.sin(self.an)
        else:
            x = self.x-0.1+self.l - math.sin(self.an)-L*math.cos(self.an)
            y = self.y+0.1 - math.cos(self.an)+ L*math.sin(self.an)
            

        pygame.draw.line(surface= self.screen, color=self.color, start_pos=[self.x+self.l, self.y],
                         end_pos=[x, y], width=10)

        pygame.draw.rect(screen, MyGREEN, (self.x, self.y, self.l, self.l))



    def power_up(self):
        """Вид дула при активации"""
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = GREEN
        elif self.f_on:
            self.color=GREEN
        else:
            self.color = GREY

class Bomb:

    def __init__(self,screen: pygame.Surface, x, y):
        """Конструктор бомб для агресивной цели"""
        self.color=BLACK
        self.c2=RED
        self.x=x
        self.y=y
        self.r=10
        self.o=3
        self.vy=1
        self.live=1
        

    def draw(self):
        """Отрисовка"""
        pygame.draw.circle(
            screen,
            self.color,
            (self.x, self.y),
            self.r
        )
        pygame.draw.circle(screen,self.c2, (self.x, self.y), self.r, self.o)
    def move(self):
        """Движение. Умирает, если попадает по пушке"""
        if self.live==0:
            self.y=1000
        else:
            g=2
            self.y+=self.vy
            self.vy+=g

    def hittest(self,obj):
        """Проверка сталкивания с пушкой"""
        if obj.x+obj.l > self.x-self.r and \
   obj.x < self.x+self.r and \
   obj.y+obj.l > self.y-self.r and \
   obj.y < self.y+self.r:
            return True
        else:
            return False
        

class Evil:
    def __init__(self, screen: pygame.Surface):
        """Конструктор агресивной цели"""
        self.x=random.randint(600, 780)
        self.y=random.randint(10, 30)
        self.vx = random.randint(-1,1)
        self.l = random.randint(10, 50)
        self.live=10
        self.color = DRED
        self.new_evil()
        #self.on=0
        self.time=1
        self.screen = screen

    def new_evil(self):
        """Респавн агресивной цели"""
        self.x=random.randint(600, 780)
        self.y=random.randint(10, 30)
        self.l = random.randint(50, 100)
        self.live=8

    ''' Не реализовано
    def speed(self):
        if POINTS<5:
            self.vx =0
        else:
            self.vx+=1
    '''
            

    def move(self):
        """Движение агресивной цели. Бегает по горизонтали"""
        self.x+=self.vx

        if self.x+self.l>=WIDTH-2:
            self.vx*=-1
            self.x=WIDTH-self.l-3
        elif self.x-self.l<=0:
            self.vx*=-1
            self.x=self.l+1


    def boom(self):
        """Пуляется бомбами если пушка движется. При убивании пушки обнуляет счёт (перезапуск)"""
        global bombs
        self.time += 1
        if self.time > 5:
            new_bomb = Bomb(self.screen, self.x+self.l*0.5, self.y+self.l)
            bombs.append(new_bomb)
            self.time=0
        

    def draw(self):
        """Рисует цель"""

        pygame.draw.rect(screen, self.color, (self.x, self.y, self.l, self.l))


    
    

class Target:

    def __init__(self, c):
        """Конструктор обычной цели"""
        self.x=random.randint(600, 780)
        self.y=random.randint(300, 550)
        self.vx = 1
        self.vy = 2
        self.color = c
        self.r = random.randint(5, 50)
        self.live=10
        self.k=0
        
        self.new_target()
        

    def new_target(self):
        """ Инициализация новой цели. """
        x = random.randint(600, 780)
        self.x = x
        self.y = random.randint(300, 550)
        self.r = random.randint(5, 50)
        self.live=10

    def speed(self):
        ''' Скорость мишений. После 5го попадания уровень усложняется - мишени начинают двигаться.
            После каждого попадания мишень ускоряется'''
        if POINTS<5:
            self.vx =0
            self.vy =0
        else:
            self.vx = 1*(POINTS-4)
            self.vy = 2*(POINTS-4)
            
        
        
    def move(self):
        ''' Движение мишени'''
        
        self.x+=self.vx
        self.y+=self.vy
        

        
        if self.x+self.r>=WIDTH-2:
            self.vx*=-0.8
            self.x=WIDTH-self.r-3
            

        elif self.x-self.r<=0:
            
            self.vx*=-0.8
            self.x=self.r+1
        elif self.y+self.r>=HEIGHT-2:
            self.live-=1
            
            self.vy*=-0.8
            self.y-=self.r+1

        elif self.y-self.r<=0+5:
            self.vy*=-0.8
            self.y=self.r+6
        
    

    def draw(self):
        """Рисует цель"""

        pygame.draw.circle(
            screen,
            self.color,
            (self.x, self.y),
            self.r
        )
        


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []
triangles=[]
bombs=[]
gun=[]
rocket=0

background = pygame.image.load('background1.png').convert()
background = pygame.transform.smoothscale(background, screen.get_size())




clock = pygame.time.Clock()
gun = Gun(screen)
target = Target(RED)
target2 = Target(BLUE)
evil=Evil(screen)
finished = False
k=0
k2=0
f=0
m=0


while not finished:
    screen.blit(background,(0,0))
    gun.draw()
    target.draw()
    if POINTS>=3:
        target2.draw()
    if POINTS>=7:
        evil.draw()
        m=1    

    evil.move()
    
    draw_score()
    draw_live()
    
    for b in balls:
        b.draw()
    pygame.display.update()

    for t in triangles:
        t.draw_t()
    pygame.display.update()

    for b in bombs:
        b.draw()
    pygame.display.update()


    clock.tick(FPS)
    
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        gun.fire_do(event)
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button==3:
                gun.fire_start(event)
                f=1
            elif event.button==1 or event.button==2:
                gun.fire2_start(event)
                f=2
        elif event.type == pygame.MOUSEBUTTONUP and f==2 :
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEBUTTONUP and f==1 :
            gun.fire_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)
        elif keys[pygame.K_d]:
            gun.mover()
            if m==1:
                evil.boom()
        elif keys[pygame.K_a]:
            gun.movel()
            if m==1:
                evil.boom()


    if k==0:
        target.speed()
        k+=1
    if k2==0:
        target2.speed()
        k2+=1
    #gun.move()
    target.move()
    target2.move()
    #evil.boom()
    for b in bombs:
        b.move()
        if b.hittest(gun):
            gun.live-=1
            b.live=0
            live()
            if gun.live==0:
                POINTS=0
                gun.live=5
                m=0
                LIFE=5
    for b in balls:
        b.move()
        if b.hittest(target):
            target.live = 0
            hit()
            k=0
            target.new_target()
        if b.hite(evil):
            evil.live = 0
            hit()

            evil.new_evil()
        if POINTS>=3 and b.hittest(target2):
            target2.live = 0
            hit()
            k2=0
            target2.new_target()
            
    for t in triangles:
        t.move_t()
        if t.hittest_t(target):
            target.live-=1
            if target.live==0:
                hit()
                target.new_target()
        if t.hittest_t(target2):
            target2.live-=1
            if target2.live==0:
                hit()
                target2.new_target()
        if t.hite(evil):
            evil.live = 0
            hit()
            evil.new_evil()
    


        
    gun.power_up()

pygame.quit()
