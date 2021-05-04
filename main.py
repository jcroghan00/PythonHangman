import pygame
import random
import math
import re

pygame.init()

dis_width = 600
dis_height = 400
dis = pygame.display.set_mode((dis_width, dis_height))

pygame.display.update()

pygame.display.set_caption('Hangman')

white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
blue = (50, 153, 213)
green = (0, 255, 0)
yellow = (255, 255, 102)

end_font = pygame.font.SysFont("comicsansms", 30)
hidden_font = pygame.font.SysFont("comicsansms", 40)
letter_font = pygame.font.SysFont("comicsansms", 20)


def choose_word(word_list):
    random_int = random.randrange(0, len(word_list))
    return word_list[random_int]


def read_file(file):
    with open(file) as f:
        return f.readlines()


def check_char(word, char):
    index = [letter.start() for letter in re.finditer(char, word)]
    return index


def hidden_word(word):
    word_hidden = ""
    for char in word:
        word_hidden = word_hidden + "_"
    return word_hidden[0:len(word) - 1]


def reveal_letters(word, word_hidden, index):
    for i in index:
        word_hidden = word_hidden[:i] + word[i] + word_hidden[i + 1:]
    return word_hidden


def add_used_char(used_chars, char):
    if char not in used_chars:
        used_chars.append(char)
        used_chars.sort()
    return used_chars


def message_dynamic(msg, color, font, pos_x, pos_y):
    mesg = font.render(msg, True, color)
    dis.blit(mesg, [pos_x, pos_y])


def message_dynamic_centered(msg, color, font, pos_x, pos_y):
    msg_width, msg_height = font.size(msg)
    mesg = font.render(msg, True, color)
    dis.blit(mesg, [pos_x - msg_width / 2, pos_y - msg_height / 2])


def message_middle(msg, color, font):
    msg_width, msg_height = font.size(msg)
    mesg = font.render(msg, True, color)
    dis.blit(mesg, [dis_width / 2 - msg_width / 2, dis_height / 2 - msg_height / 2])


def print_used_chars(used_chars):
    message_dynamic("Used Letters:", black, letter_font, dis_width - 200, 15)
    i = 0
    for char in used_chars:
        message_dynamic_centered(char, black, letter_font, dis_width - 250 + i, 55)
        i += 15


def render_screen(word_hidden, num_tries, used_chars):
    dis.fill(blue)

    # print game info
    message_dynamic(word_hidden, black, hidden_font, 25, dis_height - 75)
    message_dynamic("Number of tries: " + str(7 - num_tries), black, letter_font, 25, 15)
    print_used_chars(used_chars)

    # draw support
    pygame.draw.line(dis, black, (25, dis_height - 75), (125, dis_height - 75), 4)
    pygame.draw.lines(dis, black, False, [(75, dis_height - 75), (75, dis_height - 275), (100, dis_height - 300), (150, dis_height - 300), (175, dis_height - 275)], 4)

    # draw the man
    if num_tries > 0:
        pygame.draw.circle(dis, yellow, (175, dis_height - 250), 25)
    if num_tries > 1:
        pygame.draw.line(dis, yellow, (175, dis_height - 225), (175, dis_height - 150), 4)
    if num_tries > 2:
        pygame.draw.line(dis, yellow, (175, dis_height - 210), (150, dis_height - 175), 4)
    if num_tries > 3:
        pygame.draw.line(dis, yellow, (175, dis_height - 210), (200, dis_height - 175), 4)
    if num_tries > 4:
        pygame.draw.line(dis, yellow, (175, dis_height - 150), (150, dis_height - 110), 4)
    if num_tries > 5:
        pygame.draw.line(dis, yellow, (175, dis_height - 150), (200, dis_height - 110), 4)
    if num_tries > 6:
        # sad face
        pygame.draw.arc(dis, black, pygame.Rect(150, dis_height - 240, 50, 25), math.pi / 4, (3 * math.pi) / 4, 2)
        pygame.draw.line(dis, black, (165, dis_height - 255), (165, dis_height - 265), 2)
        pygame.draw.line(dis, black, (185, dis_height - 255), (185, dis_height - 265), 2)
    pygame.display.update()


def game_loop():
    game_over = False
    game_close = False

    key_pressed = False

    key = None
    index = None

    num_tries = 0
    used_chars = []

    word_list = read_file("words.txt")
    word = choose_word(word_list)
    word_hidden = hidden_word(word)

    word = word[:len(word) - 1]

    dis.fill(blue)
    render_screen(word_hidden, num_tries, used_chars)
    pygame.display.update()

    while not game_over:
        while game_close:
            message_dynamic("Word: " + word, red, letter_font, dis_width - 175, dis_height - 50)

            if num_tries > 6:
                message_middle("You Lost! Press Q-Quit or C-Play Again", red, end_font)
            if word_hidden == word:
                message_middle("You Won! Press Q-Quit or C-Play Again", green, end_font)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        word = choose_word(word_list)
                        word_hidden = hidden_word(word)
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                key = chr(event.key)
                key_pressed = True
        if key_pressed:
            index = check_char(word, key)
            if len(index) == 0:
                num_tries += 1
            else:
                word_hidden = reveal_letters(word, word_hidden, index)
            used_chars = add_used_char(used_chars, key)
            render_screen(word_hidden, num_tries, used_chars)
            key_pressed = False
        if word_hidden == word or num_tries > 6:
            game_close = True

    pygame.quit()
    quit()


game_loop()
