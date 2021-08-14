import os
import turtle
import random
import time
BASE_PATH = os.path.dirname(__file__)

class Missile():
    def __init__(self, x, y, color, x2, y2, uppen):
        self.x =x
        self.y=y
        self.color = color
        self.x2 = x2
        self.y2 =y2
        self.uppen = uppen
        global pen
        pen = turtle.Turtle(visible=False)
        pen.speed(0)
        pen.color(color)
        pen.penup()
        pen.setpos(x=x, y=y)
        pen.pendown()
        heading = pen.towards(x=x2, y=y2)
        pen.setheading(heading)
        pen.showturtle()

        self.pen = pen

        self.state = 'launched'
        self.target = [x2, y2]
        self.radius = 0
        self.damage = 0

    def step(self):
        if self.state == 'launched':
            self.pen.forward(self.uppen)
            if self.pen.distance(self.target[0], self.target[1]) < 50:
                self.state = 'explode'
                self.pen.shape('circle')
        elif self.state == 'explode':
            self.radius += 1
            if self.radius > 5:
                self.pen.clear()
                self.pen.hideturtle()
                self.state = 'dead'
            else:
                self.pen.shapesize(self.radius)
        elif self.state == 'dead':
            self.pen.clear()
            self.pen.hideturtle()

    def distance(self,x,y):
        return self.pen.distance(x=x,y=y)
    def get_x(self):
        return self.pen.xcor()
    def get_y(self):
        return self.pen.ycor()

class Base():
    MAX_HP = 1000

    def __init__(self, coordinate, photo_base):
        self.coordinate = coordinate
        self.x = coordinate[0]
        self.y = coordinate[1]
        self.healds = self.MAX_HP
        self.photo_base = photo_base
        global base
        base = turtle.Turtle()
        base.hideturtle()
        base.speed(0)
        base.penup()
        base.setpos(x=self.x, y=self.y)
        pic_pas = os.path.join(BASE_PATH, 'images', photo_base)
        window.register_shape(pic_pas)
        base.shape(pic_pas)
        base.showturtle()
        self.base = base


        display_life = turtle.Turtle()
        display_life.hideturtle()
        display_life.speed(0)
        display_life.penup()
        display_life.goto(x=self.x, y=(self.y-70))
        display_life.write(str(self.healds),align='center', font=['Arial',10,'bold'] )
        self.display_life = display_life
        self.display_hp = self.healds

    def actual_number_of_lives(self):
        if self.healds != self.display_hp:
            self.display_hp = self.healds
            self.display_life.clear()
            self.display_life.write(str(self.display_hp), align='center', font=['Arial', 10, 'bold'])
        elif self.healds <= 0:
            self.healds = 0
            self.display_hp = self.healds
            self.display_life.clear()
            self.display_life.write(str(self.display_hp), align='center', font=['Arial', 10, 'bold'])

    def check_impank(self):
        for enemy_missile in our_attak_missiles:
            if enemy_missile.state != 'explode':
                continue
            if enemy_missile.distance(x=self.x, y=self.y) < enemy_missile.radius * 10:
                self.healds = self.healds - enemy_missile.damage
                print(self.healds)

    def condition(self,cond2,cond3):
        if self.healds <= (self.MAX_HP/2) and self.healds > 0:
            pic_pas = os.path.join(BASE_PATH, 'images', cond2)
            window.register_shape(pic_pas)
            self.base.shape(pic_pas)
            self.base.showturtle()
        elif self.healds <= 0:
            pic_pas = os.path.join(BASE_PATH, 'images', cond3)
            window.register_shape(pic_pas)
            self.base.shape(pic_pas)
            self.base.showturtle()

class Base_fier(Base):
    MAX_HP = 2000

    def get_pic_name(self):
        for missile in our_missiles:
            if missile.distance(self.x, self.y) < 20:
                self.photo_base = start_bilding[5]
            else:
                self.photo_base = start_bilding[0]
            pic_pas = os.path.join(BASE_PATH, 'images', self.photo_base)
            window.register_shape(pic_pas)
            self.base.shape(pic_pas)
            return

class Point_counter():
    def __init__(self):
        display_glasses = turtle.Turtle()
        display_glasses.hideturtle()
        display_glasses.speed(0)
        display_glasses.goto(x=-350, y=(200))
        display_glasses.penup()
        display_glasses.color('gold')
        self.display_glasses = display_glasses
        self.glasses = 0
        self.display_glasses.write(str(self.glasses), align='center', font=['Arial', 10, 'bold'])
        self.display_glasses_1 = self.glasses

    def points_calculation(self):
        self.display_glasses_1 = sum(list_glasses)
        if self.display_glasses_1 != self.glasses:
            self.display_glasses.clear()
            self.display_glasses.write(str(self.display_glasses_1 ), align='center', font=['Arial', 10, 'bold'])


