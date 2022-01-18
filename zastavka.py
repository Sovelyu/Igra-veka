import os
import random
import sys
import pygame
from random import choice
import pygame as pg
import sqlite3


def draw(screen):
    fon = pygame.transform.scale(load_image('backg.png'), (500, 500))
    screen.blit(fon, (0, 0))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


FPS = 50
clock = pygame.time.Clock()
airs = pygame.sprite.Group()
angry = pygame.sprite.Group()
fish = pygame.sprite.Group()
chr = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
au = 10
och = 0
maxoch = 0
muss = True
fl = False
ids = ''
pg.init()
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT = pg.font.Font(None, 32)


class InputBox:

    def __init__(self, x, y, w, h, pas=False):
        size = 500, 500
        screen = pygame.display.set_mode(size)
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = ''
        self.txt_surface = FONT.render(self.text, True, self.color)
        self.active = False
        self.pas = pas

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text) < 20:
                        self.text += event.unicode
                if self.pas:
                    self.txt_surface = FONT.render('⚫' * len(self.text), True, self.color)
                else:
                    self.txt_surface = FONT.render(self.text, True, self.color)

    def get_text(self):
        return self.text

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pg.draw.rect(screen, self.color, self.rect, 2)


def terminate():
    pygame.quit()
    sys.exit()


def buttons(screen, button, button1, button2, button3, button4):
    sp = ['Играть', 'Описание', 'Таблица лидеров', 'Выкл/вкл звук', 'Выход']
    spp = [button, button1, button2, button3, button4]
    font = pygame.font.Font(pygame.font.match_font('monsterrat'), 30)

    # потом картинку для кнопки сделаю maybe
    for i in range(5):
        pygame.draw.rect(screen, pygame.Color('lightblue'), spp[i])
        string = font.render(sp[i], 1, pygame.Color('darkblue'))
        intro_rect = string.get_rect()
        if i != 2 and i != 1:
            intro_rect.left = 445 // 2 - (intro_rect.height // 2)
        else:
            if i == 1:
                intro_rect.left = 345 // 2 - (intro_rect.height // 2) + 35
            else:
                intro_rect.left = 345 // 2 - (intro_rect.height // 2)

        intro_rect.top = 50 + 100 * i
        if i == 3:
            intro_rect.left = 345 // 2 - (intro_rect.height // 2) + 10
        screen.blit(string, intro_rect)


def button(screen, ret, text, coord=(305, 160)):
    sp = [text]
    spp = [ret]
    font = pygame.font.Font(pygame.font.match_font('monsterrat'), 30)

    # потом картинку для кнопки сделаю maybe
    pygame.draw.rect(screen, pygame.Color('lightblue'), ret)
    string = font.render(text, 1, pygame.Color('darkblue'))
    intro_rect = string.get_rect()
    intro_rect.top, intro_rect.left = coord
    screen.blit(string, intro_rect)


def ffon():
    fon = pygame.transform.scale(load_image('backg.png'), (500, 500))
    screen.blit(fon, (0, 0))
    pygame.display.flip()


def button_fon():
    fon = pygame.transform.scale(load_image('okean.jpg'), (500, 500))
    screen.blit(fon, (0, 0))
    pygame.display.flip()


