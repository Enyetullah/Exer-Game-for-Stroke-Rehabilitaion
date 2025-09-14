import pygame
import random
import pandas as pd
import sys
import cv2
import mediapipe as mp
import time
import os
import json

# ---------------------------
# Constants
# ---------------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ball_radius = 20
ball_speed = 5
cup_width = 100
cup_height = 100
max_trials = 10

# ---------------------------
# Main game function
# ---------------------------
def run_game(user_name, difficulty, screen_width, screen_height, game_type):

    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("D:/TruScholars Project/src/music/the-return-of-the-8-bit-era-301292.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    catch_sound = pygame.mixer.Sound("D:/TruScholars Project/src/music/mixkit-game-ball-tap-2073.wav")
    catch_sound.set_volume(0.7)

    bounce_sound = pygame.mixer.Sound("D:/TruScholars Project/src/music/mixkit-ball-bouncing-in-the-ground-2077.wav")
    bounce_sound.set_volume(1.0)

    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    pygame.display.set_caption("Stroke Rehab Catch Game")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    large_font = pygame.font.SysFont(None, 48)

    # Load images
    cup_image = pygame.image.load("D:/TruScholars Project/src/images/cup.png")
    cup_image = pygame.transform.scale(cup_image, (cup_width, cup_height))
    background = pygame.image.load("D:/TruScholars Project/src/images/background.png")
    background = pygame.transform.scale(background, (screen_width, screen_height))

    # MediaPipe setup
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)
    cap = cv2.VideoCapture(0)

    # History file path
    user_folder = os.path.join("data", user_name)
    os.makedirs(user_folder, exist_ok=True)
    history_file = os.path.join(user_folder, f"{game_type}_history.json")

    # Load existing history
    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            history = json.load(f)
    else:
        history = []

    # Game state
    cup_x = screen_width // 2 - cup_width // 2
    cup_y = screen_height - 60
    game_logs = []
    success_count = 0
    count = 0
    waiting_for_next = False

    def get_zone(ball_x):
        if ball_x < screen_width // 3:
            return "left"
        elif ball_x < 2 * screen_width // 3:
            return "center"
        else:
            return "right"

    def reset_ball():
        spawn_x = random.randint(0, screen_width - ball_radius)
        spawn_y = 0
        angle_x = random.uniform(-2.5, 2.5) * difficulty
        angle_y = ball_speed * difficulty
        return [spawn_x, spawn_y], [angle_x, angle_y]

    ball_pos, ball_vel = reset_ball()
    running = True

    while running:
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    return
                if waiting_for_next and event.key == pygame.K_RETURN:
                    count = 0
                    success_count = 0
                    game_logs = []
                    ball_pos, ball_vel = reset_ball()
                    cup_x = screen_width // 2 - cup_width // 2
                    waiting_for_next = False
            elif event.type == pygame.VIDEORESIZE:
                screen_width, screen_height = event.w, event.h
                screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
                background = pygame.transform.scale(background, (screen_width, screen_height))
                cup_y = screen_height - 60

        ret, frame = cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb_frame)
            if result.multi_hand_landmarks:
                hand_landmarks = result.multi_hand_landmarks[0]
                index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                cup_x = int(index_finger.x * screen_width) - cup_width // 2

        if not waiting_for_next:
            cup_x = max(0, min(cup_x, screen_width - cup_width))
            ball_pos[0] += ball_vel[0]
            ball_pos[1] += ball_vel[1]

            if ball_pos[0] <= ball_radius or ball_pos[0] >= screen_width - ball_radius:
                ball_vel[0] = -ball_vel[0]
                bounce_sound.play()
            ball_pos[0] = max(ball_radius, min(ball_pos[0], screen_width - ball_radius))

            pygame.draw.circle(screen, RED, ball_pos, ball_radius)
            screen.blit(cup_image, (cup_x, cup_y))

            zone_label = get_zone(ball_pos[0])
            zone_text = font.render(f"Zone: {zone_label}", True, BLACK)
            screen.blit(zone_text, (10, 50))

            if (cup_y <= ball_pos[1] + ball_radius <= cup_y + cup_height and
                cup_x <= ball_pos[0] <= cup_x + cup_width):
                success = 1
                success_count += 1
                count += 1
                catch_sound.play()
                game_logs.append({
                    "timestamp": time.time(),
                    "trial": count,
                    "ball_x": ball_pos[0],
                    "cup_x": cup_x,
                    "zone": zone_label,
                    "success": success,
                    "difficulty": difficulty,
                    "game_type": game_type
                })
                ball_pos, ball_vel = reset_ball()

            elif ball_pos[1] > screen_height:
                success = 0
                count += 1
                game_logs.append({
                    "timestamp": time.time(),
                    "trial": count,
                    "ball_x": ball_pos[0],
                    "cup_x": cup_x,
                    "zone": zone_label,
                    "success": success,
                    "difficulty": difficulty,
                    "game_type": game_type
                })
                ball_pos, ball_vel = reset_ball()

            score_text = font.render(f"Score: {success_count}/{count}", True, BLACK)
            screen.blit(score_text, (10, 10))

            if count >= max_trials:
                os.makedirs(user_folder, exist_ok=True)
                filename = os.path.join(user_folder, f"session_{game_type}_{int(time.time())}.csv")
                pd.DataFrame(game_logs).to_csv(filename, index=False)

                session_result = ['S' if log["success"] else 'F' for log in game_logs[-max_trials:]]
                history.append(session_result)
                if len(history) > 5:
                    history.pop(0)
                with open(history_file, "w") as f:
                    json.dump(history, f)

                successful_tries = sum([log["success"] for log in game_logs[-max_trials:]])
                if successful_tries >= 7:
                    difficulty += 1
                    level_result = "Level Up!"
                elif successful_tries < 5 and difficulty > 1:
                    difficulty -= 1
                    level_result = "Level Down"
                else:
                    level_result = "Try Again to Level Up"
                waiting_for_next = True

        else:
            result_text = large_font.render(f"Final Score: {success_count}/{max_trials}", True, BLACK)
            level_text = font.render(level_result, True, GREEN if "Up" in level_result else RED)
            prompt_text = font.render("Press ENTER to start next level", True, BLACK)
            back_text = font.render("Press ESC to go back to the difficulty selection menu", True, BLACK)
            screen.blit(result_text, (screen_width // 2 - result_text.get_width() // 2, screen_height // 3))
            screen.blit(level_text, (screen_width // 2 - level_text.get_width() // 2, screen_height // 3 + 50))
            screen.blit(prompt_text, (screen_width // 2 - prompt_text.get_width() // 2, screen_height // 3 + 100))
            screen.blit(back_text, (screen_width // 2 - back_text.get_width() // 2, screen_height // 3 + 150))

            # Display history
            history_start_y = screen_height * 0.66
            line_height = 35

            history_title = font.render("Last 5 Sessions:", True, RED)
            screen.blit(history_title, (50, history_start_y))

            for i, session in enumerate(history[-5:]):
                summary = " ".join(session)
                session_text = font.render(f"Session {i+1}: {summary}", True, GREEN)
                screen.blit(session_text, (50, history_start_y + (i + 1) * line_height))

        pygame.display.flip()
        clock.tick(60)

    cap.release()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    run_game("TestUser", 1, 800, 600, "diagonal_random")
