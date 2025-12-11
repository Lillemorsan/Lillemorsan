# -*- coding: utf-8 -*-
import random
import pygame
import pygbag
import time

# Seedning
try:
    seed = pygbag.web.loop.time()
except:
    seed = time.time()

random.seed(seed)

def load_dict(file_name):
    with open(file_name, encoding="utf-8") as file:
        words = file.read().splitlines()
    words = [w.strip() for w in words if w.strip()]
    return [word[:5].upper() for word in words]

DICT_GUESSING = load_dict("svenska_5bokstaver.txt")
DICT_ANSWERS = load_dict("svenska_5bokstaver.txt")
ANSWER = random.choice(DICT_ANSWERS)

WIDTH = 600
HEIGHT = 700
MARGIN = 10
T_MARGIN = 100
B_MARGIN = 125
LR_MARGIN = 690

GREY = (70,70,80)
GREEN = (0,160,0)
PURPLE = (67,0,90)

INPUT = ""
GUESSES = []
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"
UNGUESSED = ALPHABET
GAME_OVER = False

pygame.init()
pygame.font.init()
pygame.display.set_caption("Lettro")
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
background_image = pygame.image.load("mounteverest.jpg").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

SQ_SIZE = 100
FONT = pygame.font.SysFont("free sans bold", 50)
FONT_SMALL = pygame.font.SysFont("free sans bold", 25)

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_COLOR = (0,160,0)
BUTTON_TEXT_COLOR = (255, 255, 255)
BUTTON_FONT = pygame.font.SysFont("free sans bold", 30)

# Tangentbordslayout
KEYBOARD_LAYOUT = [
    "QWERTYUIOPÅ",
    "ASDFGHJKLÖÄ",
    "ZXCVBNM"
]

KEY_RADIUS = 25
KEY_SPACING_X = 10
KEY_SPACING_Y = 10
KEY_COLOR = (70, 70, 80)
KEY_USED_COLOR = (40, 40, 50)
KEY_PRESSED_COLOR = (100, 100, 100)
LETTER_COLOR = (255, 255, 255)

# ---- Funktioner ----

def determine_unguessed_letters(guesses):
    guessed_letters = "".join(guesses)
    return "".join([l for l in ALPHABET if l not in guessed_letters])

def determine_color(guess, j):
    letter = guess[j]
    if letter == ANSWER[j]:
        return GREEN
    elif letter in ANSWER:
        n_target = ANSWER.count(letter)
        n_correct = sum(1 for i in range(5) if guess[i] == ANSWER[i] and guess[i] == letter)
        n_occurrence = sum(1 for i in range(j+1) if guess[i] == letter)
        if n_target - n_correct - n_occurrence >= 0:
            return PURPLE
    return GREY

# ---- Wordle-korrekt färglogik ----
def keyboard_letter_color(letter):
    best_color = KEY_COLOR
    for guess in GUESSES:
        for i, l in enumerate(guess):
            if l == letter:
                if l == ANSWER[i]:
                    return GREEN
                elif l in ANSWER:
                    best_color = PURPLE
                else:
                    best_color = KEY_USED_COLOR
    return best_color

