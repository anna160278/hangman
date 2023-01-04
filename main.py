import random, sys, pygame, math

# setup display
pygame.init()
WIDTH, HEIGHT = 800, 550
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Hangman Game!")

# button variables
RADIUS = 20  # радиус кнопок для букв алфавита
GAP = 15  # промежуток между буквами
letters = []
startx = round((WIDTH - (RADIUS * 2 + GAP) * 11) / 2)
starty = 400
A = ord('А')
for i in range(32):
    x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 11))
    y = starty + ((i // 11) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

# fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 26)
WORD_FONT = pygame.font.SysFont('comicsans', 40)
TITLE_FONT = pygame.font.SysFont('comicsans', 40)

# load images.
images = []
for i in range(7):
    image = pygame.image.load("hangman" + str(i) + ".png")
    images.append(image)
bg = pygame.image.load('bg2.png')

# game variables
hangman_status = 0
words = ["КАРАНДАШ", "СОБАКА", "ЗЕМЛЯ", "КОМПЬЮТЕР", "ПРОГРАММА", "КЛАВИАТУРА", "ВИСЕЛИЦА", "МАТЕМАТИКА", "ТЕЛЕФОН",
         "СЛОВО", "КОШКА", "ИЗОБРЕТЕНИЕ", "ПРАЗДНИК", "ШКОЛА", "ЯБЛОКО", "АПЕЛЬСИН", "ПОДАРОК", "ШОКОЛАД"]
word = random.choice(words)
guessed = []
run = True

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (245, 227, 66)
BLUE = (28, 153, 220)


def draw():
    win.fill(WHITE)
    # win.blit(bg, (0, 0))
    # draw title
    text = TITLE_FONT.render("игра ВИСЕЛИЦА", True, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, 20))

    # draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, True, BLACK, YELLOW)
    win.blit(text, (400, 200))

    # draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, YELLOW, (x, y), RADIUS)
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 2)
            text = LETTER_FONT.render(ltr, True, BLACK)
            win.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

    win.blit(images[hangman_status], (120, 100))
    pygame.display.update()


def display_message(message):
    pygame.time.delay(1000)
    win.fill(YELLOW)
    text = WORD_FONT.render(message, True, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(2000)


def restart():
    global hangman_status, guessed, word, run
    hangman_status = 0
    guessed = []
    word = random.choice(words)
    run = True
    for letter in letters:
        letter[3] = True


def main():
    global hangman_status, run

    FPS = 60
    clock = pygame.time.Clock()
    # run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    print("R")
                    restart()

            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)
                        if dis < RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1

        draw()

        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break

        if won:
            display_message("Ты выиграл!")
            display_message('Сыграем ещё? Нажми R')
            break

        if hangman_status == 6:
            display_message("Ты проиграл!")
            display_message(f"загаданное слово: {word}")
            display_message('Сыграем ещё? Нажми R')
            break


while True:
    main()
    # sys.exit()