def registration(screen):
    global ids
    global maxoch
    pygame.display.set_caption('Дайвер')
    clock = pygame.time.Clock()
    font = pg.font.Font(pg.font.match_font('monsterrat'), 30)
    log = font.render('Логин', 1, pygame.Color('lightblue'))
    intro_rect = log.get_rect()
    intro_rect.top, intro_rect.left = 75, 55
    pas = font.render('Пароль', 1, pygame.Color('lightblue'))
    iintro_rect = log.get_rect()
    iintro_rect.top, iintro_rect.left = 180, 95
    input_box1 = InputBox(50, 100, 410, 32)
    input_box2 = InputBox(100, 200, 310, 32, pas=True)
    input_boxes = [input_box1, input_box2]
    done = False
    slovar = {}

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if rect.collidepoint(event.pos):
                    terminate()
                if ret.collidepoint(event.pos):
                    con = sqlite3.connect('data/players.sqlite')
                    cur = con.cursor()
                    result = cur.execute("""SELECT * FROM player
                                                        WHERE id > 0""").fetchall()
                    for y in result:
                        if input_box1.get_text() == y[1] and \
                                str(y[2]) == input_box2.get_text():
                            ids = y[0]
                            maxoch = y[-1]
                            start_screen(screen)

                        slovar[y[1]] = y[2]
                    if input_box1.get_text() and input_box2.get_text():
                        key = list(slovar.keys())
                        val = list(slovar.values())
                        if input_box1.get_text() not in key:
                            kortej = (len(key) + 1, input_box1.get_text(),
                                      input_box2.get_text(), 0)
                            ids = len(key) + 1
                            con = sqlite3.connect('data/players.sqlite')
                            cur = con.cursor()
                            res = cur.execute('''INSERT INTO player(id, name,
                                                            password, count) VALUES(?, ?, ?, ?);''', kortej)
                            con.commit()

                    start_screen(screen)

            screen.fill((30, 30, 30))
            screen.blit(log, intro_rect)
            screen.blit(pas, iintro_rect)
            ret = pygame.Rect(140, 300, 220, 32)
            button(screen, ret, 'Регистрация/Вход')
            rect = pygame.Rect(180, 380, 140, 32)
            button(screen, rect, 'Выход', (385, 215))

            for box in input_boxes:
                box.handle_event(event)
        for box in input_boxes:
            box.draw(screen)
        pg.display.flip()
        clock.tick(30)


def start_screen(screen):
    fl = False
    global muss
    pygame.mixer.Channel(0).play(pygame.mixer.Sound('data/mus.mp3'), -1)
    intro_text = ["                    ДАЙВЕР В ГЛУБИНАХ", "",
                  "Правила игры",
                  "нажимайте стрелки на клавиатуре",
                  "чтобы обходить препятствия и получать",
                  "кислород для жизни."]

    button, button1 = pygame.Rect(145, 40, 200, 50), pygame.Rect(145, 140, 200, 50)
    button2, button3 = pygame.Rect(145, 240, 200, 50), pygame.Rect(145, 340, 200, 50)
    button4 = pygame.Rect(145, 440, 200, 50)

    fon = pygame.transform.scale(load_image('okean.jpg'), (500, 500))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(pygame.font.match_font('monsterrat'), 30)
    text_coord = 50
    buttons(screen, button, button1, button2, button3, button4)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button3.collidepoint(event.pos):
                    if muss:
                        pygame.mixer.stop()
                        muss = False
                    else:
                        pygame.mixer.Channel(0).play(pygame.mixer.Sound('data/mus.mp3'), -1)
                        muss = True
                if button4.collidepoint(event.pos):
                    terminate()
                else:
                    ret = pygame.Rect(450, 10, 45, 45)
                    if button.collidepoint(event.pos):
                        choose_level(screen, fon, text_coord, font)
                    if button1.collidepoint(event.pos):
                        fl = True
                        screen.blit(fon, (0, 0))
                        for line in intro_text:
                            string_rendered = font.render(line, 1, pygame.Color('lightblue'))
                            intro_rect = string_rendered.get_rect()
                            text_coord += 10
                            intro_rect.top = text_coord
                            intro_rect.x = 10
                            text_coord += intro_rect.height
                            screen.blit(string_rendered, intro_rect)
                    if button2.collidepoint(event.pos):
                        screen.blit(fon, (0, 0))
                        con = sqlite3.connect('data/players.sqlite')
                        cur = con.cursor()
                        text = cur.execute("""SELECT name, count FROM player
                                    WHERE id > 0""").fetchall()
                        data = sorted(text, reverse=True, key=lambda x: int(x[1]))
                        liders = []
                        liders.append(['имя', '     очки'])
                        liders.append(['', ''])
                        for y in range(len(data)):
                            liders.append([str(data[y][0]), str(data[y][1])])
                            if y == 20:
                                break
                        n = 0
                        text_coord = 50
                        for line in liders:
                            lin = font.render(' '.join(line), 1, pygame.Color('coral'))
                            intro_rect = lin.get_rect()
                            intro_rect.left, intro_rect.top = 30, 10 + n * 20
                            screen.blit(lin, intro_rect)
                            n += 1
                        fl = True
                    if ret.collidepoint(event.pos):
                        start_screen(screen)
                    if fl:
                        pygame.draw.rect(screen, pygame.Color('lightblue'), ret)
                        string = font.render('<-', 1, pygame.Color('darkblue'))
                        intro_rect = string.get_rect()
                        intro_rect.left = 460
                        intro_rect.top = 20
                        screen.blit(string, intro_rect)

        pygame.display.flip()
        clock.tick(FPS)


