import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math

# =========================
# CONFIG
# =========================
WIDTH, HEIGHT = 1000, 700
NUM_PARTICLES = 1500

shared_mode = 1

# =========================
# INIT PARTICLES
# =========================
pos_space = np.random.uniform(-4.0, 4.0, (NUM_PARTICLES, 3))

# Saturn
pos_planet = np.zeros((NUM_PARTICLES, 3))
NUM_SPHERE = 700

for i in range(NUM_SPHERE):
    phi = np.random.uniform(0, 2*np.pi)
    costheta = np.random.uniform(-1, 1)
    theta = np.arccos(costheta)
    r = 1.3

    pos_planet[i] = [
        r * np.sin(theta) * np.cos(phi),
        r * np.sin(theta) * np.sin(phi),
        r * np.cos(theta)
    ]

for i in range(NUM_SPHERE, NUM_PARTICLES):
    theta = np.random.uniform(0, 2*np.pi)
    r = np.random.uniform(1.8, 3.8)

    pos_planet[i] = [
        r * np.cos(theta),
        np.random.uniform(-0.05, 0.05),
        r * np.sin(theta)
    ]

# TEXT MODE
text_img = np.zeros((200, 800), dtype=np.uint8)
import cv2
cv2.putText(text_img, "I LOVE YOU", (20, 130),
            cv2.FONT_HERSHEY_SIMPLEX, 3.5, 255, 12, cv2.LINE_AA)

y_idx, x_idx = np.where(text_img > 0)
x_text = (x_idx - 400) / 70.0
y_text = -(y_idx - 100) / 70.0
z_text = np.random.uniform(-0.1, 0.1, len(x_text))

text_points = np.stack((x_text, y_text, z_text), axis=-1)
pos_text = text_points[np.random.choice(len(text_points), NUM_PARTICLES)]

# HEART
pos_heart = np.zeros((NUM_PARTICLES, 3))

for i in range(NUM_PARTICLES):
    t = np.random.uniform(-np.pi, np.pi)
    p = np.random.uniform(-np.pi, np.pi)

    x = 2.0 * (np.sin(t) ** 3)
    y = 2.0*np.cos(t) - 0.7*np.cos(2*t) - 0.3*np.cos(3*t) - 0.1*np.cos(4*t)
    z = np.sin(p) * 0.4

    pos_heart[i] = [x*0.85, y*0.85 + 0.5, z]

current_pos = pos_space.copy()
target_pos = pos_space.copy()

rotation = 0

# =========================
# INIT PYGAME + OPENGL
# =========================
pygame.init()
pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
pygame.display.set_caption("NEBULA HEART - Keyboard Only")

glMatrixMode(GL_PROJECTION)
gluPerspective(45, WIDTH/HEIGHT, 0.1, 50.0)

glMatrixMode(GL_MODELVIEW)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

clock = pygame.time.Clock()

# =========================
# MAIN LOOP
# =========================
running = True

while running:
    pygame.event.pump()

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        elif event.type == KEYDOWN:

            if event.key == K_ESCAPE:
                running = False

            elif event.key == K_F1:
                shared_mode = 1

            elif event.key == K_F2:
                shared_mode = 2

            elif event.key == K_F3:
                shared_mode = 3

            elif event.key == K_F4:
                shared_mode = 4

    # =========================
    # MODE SELECT
    # =========================
    if shared_mode == 1:
        target_pos = pos_space
        rotation += 0.5
    elif shared_mode == 2:
        target_pos = pos_planet
        rotation += 2.0
    elif shared_mode == 3:
        target_pos = pos_text
        rotation = 0
    elif shared_mode == 4:
        target_pos = pos_heart
        rotation += 1.2

    # smooth morph
    current_pos += (target_pos - current_pos) * 0.12

    # =========================
    # RENDER
    # =========================
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0, 0, -12)
    glRotatef(rotation, 0, 1, 0)

    glPointSize(4)
    glBegin(GL_POINTS)

    for i in range(NUM_PARTICLES):

        if shared_mode == 3:
            glColor4f(0.2, 0.8, 1.0, 0.9)
        elif shared_mode == 4:
            glColor4f(1.0, 0.2, 0.5, 0.95)
        elif shared_mode == 2 and i < NUM_SPHERE:
            glColor4f(1.0, 0.5, 0.0, 0.9)
        elif shared_mode == 2:
            glColor4f(1.0, 0.8, 0.3, 0.6)
        else:
            glColor4f(0.2, 0.6, 1.0, 0.8)

        glVertex3f(current_pos[i][0],
                   current_pos[i][1],
                   current_pos[i][2])

    glEnd()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
