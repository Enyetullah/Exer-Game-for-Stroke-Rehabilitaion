import pygame
import sys
from login import show_user_login
# Import your different game modes
import horizontalRandomGame
import verticalRandomgame
import diagonalRandomGame
import horizontalFixedGame
import verticalFixedGame
import diagonalFixedGame

# ---------------------------
# Init Pygame
# ---------------------------
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Stroke Rehab Catch Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)
large_font = pygame.font.SysFont(None, 36)

# Load background images
difficulty_background = pygame.image.load("D:/TruScholars Project/src/images/diffuclty_background.jpg")
difficulty_background = pygame.transform.scale(difficulty_background, (screen_width, screen_height))

mode_background = pygame.image.load("D:/TruScholars Project/src/images/mode.jpg")
mode_background = pygame.transform.scale(mode_background, (screen_width, screen_height))

login_background = pygame.image.load("D:/TruScholars Project/src/images/login.png")
login_background = pygame.transform.scale(login_background, (screen_width, screen_height))

# ---------------------------
# Mode Selection Menu
# ---------------------------
def show_mode_selection(screen, screen_width, screen_height, font, large_font, mode_background):
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    selecting = True
    selected_mode = None

    modes = [
        "Horizontal Random Game",
        "Vertical Random Game",
        "Diagonal Random Game",
        "Horizontal Workout",
        "Vertical Workout",
        "Diagonal Workout"
    ]

    while selecting:
        # Draw scaled background
        resized_background = pygame.transform.scale(mode_background, (screen_width, screen_height))
        screen.blit(resized_background, (0, 0))

        # Semi-transparent overlay
        overlay_width = min(500, screen_width * 0.8)
        overlay_height = min(500, screen_height * 0.8)
        overlay_rect = pygame.Surface((overlay_width, overlay_height), pygame.SRCALPHA)
        overlay_rect.fill((255, 255, 255, 150))
        screen.blit(overlay_rect, (
            screen_width // 2 - overlay_width // 2,
            screen_height // 2 - overlay_height // 2
        ))

        # Title
        title = large_font.render("Select Game Mode (ESC to go back)", True, (0, 0, 0))
        screen.blit(title, (
            screen_width // 2 - title.get_width() // 2,
            screen_height // 2 - overlay_height // 2 + 30
        ))

        # Menu Options
        for i, mode in enumerate(modes):
            label = font.render(f"{i+1}. {mode}", True, (0, 0, 0))
            y_pos = screen_height // 2 - overlay_height // 2 + 100 + i * 50
            screen.blit(label, (screen_width // 2 - label.get_width() // 2, y_pos))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_6:
                    selected_mode = modes[event.key - pygame.K_1]
                    selecting = False
                elif event.key == pygame.K_ESCAPE:
                    return "BACK", screen_width, screen_height
            elif event.type == pygame.VIDEORESIZE:
                screen_width, screen_height = event.w, event.h
                screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

    return selected_mode, screen_width, screen_height

# ---------------------------
# Difficulty Selection Menu
# ---------------------------
def show_difficulty_menu(screen, screen_width, screen_height, font, large_font, difficulty_background):
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    selecting = True
    selected_difficulty = 1

    while selecting:
        resized_background = pygame.transform.scale(difficulty_background, (screen_width, screen_height))
        screen.blit(resized_background, (0, 0))

        overlay_width = min(500, screen_width * 0.8)
        overlay_height = min(400, screen_height * 0.8)
        overlay_rect = pygame.Surface((overlay_width, overlay_height), pygame.SRCALPHA)
        overlay_rect.fill((255, 255, 255, 150))
        screen.blit(overlay_rect, (
            screen_width // 2 - overlay_width // 2,
            screen_height // 2 - overlay_height // 2
        ))

        title = large_font.render("Choose Your Difficulty (ESC to go back)", True, (0, 0, 0))
        screen.blit(title, (
            screen_width // 2 - title.get_width() // 2,
            screen_height // 2 - overlay_height // 2 + 30
        ))

        for i in range(1, 6):
            label = font.render(f"Level {i}", True, (0, 0, 0))
            y_pos = screen_height // 2 - overlay_height // 2 + 100 + (i - 1) * 50
            screen.blit(label, (screen_width // 2 - label.get_width() // 2, y_pos))

        tip = font.render("Press 1-5 to select", True, (100, 0, 0))
        screen.blit(tip, (screen_width // 2 - tip.get_width() // 2, screen_height // 2 + overlay_height // 2 - 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_5:
                    selected_difficulty = event.key - pygame.K_0
                    selecting = False
                elif event.key == pygame.K_ESCAPE:
                    return "BACK", screen_width, screen_height
            elif event.type == pygame.VIDEORESIZE:
                screen_width, screen_height = event.w, event.h
                screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

    return selected_difficulty, screen_width, screen_height

# ---------------------------
# App Flow
# ---------------------------
while True:
    # 1️⃣ Login
    screen_width, screen_height = screen.get_size()
    user_name = show_user_login(screen, screen_width, screen_height, font, large_font, login_background)


    while True:
        screen_width, screen_height = screen.get_size()
        mode_result = show_mode_selection(screen, screen_width, screen_height, font, large_font, mode_background)
        if mode_result[0] == "BACK":
            break
        selected_mode, screen_width, screen_height = mode_result

        while True:
            screen_width, screen_height = screen.get_size()
            difficulty_result = show_difficulty_menu(
                screen, screen_width, screen_height, font, large_font, difficulty_background
            )
            if difficulty_result[0] == "BACK":
                break
            difficulty, screen_width, screen_height = difficulty_result

            # 4️⃣ Start Correct Game
            if selected_mode == "Horizontal Random Game":
                horizontalRandomGame.run_game(user_name, difficulty, screen_width, screen_height, "horizontal_random")
            elif selected_mode == "Vertical Random Game":
                verticalRandomgame.run_game(user_name, difficulty, screen_width, screen_height, "vertical_random")
            elif selected_mode == "Diagonal Random Game":
                diagonalRandomGame.run_game(user_name, difficulty, screen_width, screen_height, "diagonal_random")
            elif selected_mode == "Horizontal Workout":
                horizontalFixedGame.run_game(user_name, difficulty, screen_width, screen_height)
            elif selected_mode == "Vertical Workout":
                verticalFixedGame.run_game(user_name, difficulty, screen_width, screen_height)
            elif selected_mode == "Diagonal Workout":
                diagonalFixedGame.run_game(user_name, difficulty, screen_width, screen_height)
