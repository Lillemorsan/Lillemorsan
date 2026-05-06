# -*- coding: utf-8 -*-
import random
import pygame
import pygbag
import time

# ---------------- Seed ----------------
try:
    seed = pygbag.web.loop.time()
except:
    seed = time.time()
random.seed(seed)

# ---------------- Ladda ordlista ----------------
def load_dict(file_name):
    with open(file_name, encoding="utf-8") as f:
        words = f.read().splitlines()
    return [w.strip().upper()[:5] for w in words if len(w.strip()) >= 5]

DICT_ANSWERS = load_dict("svenska_5bokstaver.txt")
ANSWER = random.choice(DICT_ANSWERS)

# ---------------- RESET FUNKTION (NY) ----------------
def reset_game():
    global INPUT, GUESSES, GAME_OVER, ANSWER
    INPUT = ""
    GUESSES = []
    GAME_OVER = False
    ANSWER = random.choice(DICT_ANSWERS)

# ---------------- Pygame init ----------------
pygame.init()
pygame.font.init()
pygame.display.set_caption("Lettro")
screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
WIDTH, HEIGHT = screen.get_size()

# ---------------- Bakgrund ----------------
background_image = pygame.image.load("mounteverest.jpg").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# ---------------- Färger ----------------
GREY = (70, 70, 80)
GREEN = (0, 160, 0)
PURPLE = (67, 0, 90)
WHITE = (255, 255, 255)
KEY_USED = (40, 40, 50)

# ---------------- Speldata ----------------
INPUT = ""
GUESSES = []
GAME_OVER = False

# ---------------- Tangentbord ----------------
KEYBOARD_LAYOUT = [
    "QWERTYUIOPÅ",
    "ASDFGHJKLÖÄ",
    "ZXCVBNM"
]

# =================================================
# RESPONSIV LAYOUT (MED MAX / MIN)
# =================================================
def calculate_layout():
    global SQ_SIZE, MARGIN, FONT, FONT_SMALL
    global TOP_MARGIN, BOTTOM_MARGIN
    global KEY_RADIUS, KEY_SPACING_X, KEY_SPACING_Y
    global BUTTON_WIDTH, BUTTON_HEIGHT

    TOP_MARGIN = int(HEIGHT * 0.12)
    BOTTOM_MARGIN = int(HEIGHT * 0.30)

    available_h = HEIGHT - TOP_MARGIN - BOTTOM_MARGIN
    available_w = WIDTH * 0.9

    MAX_SQ_SIZE = 70
    MIN_SQ_SIZE = 45

    SQ_SIZE = min(
        available_w // 5,
        available_h // 6,
        MAX_SQ_SIZE
    )
    SQ_SIZE = max(SQ_SIZE, MIN_SQ_SIZE)

    MARGIN = int(SQ_SIZE * 0.12)

    FONT = pygame.font.SysFont("free sans bold", int(SQ_SIZE * 0.6))
    FONT_SMALL = pygame.font.SysFont("free sans bold", int(SQ_SIZE * 0.32))

    KEY_RADIUS = int(SQ_SIZE * 0.35)
    KEY_SPACING_X = int(KEY_RADIUS * 0.6)
    KEY_SPACING_Y = int(KEY_RADIUS * 0.6)

    BUTTON_WIDTH = int(SQ_SIZE * 1.8)
    BUTTON_HEIGHT = int(SQ_SIZE * 0.7)

calculate_layout()

# =================================================
# Hjälpfunktioner
# =================================================
def determine_color(guess, i):
    if guess[i] == ANSWER[i]:
        return GREEN
    if guess[i] in ANSWER:
        return PURPLE
    return GREY

def keyboard_letter_color(letter):
    best = GREY
    for guess in GUESSES:
        for i, l in enumerate(guess):
            if l == letter:
                if l == ANSWER[i]:
                    return GREEN
                elif l in ANSWER:
                    best = PURPLE
                else:
                    best = KEY_USED
    return best

# =================================================
# HUVUDLOOP
# =================================================
running = True
restart_rect = pygame.Rect(0,0,0,0)  # NY

