import pygame
import random
import json
import os

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
FONT_NAME = 'Comic Sans MS'
IMAGE_SIZE = (250, 250)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Cybersecurity Quiz')


font = pygame.font.SysFont(FONT_NAME, 28, bold=True)


pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)


background_image = pygame.image.load('background2.png')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))



def draw_background():
    screen.blit(background_image, (0, 0))



def show_start_screen():
    screen.blit(background_image, (0, 0))
    title_font = pygame.font.SysFont(FONT_NAME, 48, bold=True)
    title_surface = title_font.render('Cybersecurity Typing Game', True, WHITE)
    screen.blit(title_surface,
                (WIDTH // 2 - title_surface.get_width() // 2, HEIGHT // 2 - title_surface.get_height() // 2))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                waiting = False



def show_end_screen(score, won):
    screen.blit(background_image, (0, 0))
    end_font = pygame.font.SysFont(FONT_NAME, 48, bold=True)
    if won:
        message = "Congrats! That's all the questions!"
    else:
        message = 'Game Over! Try again by pressing Enter'
    end_surface = end_font.render(message, True, WHITE)
    screen.blit(end_surface,
                (WIDTH // 2 - end_surface.get_width() // 2, HEIGHT // 2 - end_surface.get_height() // 2 - 50))
    score_surface = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_surface,
                (WIDTH // 2 - score_surface.get_width() // 2, HEIGHT // 2 - score_surface.get_height() // 2 + 50))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False



def load_questions():
    with open('questions.json', 'r') as f:
        return json.load(f)


def get_random_questions(questions):
    random.shuffle(questions)
    return questions


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

        # Render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += font_height + line_spacing


        text = text[i:]

    return text


def main_game():
    questions = load_questions()
    questions = get_random_questions(questions)
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


        score_surface = font.render(f'Score: {score}', True, WHITE)
        level_surface = font.render(f'Level: {level}', True, WHITE)
        screen.blit(score_surface, (10, 10))
        screen.blit(level_surface, (WIDTH - 120, 10))  # Adjusted the position to be within bounds


        if question_index < len(questions):
            current_question = questions[question_index]['question']
            if current_question in images:
                question_image = images[current_question]
                screen.blit(question_image, (WIDTH // 2 - question_image.get_width() // 2, HEIGHT // 2 - 350))

            question_rect = pygame.Rect(WIDTH // 4, HEIGHT // 2 - 100, WIDTH // 2, 100)
            draw_text(screen, current_question, WHITE, question_rect, font)
        else:
            show_end_screen(score, won=True)
            main_game()
            break


        input_box = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 50, 300, 32)
        pygame.draw.rect(screen, BLACK, input_box, 2)
        input_surface = font.render(user_input, True, BLACK)
        screen.blit(input_surface, (input_box.x + 5, input_box.y + 2))  # Adjusted the y-coordinate for proper alignment


        if show_feedback:
            feedback_surface = font.render(feedback_message, True, RED if "Incorrect" in feedback_message else GREEN)
            screen.blit(feedback_surface, (WIDTH // 2 - feedback_surface.get_width() // 2, HEIGHT // 2 + 100))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if show_feedback:
                    if event.key == pygame.K_RETURN:
                        show_feedback = False
                        feedback_message = ''
                        user_input = ''
                        question_index += 1
                else:
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
            main_game()
            break

    pygame.quit()
    quit()



while True:
    show_start_screen()
    main_game()