def choose_level(screen, fon, text_coord, font):
    global au
    global och
    for item in chr:
        item.kill()
    for item in airs:
        item.kill()
    for item in fish:
        item.kill()
    for item in angry:
        item.kill()
    for item in all_sprites:
        item.kill()
    con = sqlite3.connect('data/players.sqlite')
    cur = con.cursor()
    res = cur.execute(f'''UPDATE player SET count = {str(max(och, maxoch))} WHERE id = {str(ids)}''')
    con.commit()
    au = 100
    och = 0
    screen.blit(fon, (0, 0))
    intro_text = ["Выберите сложность"]
    string_rendered = font.render(intro_text[0], 1, pygame.Color('lightblue'))
    intro_rect = string_rendered.get_rect()
    text_coord += 10
    intro_rect.top = text_coord
    intro_rect.x = 140
    text_coord += intro_rect.height
    screen.blit(string_rendered, intro_rect)
    bbutton = pygame.Rect(145, 100, 200, 50)
    bbutton1 = pygame.Rect(145, 200, 200, 50)
    bbutton2 = pygame.Rect(145, 300, 200, 50)

    sp = ['Легкий', 'Средний', 'Сложный']
    spp = [bbutton, bbutton1, bbutton2]
    font = pygame.font.Font(pygame.font.match_font('monsterrat'), 30)
    ret = pygame.Rect(450, 10, 45, 45)
    pygame.draw.rect(screen, pygame.Color('lightblue'), ret)
    string = font.render('<-', 1, pygame.Color('darkblue'))
    intro_rect = string.get_rect()
    intro_rect.left = 460
    intro_rect.top = 20
    screen.blit(string, intro_rect)

    for i in range(3):
        pygame.draw.rect(screen, pygame.Color('lightblue'), spp[i])
        string = font.render(sp[i], 1, pygame.Color('darkblue'))
        intro_rect = string.get_rect()
        if i != 2 and i != 1:
            intro_rect.left = 445 // 2 - (intro_rect.height // 2)
        else:
            intro_rect.left = 345 // 2 - (intro_rect.height // 2) + 35
        intro_rect.top = 115 + 100 * i
        screen.blit(string, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ret.collidepoint(event.pos):
                    start_screen(screen)
                if bbutton.collidepoint(event.pos):
                    ffon()
                    main(screen, 1)
                if bbutton1.collidepoint(event.pos):
                    ffon()
                    main(screen, 2)
                if bbutton2.collidepoint(event.pos):
                    ffon()
                    main(screen, 3)
        pygame.display.flip()
        clock.tick(FPS)


class Air(pygame.sprite.Sprite):
    def __init__(self, size, image, group, i, j, file, level):
        super().__init__(group)
        self.image = image  # и размеры
        self.level = level
        self.rect = self.image.get_rect()
        self.rect.x = i * 40
        self.i = i
        self.rect.y = 450
        self.jj = j + 1
        self.file = file

    def update(self):
        self.rect = self.rect.move(random.randrange(3) - 1,
                                   -1 * self.level)


class Angry_fish(pygame.sprite.Sprite):
    def __init__(self, size, image, group, i, j, file, level):
        super().__init__(group)
        self.level = level
        self.image = image  # и размеры
        self.rect = self.image.get_rect()
        self.rect.x = i * 40
        self.i = i
        sp = ['fishh1.png', 'fishh2.png', 'fishh3.png', 'fishh4.png']
        self.frames = []
        self.cou = 0
        for i in range(4):
            self.frames.append(pygame.transform.scale(load_image(sp[i], -1), (40, 40)))
        self.rect.y = 450
        self.jj = j + 1
        self.file = file

    def update(self):
        self.image = self.frames[self.cou]
        self.cou += 1
        if self.cou > 3:
            self.cou = 0
        self.rect = self.rect.move(0, -1 * self.level)


class Fish(pygame.sprite.Sprite):
    def __init__(self, size, image, group, i, j, file, level):
        super().__init__(group)
        self.level = level
        self.image = image  # и размеры
        self.rect = self.image.get_rect()
        self.rect.x = i * 40
        self.i = i
        sp = ['fish1.png', 'fish2.png', 'fish3.png', 'fish4.png', 'fish5.png']
        self.frames = []
        self.cou = 0
        for i in range(5):
            self.frames.append(pygame.transform.scale(load_image(sp[i], -1), (40, 40)))
        self.rect.y = 450
        self.jj = j + 1
        self.file = file

    def update(self):
        self.image = self.frames[self.cou]
        self.cou += 1
        if self.cou > 4:
            self.cou = 0
        self.rect = self.rect.move(0, -1 * self.level)


def vozduh():
    global au
    au += 20
    if au > 100:
        au = 100


def minus_vozduh():
    global au
    au -= 20


def ochki():
    global och
    och += 1


def vod():
    pg.mixer.music.load('data/voda.mp3')
    pg.mixer.music.play()


def smert(screen, muss):
    global au
    running = False
    if au < 0:
        if muss:
            pg.mixer.music.load('data/main.mp3')
            pg.mixer.music.play()
        running = True
    while running:
        fon = pygame.transform.scale(load_image('trup4.jpg'), (500, 500))
        font = pg.font.Font(pg.font.match_font('monsterrat'), 30)
        screen.blit(fon, (0, 0))
        ret = pygame.Rect(420, 10, 75, 30)
        button(screen, ret, 'Назад', coord=(15, 425))
        pg.display.flip()
        smert_text = ["YOU DIED", "",
                      "у вас закончился кислород!"]
        text_coord = 50
        for line in range(len(smert_text)):
            lin = font.render(smert_text[line], 1, pygame.Color('coral'))
            intro_rect = lin.get_rect()
            intro_rect.left, intro_rect.top = 200 - line * 50, 200 + line * 10
            screen.blit(lin, intro_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ret.collidepoint(event.pos):
                    fon = pygame.transform.scale(load_image('okean.jpg'), (500, 500))
                    choose_level(screen, fon, text_coord, font)
            elif event.type == pygame.KEYDOWN:
                pass
        pygame.display.flip()
        clock.tick(FPS)


class Character(pygame.sprite.Sprite):
    def __init__(self, size, image, muss, *group):
        super().__init__(*group)
        self.image = image  # и размеры
        self.rect = self.image.get_rect()
        self.rect.x = 245
        self.fl = muss
        self.rect.y = 10

    def update(self, nap, auu):
        if nap == 'left':
            self.rect = self.rect.move(-10, 0)
        if nap == 'right':
            self.rect = self.rect.move(10, 0)
        if nap == 'up' and self.rect.top >= 0:
            self.rect = self.rect.move(0, -5)
        if nap == 'down':
            self.rect = self.rect.move(0, 10)
        if self.rect.y >= 412:
            self.rect = self.rect.move(0, -402)
        if self.rect.x >= 465:
            self.rect = self.rect.move(-465, 0)
        if self.rect.x <= -5:
            self.rect = self.rect.move(455, 0)
        if nap == 'sass':
            self.rect = self.rect.move(0, 3)
        if pygame.sprite.spritecollideany(self, airs):
            if self.fl:
                vod()
            airs.remove(pygame.sprite.spritecollideany(self, airs))
            vozduh()
        if pygame.sprite.spritecollideany(self, angry):
            if self.fl:
                vod()
            angry.remove(pygame.sprite.spritecollideany(self, angry))
            minus_vozduh()
        if pygame.sprite.spritecollideany(self, fish):
            if self.fl:
                vod()
            fish.remove(pygame.sprite.spritecollideany(self, fish))
            ochki()


def nadpisi(string, intro_rect, sstring, iintro_rect, sprite, sprites, ret,
            sprut, spru, stroka, rectal):
    draw(screen)
    pygame.draw.rect(screen, pygame.Color('lightblue'), ret)
    screen.blit(string, intro_rect)
    screen.blit(sstring, iintro_rect)
    screen.blit(stroka, rectal)
    sprites.draw(screen)
    sprite.draw(screen)
    sprut.draw(screen)
    spru.draw(screen)
    sprites.update()
    sprut.update()
    spru.update()


def main(screen, level):
    global au
    global och
    running = True
    clock = pygame.time.Clock()
    vrema = 0
    if level == 1:
        file = open('data/easy_level.txt', encoding="utf8").readlines()
    elif level == 2:
        file = open('data/medium_level.txt', encoding="utf8").readlines()
    elif level == 3:
        file = open('data/hard_level.txt', encoding="utf8").readlines()
    stena = choice(file)
    for i in range(len(stena)):
        if stena[i] == '*':
            image = load_image('air.png', -1)
            image = pygame.transform.scale(image, (40, 40))
            Air(size, image, all_sprites, i, 0, file, level)
            Air(size, image, airs, i, 0, file, level)
        if stena[i] == '+':
            image3 = load_image('fish1.png', -1)
            image3 = pygame.transform.scale(image3, (40, 40))
            Fish(size, image3, all_sprites, i, 0, file, level)
            Fish(size, image3, fish, i, 0, file, level)
        if stena[i] == '&':
            image2 = load_image('fishh1.png', -1)
            image2 = pygame.transform.scale(image2, (40, 40))
            Angry_fish(size, image2, all_sprites, i, 0, file, level)
            Angry_fish(size, image2, angry, i, 0, file, level)

    image = load_image("chel.png", -1)
    image = pygame.transform.scale(image, (45, 85))
    Character(size, image, muss, chr)
    Character(size, image, muss, all_sprites)
    sprites = airs
    sprite = chr
    sprut = angry
    spru = fish
    sprite.draw(screen)
    sprites.draw(screen)
    pygame.display.flip()
    ret = pygame.Rect(430, 10, 65, 30)
    pygame.draw.rect(screen, pygame.Color('lightblue'), ret)
    font = pygame.font.Font(pygame.font.match_font('monsterrat'), 20)
    string = font.render('Назад', 1, pygame.Color('darkblue'))
    intro_rect = string.get_rect()
    intro_rect.left, intro_rect.top = 443, 17

    sstring = font.render(f'Запас кислорода; {au}/100', 1, pygame.Color('darkblue'))
    stroka = font.render(f'Очки: {och}', 1, pygame.Color('darkblue'))
    iintro_rect = sstring.get_rect()
    iintro_rect.left, iintro_rect.top = 10, 10
    rectal = sstring.get_rect()
    rectal.left, iintro_rect.top = 10, 25
    timer = pygame.time.get_ticks
    sec = 1000
    deadline = timer() + sec

    while running:
        if vrema == 200:
            vrema = 0
            stena = choice(file)
            for i in range(len(stena)):
                if stena[i] == '*':
                    image = load_image('air.png', -1)
                    image = pygame.transform.scale(image, (40, 40))
                    Air(size, image, all_sprites, i, 0, file, level)
                    Air(size, image, airs, i, 0, file, level)
                if stena[i] == '+':
                    image3 = load_image('fish1.png', -1)
                    image3 = pygame.transform.scale(image3, (40, 40))
                    Fish(size, image3, all_sprites, i, 0, file, level)
                    Fish(size, image3, fish, i, 0, file, level)
                if stena[i] == '&':
                    image2 = load_image('fishh1.png', -1)
                    image2 = pygame.transform.scale(image2, (40, 40))
                    Angry_fish(size, image2, all_sprites, i, 0, file, level)
                    Angry_fish(size, image2, angry, i, 0, file, level)
        now = timer()
        if now > deadline:
            au -= 5
            timer = pygame.time.get_ticks
            deadline = timer() + sec
            sprite.update('sass', au)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ret.collidepoint(event.pos):
                    fon = pygame.transform.scale(load_image('okean.jpg'), (500, 500))
                    text_coord = 50
                    font = pygame.font.Font(pygame.font.match_font('monsterrat'), 30)
                    for i in airs:
                        airs.remove(i)
                    for i in fish:
                        fish.remove(i)
                    for i in angry:
                        angry.remove(i)
                    choose_level(screen, fon, text_coord, font)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    sprite.update('left', au)
                elif event.key == pygame.K_RIGHT:
                    sprite.update('right', au)
                elif event.key == pygame.K_DOWN:
                    sprite.update('down', au)
                elif event.key == pygame.K_UP:
                    sprite.update('up', au)
        sprite.update('sas', au)
        nadpisi(string, intro_rect, sstring, iintro_rect, sprite, sprites, ret,
                sprut, spru, stroka, rectal)
        sstring = font.render(f'Запас кислорода: {au}/100', 1, pygame.Color('darkblue'))
        stroka = font.render(f'Очки: {och}', 1, pygame.Color('darkblue'))
        smert(screen, muss)
        pygame.display.flip()
        clock.tick(FPS)
        vrema += 1


if __name__ == '__main__':
    pygame.init()  # инициализация Pygame:
    size = 500, 500  # размеры окна:
    screen = pygame.display.set_mode(size)
    registration(screen)