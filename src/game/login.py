import pygame
import sys
import os

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)

def show_user_login(screen, screen_width, screen_height, font, large_font, login_background):
    user_name = ""
    input_active = True
    color_active = pygame.Color('dodgerblue')
    color_inactive = pygame.Color('gray15')
    color = color_inactive

    input_box_width = 300
    input_box_height = 50

    entering = True
    while entering:
        # 🟢 SCALE AND DRAW BACKGROUND
        resized_background = pygame.transform.scale(login_background, (screen_width, screen_height))
        screen.blit(resized_background, (0, 0))

        # 🟢 Overlay to make text stand out
        overlay_width = min(screen_width * 0.8, 500)
        overlay_height = min(screen_height * 0.6, 400)
        overlay_rect = pygame.Surface((overlay_width, overlay_height), pygame.SRCALPHA)
        overlay_rect.fill((255, 255, 255, 150))
        screen.blit(overlay_rect, (
            screen_width // 2 - overlay_width // 2,
            screen_height // 2 - overlay_height // 2
        ))

        # 🟢 Center the input box
        input_box = pygame.Rect(
            screen_width // 2 - input_box_width // 2,
            screen_height // 2 - 40,
            input_box_width,
            input_box_height
        )

        # 🟢 Draw title
        title = large_font.render("Enter Your Name", True, (0, 0, 0))
        screen.blit(title, (
            screen_width // 2 - title.get_width() // 2,
            screen_height // 2 - overlay_height // 2 + 30
        ))

        # 🟢 Render input text
        font_input = pygame.font.Font(None, 40)
        txt_surface = font_input.render(user_name, True, (0, 0, 0))
        input_box.w = max(300, txt_surface.get_width() + 10)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 10))
        pygame.draw.rect(screen, color, input_box, 2)

        # 🟢 Draw buttons below input
        button_spacing = 20
        button_width = 140
        button_height = 40
        login_button_rect = pygame.Rect(
            screen_width // 2 - button_spacing - button_width,
            input_box.y + input_box_height + 30,
            button_width,
            button_height
        )
        new_button_rect = pygame.Rect(
            screen_width // 2 + button_spacing,
            input_box.y + input_box_height + 30,
            button_width,
            button_height
        )

        # 🟢 Draw button text
        login_label = font.render("Login", True, (0, 0, 0))
        new_label = font.render("New User", True, (0, 0, 0))
        pygame.draw.rect(screen, GREEN, login_button_rect)
        pygame.draw.rect(screen, RED, new_button_rect)
        screen.blit(login_label, (login_button_rect.centerx - login_label.get_width() // 2, login_button_rect.centery - login_label.get_height() // 2))
        screen.blit(new_label, (new_button_rect.centerx - new_label.get_width() // 2, new_button_rect.centery - new_label.get_height() // 2))

        pygame.display.flip()

        # 🟢 Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.VIDEORESIZE:
                screen_width, screen_height = event.w, event.h
                screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    input_active = True
                    color = color_active
                else:
                    input_active = False
                    color = color_inactive

                if login_button_rect.collidepoint(event.pos):
                    if user_name.strip():
                        user_path = os.path.join("data", user_name)
                        if os.path.exists(user_path):
                            entering = False
                        else:
                            print("User does not exist.")
                    else:
                        print("Please enter a name.")
                elif new_button_rect.collidepoint(event.pos):
                    if user_name.strip():
                        user_path = os.path.join("data", user_name)
                        os.makedirs(user_path, exist_ok=True)
                        entering = False
                    else:
                        print("Please enter a name.")

            elif event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_RETURN:
                    pass
                elif event.key == pygame.K_BACKSPACE:
                    user_name = user_name[:-1]
                else:
                    user_name += event.unicode

    return user_name
