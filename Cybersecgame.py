import pygame
import random
import json
import os


pygame.init()


WIDTH, HEIGHT = 1000, 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
FONT_NAME = 'Comic Sans MS'
IMAGE_SIZE = (350, 250)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Cybersecurity Quiz')

font = pygame.font.SysFont(FONT_NAME, 28, bold=True)

pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

background_image = pygame.image.load('background2.png')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

def draw_background():
    screen.blit(background_image, (0, 0))

def render_text(surface, text, font, color, position, center=False):
    text_surface = font.render(text, True, color)
    if center:
        position = (position[0] - text_surface.get_width() // 2, position[1] - text_surface.get_height() // 2)
    surface.blit(text_surface, position)
    return text_surface.get_rect(topleft=position)

def show_start_screen():
    draw_background()
    render_text(screen, 'Cybersecurity Typing Game', pygame.font.SysFont(FONT_NAME, 48, bold=True), WHITE, (WIDTH // 2, HEIGHT // 2), center=True)
    options = ["5", "15", "25"]
    for i, option in enumerate(options):
        render_text(screen, f'Press {i + 1} to select {option} questions', pygame.font.SysFont(FONT_NAME, 36, bold=True), WHITE, (WIDTH // 2, HEIGHT // 2 + 100 + i * 50), center=True)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                    return int(options[event.key - pygame.K_1])

def show_end_screen(score, won):
    draw_background()
    end_message = "Congrats! That's all the questions!" if won else 'Game Over! Try again by pressing Enter'
    render_text(screen, end_message, pygame.font.SysFont(FONT_NAME, 48, bold=True), WHITE, (WIDTH // 2, HEIGHT // 2 - 50), center=True)
    render_text(screen, f'Score: {score}', font, WHITE, (WIDTH // 2, HEIGHT // 2 + 50), center=True)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

def load_questions():
    with open('questions.json', 'r') as f:
        return json.load(f)

def get_random_questions(questions, count):
    random.shuffle(questions)
    return questions[:count]

def load_images(questions):
    images = {}
    for question in questions:
        image_path = question['image']
        if os.path.exists(image_path):
            images[question['question']] = pygame.transform.scale(pygame.image.load(image_path), IMAGE_SIZE)
    return images

def draw_text(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    line_spacing = -2

    font_height = font.size("Tg")[1]

    while text:
        i = 1

        if y + font_height > rect.bottom:
            break

        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += font_height + line_spacing

        text = text[i:]

    return text

def main_game(question_count):
    questions = load_questions()
    questions = get_random_questions(questions, question_count)
    images = load_images(questions)

    score = 0
    incorrect_count = 0
    level = 1
    question_index = 0
    user_input = ''
    feedback_message = ''
    show_feedback = False

    running = True
    while running:
        draw_background()

        render_text(screen, f'Score: {score}', font, WHITE, (10, 10))
        render_text(screen, f'Level: {level}', font, WHITE, (WIDTH - 120, 10))

        if question_index < len(questions):
            current_question = questions[question_index]['question']
            if current_question in images:
                screen.blit(images[current_question], (WIDTH // 2 - images[current_question].get_width() // 2, HEIGHT // 2 - 350))
            draw_text(screen, current_question, WHITE, pygame.Rect(WIDTH // 4, HEIGHT // 2 - 100, WIDTH // 2, 100), font)
        else:
            show_end_screen(score, won=True)
            return

        input_box = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 50, 300, 32)
        pygame.draw.rect(screen, BLACK, input_box, 2)
        render_text(screen, user_input, font, BLACK, (input_box.x + 5, input_box.y + 2))

        if show_feedback:
            render_text(screen, feedback_message, font, RED if "Incorrect" in feedback_message else GREEN, (WIDTH // 2, HEIGHT // 2 + 100), center=True)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if show_feedback and event.key == pygame.K_RETURN:
                    show_feedback = False
                    feedback_message = ''
                    user_input = ''
                    question_index += 1
                elif not show_feedback:
                    if event.key == pygame.K_RETURN:
                        if question_index < len(questions):
                            correct_answer = questions[question_index]['answer']
                            if user_input.lower() == correct_answer.lower():
                                score += 10
                                feedback_message = 'Correct!'
                                if score % 50 == 0:
                                    level += 1
                            else:
                                incorrect_count += 1
                                feedback_message = f'Incorrect! The correct answer was: {correct_answer}'
                                if score > 0:
                                    score -= 10
                            show_feedback = True
                    elif event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    else:
                        user_input += event.unicode

        if incorrect_count >= 5:
            show_end_screen(score, won=False)
            return

    pygame.quit()
    quit()

while True:
    question_count = show_start_screen()
    main_game(question_count)