# Starta skärm
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# -----------------------------------------
# Huvudloop
# -----------------------------------------
if __name__ == "__main__":
    animating = True
    pressed_key = None

    while animating:
        screen.blit(background_image, (0, 0))

        # --------- Rita rutorna ----------
        y = T_MARGIN
        for i in range(6):
            x = LR_MARGIN
            for j in range(5):
                square = pygame.Rect(x, y, SQ_SIZE, SQ_SIZE)
                pygame.draw.rect(screen, GREY, square, width=2, border_radius=7)

                if i < len(GUESSES):
                    color = determine_color(GUESSES[i], j)
                    pygame.draw.rect(screen, color, square, border_radius=7)
                    letter = FONT.render(GUESSES[i][j], True, (255,255,255))
                    screen.blit(letter, letter.get_rect(center=square.center))

                if i == len(GUESSES) and j < len(INPUT):
                    letter = FONT.render(INPUT[j], True, GREY)
                    screen.blit(letter, letter.get_rect(center=square.center))

                x += SQ_SIZE + MARGIN
            y += SQ_SIZE + MARGIN

        # --------- Rita tangentbordet ----------
        key_rects = []
        start_y = HEIGHT - B_MARGIN - 3*(2*KEY_RADIUS + KEY_SPACING_Y)

        for row_index, row in enumerate(KEYBOARD_LAYOUT):
            row_length = len(row)
            start_x = (WIDTH - (row_length * (2*KEY_RADIUS + KEY_SPACING_X)
                     - KEY_SPACING_X)) // 2
            y = start_y + row_index * (2*KEY_RADIUS + KEY_SPACING_Y)

            for i, letter in enumerate(row):
                x = start_x + i * (2*KEY_RADIUS + KEY_SPACING_X)
                rect = pygame.Rect(x, y, 2*KEY_RADIUS, 2*KEY_RADIUS)
                key_rects.append((letter, rect))

                color = KEY_PRESSED_COLOR if pressed_key == letter else keyboard_letter_color(letter)
                pygame.draw.ellipse(screen, color, rect)

                tex = FONT_SMALL.render(letter, True, LETTER_COLOR)
                screen.blit(tex, tex.get_rect(center=rect.center))

        # --------- ENTER ----------
        enter_rect = pygame.Rect(WIDTH//2 - 140, HEIGHT - B_MARGIN, 120, 40)
        enter_color = KEY_PRESSED_COLOR if pressed_key == "ENTER" else KEY_COLOR
        pygame.draw.rect(screen, enter_color, enter_rect, border_radius=8)
        enter_tex = FONT_SMALL.render("ENTER", True, LETTER_COLOR)
        screen.blit(enter_tex, enter_tex.get_rect(center=enter_rect.center))

        # --------- DELETE ----------
        delete_rect = pygame.Rect(WIDTH//2 + 20, HEIGHT - B_MARGIN, 120, 40)
        delete_color = KEY_PRESSED_COLOR if pressed_key == "DELETE" else KEY_COLOR
        pygame.draw.rect(screen, delete_color, delete_rect, border_radius=8)
        delete_tex = FONT_SMALL.render("DELETE", True, LETTER_COLOR)
        screen.blit(delete_tex, delete_tex.get_rect(center=delete_rect.center))

        # --------- Game over ----------
        if len(GUESSES) == 6 and GUESSES[5] != ANSWER:
            GAME_OVER = True

        if GAME_OVER:
            ans_tex = FONT.render(ANSWER, True, GREY)
            screen.blit(ans_tex, ans_tex.get_rect(center=(WIDTH//2 , 75)))

            button_rect = pygame.Rect((WIDTH - BUTTON_WIDTH)//2,
                                      HEIGHT - 10 - B_MARGIN//2,
                                      BUTTON_WIDTH, BUTTON_HEIGHT)

            pygame.draw.rect(screen, BUTTON_COLOR, button_rect, border_radius=10)
            txt = BUTTON_FONT.render("Starta Om", True, BUTTON_TEXT_COLOR)
            screen.blit(txt, txt.get_rect(center=button_rect.center))

        pygame.display.flip()

        # --------- Events ----------
        pressed_key = None
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                animating = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    animating = False

                elif event.key == pygame.K_BACKSPACE and len(INPUT) > 0:
                    INPUT = INPUT[:-1]

                elif event.key == pygame.K_RETURN and len(INPUT) == 5:
                    GUESSES.append(INPUT)
                    UNGUESSED = determine_unguessed_letters(GUESSES)
                    GAME_OVER = INPUT == ANSWER
                    INPUT = ""

                elif event.key == pygame.K_SPACE:
                    ANSWER = random.choice(DICT_ANSWERS)
                    GUESSES = []
                    INPUT = ""
                    UNGUESSED = ALPHABET
                    GAME_OVER = False

                elif len(INPUT) < 5 and not GAME_OVER:
                    INPUT += event.unicode.upper()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                if not GAME_OVER:
                    # Klick på bokstäver
                    for letter, rect in key_rects:
                        if rect.collidepoint(mx, my) and len(INPUT) < 5:
                            INPUT += letter
                            pressed_key = letter

                    # ENTER
                    if enter_rect.collidepoint(mx, my) and len(INPUT) == 5:
                        GUESSES.append(INPUT)
                        UNGUESSED = determine_unguessed_letters(GUESSES)
                        GAME_OVER = INPUT == ANSWER
                        INPUT = ""
                        pressed_key = "ENTER"

                    # DELETE
                    if delete_rect.collidepoint(mx, my) and len(INPUT) > 0:
                        INPUT = INPUT[:-1]
                        pressed_key = "DELETE"

                # Starta om-knapp
                if GAME_OVER and button_rect.collidepoint((mx, my)):
                    ANSWER = random.choice(DICT_ANSWERS)
                    GUESSES = []
                    UNGUESSED = ALPHABET
                    INPUT = ""
                    GAME_OVER = False

