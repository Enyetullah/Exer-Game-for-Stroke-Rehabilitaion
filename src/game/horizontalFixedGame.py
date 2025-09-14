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
ball_speed = 4
cup_width = 100
cup_height = 100
max_trials = 10

LEVEL_BALL_POSITIONS = {
    1: [0.3, 0.01, 1.0, 0.1, 0.3, 0.8, 1.0, 0.35, 0.85, 0.25],
    2: [0.3, 0.6, 0.2, 0.8, 0.5, 0.6, 0.14, 1.0, 0.85, 0.55],
    3: [0.15, 0.32, 0.15, 1.0, 0.75, 0.01, 0.45, 0.4, 0.25, 0.3],
    4: [0.205, 0.1, 0.4, 0.8, 0.2, 0.05, 0.3, 0.5, 0.85, 0.35],
    5: [0.25, 0.85, 0.35, 0.12, 0.85, 0.06, 0.15, 0.4, 0.65, 1.0],
}

def run_game(user_name, difficulty, screen_width, screen_height):
    game_type = "horizontal_fixed"

    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("D:/TruScholars Project/src/music/the-return-of-the-8-bit-era-301292.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    catch_sound = pygame.mixer.Sound("D:/TruScholars Project/src/music/mixkit-game-ball-tap-2073.wav")
    catch_sound.set_volume(0.7)

    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    pygame.display.set_caption("Stroke Rehab Catch Game")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    large_font = pygame.font.SysFont(None, 48)

    cup_image = pygame.image.load("D:/TruScholars Project/src/images/cup.png")
    cup_image = pygame.transform.scale(cup_image, (cup_width, cup_height))
    background = pygame.image.load("D:/TruScholars Project/src/images/background.png")
    background = pygame.transform.scale(background, (screen_width, screen_height))

    # Load healthy benchmark scores
    benchmark_file = os.path.join("data", "benchmark", "healthy_benchmarks.json")
    healthy_benchmark_score = None

    if os.path.exists(benchmark_file):
        with open(benchmark_file, "r") as f:
            benchmark_data = json.load(f)
            healthy_benchmark_score = benchmark_data.get(game_type, {}).get(str(difficulty))

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)
    cap = cv2.VideoCapture(0)

    user_folder = os.path.join("data", user_name)
    os.makedirs(user_folder, exist_ok=True)
    history_file = os.path.join(user_folder, f"{game_type}_history.json")
    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            history = json.load(f)
    else:
        history = []

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

    def reset_ball(trial_index, current_level):
        positions = LEVEL_BALL_POSITIONS.get(current_level, [0.5] * max_trials)
        x_percent = positions[trial_index] if trial_index < len(positions) else 0.5
        x_pos = int(x_percent * screen_width)
        return [x_pos, 0]

    ball_pos = reset_ball(count, difficulty)
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
                    ball_pos = reset_ball(count, difficulty)
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
                index_finger = result.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                cup_x = int(index_finger.x * screen_width) - cup_width // 2

        if not waiting_for_next:
            cup_x = max(0, min(cup_x, screen_width - cup_width))
            ball_pos[1] += ball_speed * difficulty
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
                ball_pos = reset_ball(count, difficulty)

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
                ball_pos = reset_ball(count, difficulty)

            score_text = font.render(f"Score: {success_count}/{count}", True, BLACK)
            screen.blit(score_text, (10, 10))

            if count >= max_trials:
                filename = os.path.join(user_folder, f"session_{game_type}_{int(time.time())}.csv")
                pd.DataFrame(game_logs).to_csv(filename, index=False)
                session_result = ['S' if g['success'] else 'F' for g in game_logs[-max_trials:]]
                history.append(session_result)
                if len(history) > 5:
                    history.pop(0)
                with open(history_file, "w") as f:
                    json.dump(history, f)

                successful_tries = sum(g['success'] for g in game_logs[-max_trials:])
                if successful_tries >= 7:
                    if difficulty < 5:
                        difficulty += 1
                        level_result = "Level Up!"
                    else:
                        level_result = "Level 5 Complete! Replaying Level 5"
                elif successful_tries < 5 and difficulty > 1:
                    difficulty -= 1
                    level_result = "Level Down"
                else:
                    level_result = "Try Again to Level Up"
                waiting_for_next = True

        else:
            # Move text higher on the screen using y_base
            y_base = screen_height // 4  # Instead of screen_height // 3

            result_text = large_font.render(f"Final Score: {success_count}/{max_trials}", True, BLACK)
            level_text = font.render(level_result, True, GREEN if "Up" in level_result else RED)
            prompt_text = font.render("Press ENTER to start next level", True, BLACK)
            back_text = font.render("Press ESC to go back to the difficulty selection menu", True, BLACK)

            screen.blit(result_text, (screen_width // 2 - result_text.get_width() // 2, y_base))
            screen.blit(level_text, (screen_width // 2 - level_text.get_width() // 2, y_base + 40))
            screen.blit(prompt_text, (screen_width // 2 - prompt_text.get_width() // 2, y_base + 80))
            screen.blit(back_text, (screen_width // 2 - back_text.get_width() // 2, y_base + 120))

            history_start_y = screen_height * 0.66
            line_height = 35
            history_title = font.render("Last 5 Sessions:", True, RED)
            screen.blit(history_title, (50, history_start_y))

            for i, session in enumerate(history[-5:]):
                summary = " ".join(session)
                session_text = font.render(f"Session {i+1}: {summary}", True, GREEN)
                screen.blit(session_text, (50, history_start_y + (i + 1) * line_height))

            # Benchmark display moved higher using same y_base
            if healthy_benchmark_score is not None:
                benchmark_text = font.render(
                    f"Avg Healthy Score: {healthy_benchmark_score}/10", True, BLACK
                )
                comparison = "You met the benchmark!" if success_count >= healthy_benchmark_score else "Try to improve!"
                comparison_text = font.render(comparison, True, GREEN if success_count >= healthy_benchmark_score else RED)

                screen.blit(benchmark_text, (screen_width // 2 - benchmark_text.get_width() // 2, y_base + 160))
                screen.blit(comparison_text, (screen_width // 2 - comparison_text.get_width() // 2, y_base + 200))

        pygame.display.flip()
        clock.tick(60)

    cap.release()
    pygame.quit()
    sys.exit()
