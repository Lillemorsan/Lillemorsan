# -*- coding: utf-8 -*-
import random
import pygame
import pygbag

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
B_MARGIN = 100
LR_MARGIN = 125

GREY = (70,70,80)
GREEN = (0,160,0)
PURPLE = (100,0,102)

INPUT = ""
GUESSES = []
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"
UNGUESSED = ALPHABET
GAME_OVER = False

pygame.init()
pygame.font.init()
pygame.display.set_caption("Lettro")

SQ_SIZE = (WIDTH-4*MARGIN-2*LR_MARGIN) // 5
FONT = pygame.font.SysFont("free sans bold", SQ_SIZE)
FONT_SMALL = pygame.font.SysFont("free sans bold", SQ_SIZE//2)

# --------- Starta om-knapp ---------
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_COLOR = (0,160,0)
BUTTON_TEXT_COLOR = (255, 255, 255)
BUTTON_FONT = pygame.font.SysFont("free sans bold", 30)

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

# skapa skärm
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# -----------------------------------------
# Direkt huvudloop för pygbag (main.js)
# -----------------------------------------
if __name__ == "__main__":
    animating = True
    while animating:
        screen.fill("white")
        
        # rita ogissade bokstäver på två rader
        split_index = len(UNGUESSED)//3
        letters_top = FONT_SMALL.render(UNGUESSED[:split_index], False, GREY)
        letters_bottom = FONT_SMALL.render(UNGUESSED[split_index:], False, GREY)
        surface_top = letters_top.get_rect(center=(WIDTH//2, T_MARGIN//4))
        surface_bottom = letters_bottom.get_rect(center=(WIDTH//2, T_MARGIN//2))
        screen.blit(letters_top, surface_top)
        screen.blit(letters_bottom, surface_bottom)
        
        # målar kuberna
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

        # kontrollera om spelet är slut efter 6 gissningar
        if len(GUESSES) == 6 and GUESSES[5] != ANSWER:
            GAME_OVER = True

        # ----------- Visa svar och knapp om spelet är slut -----------
        if GAME_OVER:
            # visa rätt ord ovanför knappen
            letters = FONT.render(ANSWER, False, GREY)
            surface = letters.get_rect(center=(WIDTH//2, HEIGHT - B_MARGIN//2 - BUTTON_HEIGHT - 30))
            screen.blit(letters, surface)

            # rita starta om-knappen
            button_rect = pygame.Rect((WIDTH - BUTTON_WIDTH)//2, HEIGHT - B_MARGIN//2, BUTTON_WIDTH, BUTTON_HEIGHT)
            pygame.draw.rect(screen, BUTTON_COLOR, button_rect, border_radius=10)

            button_text = BUTTON_FONT.render("Köra igen?!?", True, BUTTON_TEXT_COLOR)
            text_rect = button_text.get_rect(center=button_rect.center)
            screen.blit(button_text, text_rect)
        
        # uppdaterar skärmen
        pygame.display.flip()
        
        # spåra användar interactions
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                animating = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    animating = False
                if event.key == pygame.K_BACKSPACE:
                    if len(INPUT) > 0:
                        INPUT = INPUT[:-1]
                elif event.key == pygame.K_RETURN:
                    if len(INPUT) == 5 and INPUT:
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
            # ---------- Klick på starta om-knapp ----------
            elif event.type == pygame.MOUSEBUTTONDOWN and GAME_OVER:
                if button_rect.collidepoint(event.pos):
                    ANSWER = random.choice(DICT_ANSWERS)
                    GUESSES = []
                    UNGUESSED = ALPHABET
                    INPUT = ""
                    GAME_OVER = False
