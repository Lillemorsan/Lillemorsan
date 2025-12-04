# -*- coding: utf-8 -*-
import random
import pygame
import pygbag
import time

# Fixa att random alltid seedas vid sidstart
try:
    # ta tid i millisekunder från javascript
    seed = pygbag.web.loop.time()
except:
    # fallback om programmet körs lokalt
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
#bokstäver som man skriver storlek
FONT = pygame.font.SysFont("free sans bold", 50)
#tangentbord bokstäver storlek
FONT_SMALL = pygame.font.SysFont("free sans bold", 25)

# --------- Starta om-knapp ---------
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_COLOR = (0,160,0)
BUTTON_TEXT_COLOR = (255, 255, 255)
BUTTON_FONT = pygame.font.SysFont("free sans bold", 30)

# --------- Tangentbord längst ner ---------
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
    unguessed_letters = ""
    for letter in ALPHABET:
        if letter not in guessed_letters:
            unguessed_letters += letter
    return unguessed_letters

def determine_color(guess, j):
    letter = guess[j]
    if letter == ANSWER[j]:
        return GREEN
    elif letter in ANSWER:
        n_target = ANSWER.count(letter)
        n_correct = 0
        n_occurrence = 0
        for i in range(5):
            if guess[i] == letter:
                if i <= j:
                    n_occurrence += 1
                if letter == ANSWER[i]:
                    n_correct += 1
        if n_target - n_correct - n_occurrence >= 0:
            return PURPLE
    return GREY

def keyboard_letter_color(letter):
    for guess in GUESSES:
        for i, l in enumerate(guess):
            if l == letter:
                if l == ANSWER[i]:
                    return GREEN
                elif l in ANSWER:
                    return PURPLE
    return KEY_COLOR if letter in UNGUESSED else KEY_USED_COLOR

# skapa skärm
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# -----------------------------------------
# Direkt huvudloop
# -----------------------------------------
if __name__ == "__main__":
    animating = True
    pressed_key = None
    while animating:
        # Rita bakgrund
        screen.blit(background_image, (0, 0))
        
        # --------- Rita kuberna ----------
        y = T_MARGIN
        for i in range(6):
            x = LR_MARGIN
            for j in range(5):
                square = pygame.Rect(x, y, SQ_SIZE, SQ_SIZE)
                pygame.draw.rect(screen, GREY, square, width=2, border_radius=7)
                
                if i < len(GUESSES):
                    color = determine_color(GUESSES[i], j)
                    pygame.draw.rect(screen, color, square, border_radius=7)
                    letter = FONT.render(GUESSES[i][j], False, (255,255,255))
                    surface = letter.get_rect(center=(x+SQ_SIZE//2, y+SQ_SIZE//2))
                    screen.blit(letter, surface)
                
                if i == len(GUESSES) and j < len(INPUT):
                    letter = FONT.render(INPUT[j], False, GREY)
                    surface = letter.get_rect(center=(x+SQ_SIZE//2, y+SQ_SIZE//2))
                    screen.blit(letter, surface)
                    
                x += SQ_SIZE + MARGIN
            y += SQ_SIZE + MARGIN

        # --------- Rita tangentbordet längst ner ----------
        key_rects = []
        start_y = HEIGHT - B_MARGIN - 3*(2*KEY_RADIUS + KEY_SPACING_Y)
        for row_index, row in enumerate(KEYBOARD_LAYOUT):
            row_length = len(row)
            start_x = (WIDTH - (row_length * (2*KEY_RADIUS + KEY_SPACING_X) - KEY_SPACING_X)) // 2
            y = start_y + row_index * (2*KEY_RADIUS + KEY_SPACING_Y)
            
            for i, letter in enumerate(row):
                x = start_x + i * (2*KEY_RADIUS + KEY_SPACING_X)
                circle_rect = pygame.Rect(x, y, 2*KEY_RADIUS, 2*KEY_RADIUS)
                key_rects.append((letter, circle_rect))
                
                color = KEY_PRESSED_COLOR if pressed_key == letter else keyboard_letter_color(letter)
                pygame.draw.ellipse(screen, color, circle_rect)
                
                letter_surface = FONT_SMALL.render(letter, True, LETTER_COLOR)
                letter_rect = letter_surface.get_rect(center=circle_rect.center)
                screen.blit(letter_surface, letter_rect)

        # --------- Rita Enter-knappen separat ----------
        enter_rect = pygame.Rect(WIDTH//2 - 60, HEIGHT - B_MARGIN, 120, 40)
        pygame.draw.rect(screen, KEY_COLOR, enter_rect, border_radius=8)
        enter_surface = FONT_SMALL.render("ENTER", True, LETTER_COLOR)
        enter_rect_text = enter_surface.get_rect(center=enter_rect.center)
        screen.blit(enter_surface, enter_rect_text)

        # --------- Kontrollera game over ----------
        if len(GUESSES) == 6 and GUESSES[5] != ANSWER:
            GAME_OVER = True

        if GAME_OVER:
            letters = FONT.render(ANSWER, False, GREY)
            surface = letters.get_rect(center=(WIDTH//2 , HEIGHT - T_MARGIN//2 - BUTTON_HEIGHT - 930))
            screen.blit(letters, surface)

            button_rect = pygame.Rect((WIDTH - BUTTON_WIDTH)//2, HEIGHT-10 - B_MARGIN//2, BUTTON_WIDTH, BUTTON_HEIGHT)
            pygame.draw.rect(screen, BUTTON_COLOR, button_rect, border_radius=10)
            button_text = BUTTON_FONT.render("Starta Om", True, BUTTON_TEXT_COLOR)
            text_rect = button_text.get_rect(center=button_rect.center)
            screen.blit(button_text, text_rect)

        pygame.display.flip()

        # --------- Händelsehantering ----------
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
                    GAME_OVER = True if INPUT == ANSWER else False
                    INPUT = ""
                elif event.key == pygame.K_SPACE:
                    GAME_OVER = False
                    ANSWER = random.choice(DICT_ANSWERS)
                    GUESSES = []
                    UNGUESSED = ALPHABET
                    INPUT = ""
                elif len(INPUT) < 5 and not GAME_OVER:
                    INPUT += event.unicode.upper()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                if not GAME_OVER:
                    # Klick på bokstäver
                    for letter, rect in key_rects:
                        if rect.collidepoint(mx, my) and len(INPUT) < 5 and letter in UNGUESSED:
                            INPUT += letter
                            pressed_key = letter
                    # Klick på Enter-knappen
                    if enter_rect.collidepoint(mx, my) and len(INPUT) == 5:
                        GUESSES.append(INPUT)
                        UNGUESSED = determine_unguessed_letters(GUESSES)
                        GAME_OVER = True if INPUT == ANSWER else False
                        INPUT = ""
                        pressed_key = "ENTER"

                # Klick på starta om-knapp
                if GAME_OVER and button_rect.collidepoint((mx, my)):
                    ANSWER = random.choice(DICT_ANSWERS)
                    GUESSES = []
                    UNGUESSED = ALPHABET
                    INPUT = ""
                    GAME_OVER = False