def mofe_missiles(our_missiles_1):
    for out_missile in our_missiles_1:
        out_missile.step()
    dead_missiles = [missile for missile in our_missiles_1 if missile.state== 'dead']
    for dead in dead_missiles:
        our_missiles_1.remove(dead)

def fire_missile(x, y):
    info = Missile(x=coordinate[0][0], y=coordinate[0][1], color='white', x2=x, y2=y, uppen=10)
    our_missiles.append(info)

def configuring_the_attack():
    ATTACK_X, ATTAK_Y = random.randint(-400, 400), random.randint(150, 200)
    direction_of_attack = coordinate[random.randint(0, (len(coordinate)-1))]
    info = Missile(x=ATTACK_X, y=ATTAK_Y, color='red', x2=direction_of_attack[0],
                   y2=direction_of_attack[1], uppen=5)
    info.damage = random.randint(50, 100)
    our_attak_missiles.append(info)

def check_enemi_could():
    if len(our_attak_missiles) < 2:
        configuring_the_attack()

def check_intepriteition():
    for missile in our_missiles:
        if missile.state != 'explode'  :
            continue
        for enemy_missile in our_attak_missiles:
            if enemy_missile.distance(x= missile.get_x(), y= missile.get_y()) < missile.radius*10:
                enemy_missile.state = 'dead'
                list_glasses.append(enemy_missile.damage)

def game_over():
    return game_base.healds < 0 or (house.healds < 0 and kreml.healds <0
    and nucl.healds<0 and skyscr.healds<0)
def building_condition():
    i = 0
    x = 0
    z = 1

    for bilding in bildings:
        bilding.condition(cond2=the_texture_of_the_buildings[i][x],cond3=the_texture_of_the_buildings[i][z])
        i = i+1
        if i ==4 :
            i = 0

def deleting_coordinates_destruction_building():
    for bilding in bildings:
        if bilding.healds <= 0:
            delet_bilding = bilding.coordinate
            for i in coordinate:
                if i == delet_bilding:
                    coordinate.remove(i)

def game():
    global our_missiles,our_attak_missiles,the_texture_of_the_buildings,start_bilding,coordinate
    global game_base,house,kreml,nucl,skyscr,bildings,bilding_and_base
    window.clear()
    window.bgpic(os.path.join(BASE_PATH, 'images', 'background.png'))
    window.tracer(n=2)
    window.onclick(fire_missile)

    our_missiles = []
    our_attak_missiles = []

    the_texture_of_the_buildings = [['house_2.gif', 'house_3.gif'], ['kremlin_2.gif', 'kremlin_3.gif'],
                                    ['nuclear_2.gif', 'nuclear_3.gif'], ['skyscraper_2.gif', 'skyscraper_3.gif']]

    start_bilding = ['base.gif', 'house_1.gif', 'kremlin_1.gif', 'nuclear_1.gif', 'skyscraper_1.gif', 'base_opened.gif']

    coordinate = [[0, -200], [200, -200], [400, -200], [-200, -200], [-400, -200]]

    game_base = Base_fier(coordinate[0], start_bilding[0])
    house = Base(coordinate[1], start_bilding[1])
    kreml = Base(coordinate[2], start_bilding[2])
    nucl = Base(coordinate[3], start_bilding[3])
    skyscr = Base(coordinate[4], start_bilding[4])
    bildings = [house, kreml, nucl, skyscr]
    bilding_and_base = [game_base, house, kreml, nucl, skyscr]

    while True:
        window.update()
        if game_over():
            break
        # попала вражеская ракета или нет в базу
        for bilding in bilding_and_base:
            bilding.check_impank()
        # создание вражеских ракет
        check_enemi_could()
        # перехватила слюзная ракета вражескую
        check_intepriteition()
        # цикл союзной ракеты
        mofe_missiles(our_missiles)
        # раскрытие базы
        game_base.get_pic_name()
        # цикл вражеской ракеты
        mofe_missiles(our_attak_missiles)
        # проверка состояния здания
        building_condition()
        # удаление координат уничтоженного строения
        deleting_coordinates_destruction_building()
        # выволим состояние здоровья здания
        for bilding in bilding_and_base:
            bilding.actual_number_of_lives()
        # Проверка счета
        glasses.points_calculation()
        time.sleep(.01)
    pen = turtle.Turtle(visible=False)
    pen.hideturtle()
    pen.speed(0)
    pen.penup()
    pen.color('red')
    pen.write('game over', align='center', font=['Arial',80,'bold'] )

window = turtle.Screen()
window.setup(1024 + 3, 600 + 3)
window.screensize(1024, 600)
glasses = Point_counter()
list_glasses = []
while True:
    game()
    answer = window.textinput(title='Привет', prompt='Хотите сыграть еще ?(Да/Нет')
    answer = answer.lower()
    if answer not in  ('да', 'д','y','yes'):
        break
input()
window.exitonclick()
window.mainloop()
