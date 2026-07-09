"""
Week 6 - Gesture Controlled Snake Game
-----------------------------------------
Takes the keyboard Snake game from Week 5 and swaps the arrow-key input
for gesture input, using my own HandTrackingModule.py (Week 3/4) and the
new game_gestures.py classifier instead of the raw MediaPipe Tasks API
shown in the course reference. Everything about the game loop, movement,
collision, and rendering is unchanged from Week 5 -- only *where*
`direction` comes from has changed.

Approach used: Merged Single Loop (webcam read -> gesture detect -> game
update -> render), all inside one while loop, same as recommended for a
slow-paced game like Snake.

Gesture -> Action map:
    FIST         -> start game / restart after game over
    OPEN PALM    -> pause (point in any direction to resume)
    POINT UP     -> move up
    POINT DOWN   -> move down
    POINT LEFT   -> move left
    POINT RIGHT  -> move right

Keyboard is kept as a backup/debug control (arrows, P, G, +/-, Q) in case
the camera misbehaves mid-testing -- doesn't interfere with gestures,
since both paths just set the same `direction` / `is_paused` variables.

Requires (same folder): HandTrackingModule.py, game_gestures.py
"""

import cv2 as cv
import pygame
import random
import sys
import os

import HandTrackingModule as htm
import game_gestures

# =====================================================================
# 1. CONFIGURATION
# =====================================================================

CELL_SIZE = 30
GRID_WIDTH = 30
GRID_HEIGHT = 22
WIDTH = CELL_SIZE * GRID_WIDTH
HEIGHT = CELL_SIZE * GRID_HEIGHT

BG_COLOR   = (15, 15, 25)
SNAKE_HEAD = (0, 230, 120)
SNAKE_BODY = (0, 170, 90)
FOOD_COLOR = (240, 70, 90)
TEXT_COLOR = (235, 235, 245)
GRID_COLOR = (30, 30, 45)
GOLD       = (255, 215, 0)

HIGH_SCORE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "highscore.txt")

STABILITY_FRAMES = 4   # a gesture must repeat this many consecutive frames to be trusted


# =====================================================================
# 2. HELPERS
# =====================================================================

def random_food(snake):
    while True:
        pos = (random.randint(2, GRID_WIDTH - 3), random.randint(2, GRID_HEIGHT - 3))
        if pos not in snake:
            return pos


def draw_cell(surface, pos, color):
    x = pos[0] * CELL_SIZE
    y = pos[1] * CELL_SIZE
    rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(surface, color, rect)
    pygame.draw.rect(surface, BG_COLOR, rect, 1)


def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            with open(HIGH_SCORE_FILE, "r") as f:
                return int(f.read().strip())
        except (ValueError, OSError):
            return 0
    return 0


def save_high_score(value):
    try:
        with open(HIGH_SCORE_FILE, "w") as f:
            f.write(str(value))
    except OSError:
        pass


