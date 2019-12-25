import time
import sys
import random
import math

import pygame
from pygame.locals import *

from config import *

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
FRAME_WIDTH = 50
TEXT_OFFSET = 10

POINTS_NBR = 1


class App(object):
    def __init__(s):
        pygame.init()
        pygame.display.set_caption('Rota')
        s.d = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        s.deltaTime = 0.0002
        s.angle_speed = 0.003

        s.last_pivot_change_time = time.time()
        s.endTime = time.time()

        s.points = [[random.randint(FRAME_WIDTH, WINDOW_WIDTH - 2 * FRAME_WIDTH),
                    random.randint(FRAME_WIDTH, WINDOW_HEIGHT - FRAME_WIDTH * 2)]
                    for a in range(POINTS_NBR)]
        s.pivot = s.points[random.randint(0, POINTS_NBR - 1)]
        s.point_angles = [math.atan2(point[1] - s.pivot[1], point[0] - s.pivot[0]) for point in s.points]
        s.angle = 1
        s.persistant = False

    def launch(s):
        while not s.handle_loop():
            s.angle += s.angle_speed
            if 2 * math.pi - 0.01 < s.angle < 2 * math.pi + 0.01:
                s.angle = 0

            x = math.cos(s.angle) * 2 * WINDOW_WIDTH
            y = math.sin(s.angle) * 2 * WINDOW_HEIGHT
            angle = math.atan2(y, x)
            inv_angle = math.atan2(-y, -x)

            delta = time.time() - s.last_pivot_change_time
            size = 20 - (5 * delta) if delta < 1 else 10

            trans = (angle + 4) * (200 / 7)
            trans2 = (angle + 4) * (150 / 7)
            line_color = (trans, 255 - trans2, trans)

            pygame.draw.aaline(s.d, line_color, s.pivot, (s.pivot[0] + x, s.pivot[1] + y))
            pygame.draw.aaline(s.d, line_color, s.pivot, (s.pivot[0] - x, s.pivot[1] - y))

            for idx, point in enumerate(s.points):
                if point == s.pivot:
                    pygame.draw.circle(s.d, WHITE, point, int(size))
                    continue
                color = (
                        point[0] * (255 / WINDOW_WIDTH),
                        point[1] * (255 / WINDOW_HEIGHT),
                        255 - (point[1] * (255 / WINDOW_HEIGHT))
                    )
                pygame.draw.circle(s.d, color, point, 10)

                if angle < s.point_angles[idx] < angle + s.angle_speed or inv_angle < s.point_angles[idx] < inv_angle + s.angle_speed:
                    s.pivot = point
                    s.point_angles = [math.atan2(point[1] - s.pivot[1], point[0] - s.pivot[0]) for point in s.points]
                    s.last_pivot_change_time = time.time()
                    break

    def handle_loop(s):
        pygame.display.update()
        s.handle_input()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        delta = time.time() - s.endTime
        if delta < s.deltaTime:
            time.sleep(s.deltaTime - delta)
        s.endTime = time.time()

        if not s.persistant:
            s.d.fill(BLACK)

    def handle_input(s):
        keys = pygame.key.get_pressed()
        buttons = pygame.mouse.get_pressed()
        if keys[K_SPACE]:
            s.angle_speed = 0.003 if s.persistant else 0.512
            s.persistant = not s.persistant
        if keys[K_RETURN]:
            s.points = [s.pivot]
            s.point_angles = [math.atan2(point[1] - s.pivot[1], point[0] - s.pivot[0]) for point in s.points]
        if keys[K_LEFT] and s.angle_speed >= 0:
            s.angle_speed -= 0.00001
        elif keys[K_RIGHT]:
            s.angle_speed += 0.00001
        if buttons[0]:
            pos = pygame.mouse.get_pos()
            s.points.append(list(pos))
            s.point_angles = [math.atan2(point[1] - s.pivot[1], point[0] - s.pivot[0]) for point in s.points]
