import pygame
from pygame.locals import *
from _thread import *
import os
import random
import socket
import json
import math

from gamelogic import objects, world, common

SOCK_COUNT = 2

pygame.init()

W, H = 800, 437
win = pygame.display.set_mode((W, H))
pygame.display.set_caption("Projekt Kyyber 2021 Client")

bg_orig = [
    pygame.image.load(os.path.join("images/bg1/", str(x) + ".png")).convert_alpha()
    for x in range(1, 8)
]
# bg_orig = [pygame.image.load(os.path.join('images/bg2/', str(x) + '.png')).convert_alpha() for x in range(1,7)]

bg = []
BGW = int(bg_orig[0].get_width() * (H / float(bg_orig[0].get_height())))
for i in bg_orig:
    bg.append(pygame.transform.scale(i, (BGW, H)))
bg.reverse()

clock = pygame.time.Clock()
camera_pos = 0
gameoverfade = 0


def redrawWindow():
    global camera_pos, gameoverfade
    largeFont = pygame.font.SysFont("comicsans", 30)
    hugeFont = pygame.font.SysFont("comicsans", 90)

    gameover = False
    for player in gamestate.players:
        if player.id == my_id:
            camera_pos = player.x - W / 2
            camera_pos = min(camera_pos, world.WORLD_SIZE - W)
            camera_pos = max(camera_pos, 0)
            text = largeFont.render(
                "AMMO: {}, RELOAD: {}, HP: {}".format(
                    player.ammo, player.reloadleft, player.hp
                ),
                1,
                (255, 255, 255),
            )
            break
    else:
        text = hugeFont.render("TRY HARDER!", 1, (255, 255, 255))
        gameover = True

    for j, layer in enumerate(bg):
        for i in range(0, W * 2, BGW):
            camera_pos_bg = (camera_pos * (float(j) / float(len(bg)))) % BGW
            win.blit(bg[j], (i - camera_pos_bg, 0))
    for player in gamestate.players:
        player.draw(win, camera_pos, my_id)
    sorted_enemies = sorted(gamestate.enemies, key=lambda i: i.y_pos)
    sorted_enemies.reverse()  # Closest ones to front
    for enemy in sorted_enemies:
        enemy.draw(win, camera_pos)
    for boss in gamestate.bosses:
        boss.draw(win, camera_pos)
    for projectile in gamestate.projectiles:
        projectile.draw(win, camera_pos)

    if gameover:
        veil = pygame.Surface((W, H))
        veil.fill((0, 0, 0))
        veil.set_alpha(gameoverfade)
        gameoverfade += 0.1
        if gameoverfade > 255:
            gameoverfade = 255
        win.blit(veil, (0, 0))
        win.blit(text, (W / 2 - text.get_width() / 2, H / 2 - text.get_height() / 2))
    else:
        win.blit(text, (20, 400))
        for i, achievement in enumerate(achievements):
            win.blit(
                largeFont.render(
                    str(achievement) + ": " + str(achievements[achievement]),
                    1,
                    (255, 255, 255),
                ),
                (10, 10 + 30 * i),
            )
    pygame.display.update()


def update_gamestate_thread():
    global gamestate
    while True:
        clock.tick(world.SPEED)
        gamestate = common.physics(gamestate)
        redrawWindow()


gamestate = objects.gamestate()
achievements = []
my_id = 0
sendevent = []

start_new_thread(update_gamestate_thread, ())

sockets = set()
main = None

for i in range(SOCK_COUNT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockets.add(sock)

serveraddr = "127.0.0.1"
serveraddr = "challenge.fi" # Join remote server
for sock in sockets:
    if main is None:
        main = sock
    sock.connect((serveraddr, 9999))

data = main.recv(1024).strip()
my_id = json.loads(data)["player_id"]
while True:
    me = None
    for player in gamestate.players:
        if player.id == my_id:
            me = player
    if me:
        sendevent.append(
            [
                ['shoot', 4900, 100, 0.38]
            ])
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if keys[pygame.K_x]:
                eka = me.x #+ math.cos(me.mouseDir(camera_pos)) * 60
                toka = me.y + 60 #- math.sin(me.mouseDir(camera_pos)) * 60
                mouse = me.mouseDir(camera_pos)
                sendevent.append(
                    [
                        "shoot", eka, toka, mouse
                    ]
                )
                print(f"{eka}, {toka}, {mouse}")
            if keys[pygame.K_r]:
                eka = 4900
                sendevent.append(
                        # ['shoot', 4931.029795212544, 260.67432742841345, 1.7208623491309805]
                        #['shoot', 4754.656506303356, 100, 0]
                        ['shoot', 4900, 100, 0.38]
                        #205.57772405728508, 297.39211224788403, 0.38633721482131445]
                )
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                eka = me.x - 20 + math.cos(me.mouseDir(camera_pos)) * 60
                print(eka)
                toka = me.y - math.sin(me.mouseDir(camera_pos)) * 60
                mouse = me.mouseDir(camera_pos)
                sendevent.append(
                    [
                        "shoot", eka, toka, mouse
                    ]
                )
                print(f"{eka}, {toka}, {mouse}")
        if keys[pygame.K_SPACE]:
            sendevent.append(["jump"])

        if keys[pygame.K_m]:
            sendevent.append(["jump"])
            sendevent.append(["reload"])
            sendevent.append(["jump"])
        if keys[pygame.K_a] and not me.dir == 1:
            sendevent.append(["left"])
        elif keys[pygame.K_d] and not me.dir == -1:
            sendevent.append(["right"])
        elif not me.dir == 0:
            sendevent.append(["stop"])

    common.parse_clientevents(my_id, json.dumps(sendevent), gamestate)
    # for boss in gamestate.bosses:
    #     print(f"{boss.id} {boss.x},{boss.y}, hp:{boss.hp}")
    for sock in sockets:
        sock.sendall(bytes(json.dumps(sendevent), "utf-8"))
    # if gamestate.projectiles:
    #     for projectile in gamestate.projectiles:
    #         print(f"{projectile.x},{projectile.y} d:{projectile.dir} r:{projectile.moveremaining}")

    if sendevent:
        print(sendevent)
        print(f"{me.x},{me.y}")
    sendevent = []

    for boss in gamestate.bosses:
        print(boss.x-me.x, boss.y-me.y, boss.hp)

    # receive packets until a valid json can be formed
    response = b""
    while True:
        chunk = main.recv(1000)
        response += chunk
        try:
            gamestate_dict, achievements = json.loads(response)
            gamestate = common.update_gamestate_from_dict(
                gamestate, gamestate_dict
            )
            break
        except Exception as e:
            pass