# =====================================================================
# 3. MAIN GAME
# =====================================================================

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Gesture Controlled Snake - Week 6")
    font = pygame.font.SysFont("consolas", 22)
    big_font = pygame.font.SysFont("consolas", 40, bold=True)

    cap = cv.VideoCapture(0)
    detector = htm.handDetector(detectionCon=0.7, maxHands=1)

    def reset_game():
        start = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        return [start], (1, 0), random_food([start]), 0

    snake, direction, food, score = reset_game()
    game_over = False
    is_paused = False
    game_started = False
    show_grid = True
    high_score = load_high_score()

    MOVE_DELAY_START = 150     # a bit slower start than Week 5's keyboard version,
    MOVE_DELAY_MIN = 80        # since webcam-driven input has a ~4-frame stability delay
    SPEED_STEP = 5
    MANUAL_SPEED_STEP = 10
    MOVE_DELAY = MOVE_DELAY_START
    last_move_time = pygame.time.get_ticks()

    # --- gesture stability filter state ---
    stable_gesture = "NONE"
    previous_gesture = "NONE"
    gesture_counter = 0

    while True:
        # -----------------------------------------------------------
        # PHASE 1: WEBCAM CAPTURE + GESTURE DETECTION (runs at webcam speed)
        # -----------------------------------------------------------
        success, frame = cap.read()
        if not success:
            print("Camera not found")
            break

        frame = cv.flip(frame, 1)                      # mirror, feels natural
        frame = detector.findHands(frame)
        lmlist = detector.findPosition(frame, draw=False)

        gesture = "NONE"
        if len(lmlist) != 0:
            handLabel = detector.findHandLabel()
            gesture = game_gestures.classifyDirectional(lmlist, handLabel)

        # stability filter: only trust a gesture after STABILITY_FRAMES
        # consecutive matching frames, otherwise brief mid-transition
        # poses (e.g. passing through POINT LEFT while going from POINT
        # DOWN to POINT RIGHT) would yank the snake around randomly
        if gesture == previous_gesture:
            gesture_counter += 1
        else:
            gesture_counter = 1
            previous_gesture = gesture

        if gesture_counter >= STABILITY_FRAMES:
            stable_gesture = gesture

        # -----------------------------------------------------------
        # PHASE 2: EVENTS - gestures drive the game, keyboard is a backup
        # -----------------------------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    cap.release()
                    pygame.quit()
                    sys.exit()

                if not game_started:
                    if event.key == pygame.K_SPACE:
                        game_started = True
                        snake, direction, food, score = reset_game()
                        last_move_time = pygame.time.get_ticks()
                        MOVE_DELAY = MOVE_DELAY_START

                elif game_over:
                    if event.key == pygame.K_SPACE:
                        snake, direction, food, score = reset_game()
                        game_over = False
                        is_paused = False
                        last_move_time = pygame.time.get_ticks()
                        MOVE_DELAY = MOVE_DELAY_START

                else:
                    if event.key == pygame.K_p:
                        is_paused = not is_paused
                    if event.key == pygame.K_g:
                        show_grid = not show_grid

                    if not is_paused:
                        if event.key == pygame.K_UP and direction != (0, 1):
                            direction = (0, -1)
                        elif event.key == pygame.K_DOWN and direction != (0, -1):
                            direction = (0, 1)
                        elif event.key == pygame.K_LEFT and direction != (1, 0):
                            direction = (-1, 0)
                        elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                            direction = (1, 0)
                        elif event.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
                            MOVE_DELAY = max(MOVE_DELAY_MIN, MOVE_DELAY - MANUAL_SPEED_STEP)
                        elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                            MOVE_DELAY = min(MOVE_DELAY_START, MOVE_DELAY + MANUAL_SPEED_STEP)

        # gesture -> game action (this is the actual Week 6 addition)
        if not game_started:
            if stable_gesture == "FIST":
                game_started = True
                snake, direction, food, score = reset_game()
                stable_gesture = "NONE"          # clear so it doesn't re-trigger next frame
                last_move_time = pygame.time.get_ticks()
                MOVE_DELAY = MOVE_DELAY_START

        elif game_over:
            if stable_gesture == "FIST":
                snake, direction, food, score = reset_game()
                game_over = False
                stable_gesture = "NONE"
                last_move_time = pygame.time.get_ticks()
                MOVE_DELAY = MOVE_DELAY_START

        else:
            if stable_gesture == "OPEN PALM":
                is_paused = True
            elif stable_gesture in ("POINT UP", "POINT DOWN", "POINT LEFT", "POINT RIGHT"):
                is_paused = False       # pointing anywhere auto-resumes, no separate resume gesture

            if not is_paused:
                if stable_gesture == "POINT UP" and direction != (0, 1):
                    direction = (0, -1)
                elif stable_gesture == "POINT DOWN" and direction != (0, -1):
                    direction = (0, 1)
                elif stable_gesture == "POINT LEFT" and direction != (1, 0):
                    direction = (-1, 0)
                elif stable_gesture == "POINT RIGHT" and direction != (-1, 0):
                    direction = (1, 0)

        # -----------------------------------------------------------
        # PHASE 3: MOVE THE SNAKE (throttled - decoupled from webcam fps)
        # -----------------------------------------------------------
        current_time = pygame.time.get_ticks()

        if game_started and not game_over and not is_paused and (current_time - last_move_time > MOVE_DELAY):
            last_move_time = current_time

            head = snake[0]
            new_head = (head[0] + direction[0], head[1] + direction[1])

            hit_wall = (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                        new_head[1] < 0 or new_head[1] >= GRID_HEIGHT)
            hit_self = new_head in snake

            if hit_wall or hit_self:
                game_over = True
                if score > high_score:
                    high_score = score
                    save_high_score(high_score)
            else:
                snake.insert(0, new_head)
                if new_head == food:
                    score += 1
                    food = random_food(snake)
                    MOVE_DELAY = max(MOVE_DELAY_MIN, MOVE_DELAY - SPEED_STEP)
                else:
                    snake.pop()

        # -----------------------------------------------------------
        # PHASE 4: RENDER GAME WINDOW
        # -----------------------------------------------------------
        screen.fill(BG_COLOR)

        if not game_started:
            title_surf = big_font.render("GESTURE SNAKE", True, SNAKE_HEAD)
            sub_surf = font.render("Make a FIST to start", True, TEXT_COLOR)
            hint_surf = font.render("Point: move | Open palm: pause | Fist: start/restart", True, GRID_COLOR)
            screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, HEIGHT // 2 - 60))
            screen.blit(sub_surf, (WIDTH // 2 - sub_surf.get_width() // 2, HEIGHT // 2))
            screen.blit(hint_surf, (WIDTH // 2 - hint_surf.get_width() // 2, HEIGHT // 2 + 40))

        else:
            if show_grid:
                for gx in range(GRID_WIDTH):
                    pygame.draw.line(screen, GRID_COLOR, (gx * CELL_SIZE, 0), (gx * CELL_SIZE, HEIGHT))
                for gy in range(GRID_HEIGHT):
                    pygame.draw.line(screen, GRID_COLOR, (0, gy * CELL_SIZE), (WIDTH, gy * CELL_SIZE))

            draw_cell(screen, food, FOOD_COLOR)
            for i, segment in enumerate(snake):
                color = SNAKE_HEAD if i == 0 else SNAKE_BODY
                draw_cell(screen, segment, color)

            score_surf = font.render(f"Score: {score}  |  Gesture: {stable_gesture}", True, TEXT_COLOR)
            hs_surf = font.render(f"Best: {high_score}", True, GOLD)
            screen.blit(score_surf, (8, 6))
            screen.blit(hs_surf, (WIDTH - hs_surf.get_width() - 8, 6))

            if is_paused and not game_over:
                pause_surf = big_font.render("PAUSED", True, TEXT_COLOR)
                sub_surf = font.render("Point in any direction to resume", True, TEXT_COLOR)
                screen.blit(pause_surf, (WIDTH // 2 - pause_surf.get_width() // 2, HEIGHT // 2 - 40))
                screen.blit(sub_surf, (WIDTH // 2 - sub_surf.get_width() // 2, HEIGHT // 2 + 15))

            if game_over:
                msg = big_font.render("GAME OVER", True, FOOD_COLOR)
                sub = font.render("Make a FIST to restart", True, TEXT_COLOR)
                screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 40))
                screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, HEIGHT // 2 + 15))

        pygame.display.flip()

        # -----------------------------------------------------------
        # PHASE 5: WEBCAM HUD WINDOW (visual feedback for debugging)
        # -----------------------------------------------------------
        cv.putText(frame, f"Gesture: {stable_gesture}", (10, 50),
                   cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv.imshow("Vision Tracking Feedback", frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()
    pygame.quit()


if __name__ == "__main__":
    main()