while running:
    screen.blit(background_image, (0, 0))

    # -------- Wordle-rutor --------
    grid_width = 5 * SQ_SIZE + 4 * MARGIN
    start_x = (WIDTH - grid_width) // 2
    y = TOP_MARGIN

    for row in range(6):
        x = start_x
        for col in range(5):
            rect = pygame.Rect(x, y, SQ_SIZE, SQ_SIZE)
            pygame.draw.rect(screen, GREY, rect, 2, border_radius=8)

            if row < len(GUESSES):
                color = determine_color(GUESSES[row], col)
                pygame.draw.rect(screen, color, rect, border_radius=8)
                txt = FONT.render(GUESSES[row][col], True, WHITE)
                screen.blit(txt, txt.get_rect(center=rect.center))

            elif row == len(GUESSES) and col < len(INPUT):
                txt = FONT.render(INPUT[col], True, GREY)
                screen.blit(txt, txt.get_rect(center=rect.center))

            x += SQ_SIZE + MARGIN
        y += SQ_SIZE + MARGIN

    # -------- Tangentbord --------
    key_rects = []
    start_y = HEIGHT - BOTTOM_MARGIN + SQ_SIZE * 0.3

    for r, row in enumerate(KEYBOARD_LAYOUT):
        row_w = len(row) * (2 * KEY_RADIUS + KEY_SPACING_X) - KEY_SPACING_X
        start_x = (WIDTH - row_w) // 2
        y = start_y + r * (2 * KEY_RADIUS + KEY_SPACING_Y)

        for i, letter in enumerate(row):
            x = start_x + i * (2 * KEY_RADIUS + KEY_SPACING_X)
            rect = pygame.Rect(x, y, 2 * KEY_RADIUS, 2 * KEY_RADIUS)
            key_rects.append((letter, rect))

            pygame.draw.ellipse(screen, keyboard_letter_color(letter), rect)
            txt = FONT_SMALL.render(letter, True, WHITE)
            screen.blit(txt, txt.get_rect(center=rect.center))

    # -------- ENTER / DELETE --------
    enter_rect = pygame.Rect(
        WIDTH//2 - BUTTON_WIDTH - 10,
        HEIGHT - BUTTON_HEIGHT - 10,
        BUTTON_WIDTH,
        BUTTON_HEIGHT
    )
    delete_rect = pygame.Rect(
        WIDTH//2 + 10,
        HEIGHT - BUTTON_HEIGHT - 10,
        BUTTON_WIDTH,
        BUTTON_HEIGHT
    )

    pygame.draw.rect(screen, GREY, enter_rect, border_radius=8)
    pygame.draw.rect(screen, GREY, delete_rect, border_radius=8)

    screen.blit(FONT_SMALL.render("ENTER", True, WHITE),
                FONT_SMALL.render("ENTER", True, WHITE).get_rect(center=enter_rect.center))
    screen.blit(FONT_SMALL.render("DELETE", True, WHITE),
                FONT_SMALL.render("DELETE", True, WHITE).get_rect(center=delete_rect.center))

    # -------- GAME OVER --------
    if GAME_OVER:
        ans = FONT.render(ANSWER, True, GREY)
        screen.blit(ans, ans.get_rect(center=(WIDTH//2, TOP_MARGIN//2)))

        # -------- RESTART KNAPP (NY) --------
        restart_rect = pygame.Rect(
            WIDTH//2 - BUTTON_WIDTH//2,
            TOP_MARGIN//2 + 40,
            BUTTON_WIDTH,
            BUTTON_HEIGHT
        )

        pygame.draw.rect(screen, GREY, restart_rect, border_radius=8)
        screen.blit(FONT_SMALL.render("RESTART", True, WHITE),
                    FONT_SMALL.render("RESTART", True, WHITE).get_rect(center=restart_rect.center))

    pygame.display.flip()

    # ---------------- Events ----------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
            calculate_layout()

        elif event.type == pygame.KEYDOWN and not GAME_OVER:
            if event.key == pygame.K_BACKSPACE and INPUT:
                INPUT = INPUT[:-1]

            elif event.key == pygame.K_RETURN and len(INPUT) == 5:
                GUESSES.append(INPUT)
                GAME_OVER = INPUT == ANSWER or len(GUESSES) == 6
                INPUT = ""

            elif len(INPUT) < 5 and event.unicode.isalpha():
                INPUT += event.unicode.upper()

        elif event.type == pygame.MOUSEBUTTONDOWN and not GAME_OVER:
            mx, my = event.pos

            for letter, rect in key_rects:
                if rect.collidepoint(mx, my) and len(INPUT) < 5:
                    INPUT += letter

            if enter_rect.collidepoint(mx, my) and len(INPUT) == 5:
                GUESSES.append(INPUT)
                GAME_OVER = INPUT == ANSWER or len(GUESSES) == 6
                INPUT = ""

            if delete_rect.collidepoint(mx, my) and INPUT:
                INPUT = INPUT[:-1]

        # -------- RESTART CLICK (NY) --------
        elif event.type == pygame.MOUSEBUTTONDOWN and GAME_OVER:
            mx, my = event.pos
            if restart_rect.collidepoint(mx, my):
                reset_game()
