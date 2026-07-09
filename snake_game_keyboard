"""
Week 5 - Snake Game (Keyboard Controlled)
------------------------------------------
Base game built with Pygame, using a grid-based snake that grows on food,
speeds up over time, and supports pause/restart.

On top of the base version from the course, I added a few small features
of my own to make sure I actually understood the state variables instead
of just copy-pasting:

  1. High score is now saved to disk (highscore.txt) so it survives
     between runs instead of resetting to 0 every launch.
  2. "+" / "-" keys let you manually bump the base speed up or down
     mid-game, on top of the automatic speed-up when eating food.
  3. "G" toggles the grid lines on/off, just to prove draw_cell() /
     the grid-drawing loop is separable from everything else.
  4. Live snake length is shown next to the score.

Everything else (movement, collision, welcome/pause/game-over screens)
follows the same structure as the course file, since Week 6's job is to
swap keyboard input for gesture input without touching this logic.
"""

import pygame
import random
import sys
import os

# =====================================================================
# 1. CONFIGURATION
# =====================================================================

CELL_SIZE = 30
GRID_WIDTH = 30
GRID_HEIGHT = 22
WIDTH = CELL_SIZE * GRID_WIDTH      # 900 px
HEIGHT = CELL_SIZE * GRID_HEIGHT    # 660 px

BG_COLOR   = (15, 15, 25)
SNAKE_HEAD = (0, 230, 120)
SNAKE_BODY = (0, 170, 90)
FOOD_COLOR = (240, 70, 90)
TEXT_COLOR = (235, 235, 245)
GRID_COLOR = (30, 30, 45)
GOLD       = (255, 215, 0)

HIGH_SCORE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "highscore.txt")


# =====================================================================
# 2. HELPERS
# =====================================================================

def random_food(snake):
    """Pick a random grid cell for food that isn't currently on the snake."""
    while True:
        pos = (random.randint(2, GRID_WIDTH - 3), random.randint(2, GRID_HEIGHT - 3))
        if pos not in snake:
            return pos


def draw_cell(surface, pos, color):
    """Draw one 30x30 grid cell (used for both snake segments and food)."""
    x = pos[0] * CELL_SIZE
    y = pos[1] * CELL_SIZE
    rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(surface, color, rect)
    pygame.draw.rect(surface, BG_COLOR, rect, 1)


def load_high_score():
    """My addition: read the saved high score from disk, default to 0."""
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            with open(HIGH_SCORE_FILE, "r") as f:
                return int(f.read().strip())
        except (ValueError, OSError):
            return 0
    return 0


def save_high_score(value):
    """My addition: persist the high score so it survives between runs."""
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
    pygame.display.set_caption("Snake Game - Week 5 (Keyboard)")
    font = pygame.font.SysFont("consolas", 22)
    big_font = pygame.font.SysFont("consolas", 40, bold=True)

    def reset_game():
        start = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        return [start], (1, 0), random_food([start]), 0

    snake, direction, food, score = reset_game()
    game_over = False
    is_paused = False
    game_started = False
    show_grid = True                       # my addition: toggleable grid
    high_score = load_high_score()         # my addition: persisted score

    MOVE_DELAY_START = 200
    MOVE_DELAY_MIN = 60                    # slightly faster ceiling than base
    SPEED_STEP = 5
    MANUAL_SPEED_STEP = 10                 # my addition: for +/- keys
    MOVE_DELAY = MOVE_DELAY_START
    last_move_time = pygame.time.get_ticks()

    while True:
        # -----------------------------------------------------------
        # PHASE 1: EVENTS
        # -----------------------------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_q:
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

                    # my addition: toggle grid lines any time
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

                        # my addition: manual speed control
                        elif event.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
                            MOVE_DELAY = max(MOVE_DELAY_MIN, MOVE_DELAY - MANUAL_SPEED_STEP)
                        elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                            MOVE_DELAY = min(MOVE_DELAY_START, MOVE_DELAY + MANUAL_SPEED_STEP)

        # -----------------------------------------------------------
        # PHASE 2: MOVE THE SNAKE (throttled)
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
                    save_high_score(high_score)   # my addition: write immediately on new record
            else:
                snake.insert(0, new_head)
                if new_head == food:
                    score += 1
                    food = random_food(snake)
                    MOVE_DELAY = max(MOVE_DELAY_MIN, MOVE_DELAY - SPEED_STEP)
                else:
                    snake.pop()

        # -----------------------------------------------------------
        # PHASE 3: RENDER
        # -----------------------------------------------------------
        screen.fill(BG_COLOR)

        if not game_started:
            title_surf = big_font.render("SNAKE GAME", True, SNAKE_HEAD)
            sub_surf = font.render("Press SPACE to start", True, TEXT_COLOR)
            hint_surf = font.render("Arrows: move | P: pause | +/-: speed | G: grid | Q: quit", True, GRID_COLOR)
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

            score_surf = font.render(f"Score: {score}  |  Length: {len(snake)}", True, TEXT_COLOR)
            hs_surf = font.render(f"Best: {high_score}", True, GOLD)
            screen.blit(score_surf, (8, 6))
            screen.blit(hs_surf, (WIDTH - hs_surf.get_width() - 8, 6))

            if is_paused and not game_over:
                pause_surf = big_font.render("PAUSED", True, TEXT_COLOR)
                sub_surf = font.render("Press P to resume", True, TEXT_COLOR)
                screen.blit(pause_surf, (WIDTH // 2 - pause_surf.get_width() // 2, HEIGHT // 2 - 40))
                screen.blit(sub_surf, (WIDTH // 2 - sub_surf.get_width() // 2, HEIGHT // 2 + 15))

            if game_over:
                msg = big_font.render("GAME OVER", True, FOOD_COLOR)
                sub = font.render("Press SPACE to restart   |   Q to quit", True, TEXT_COLOR)
                screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 40))
                screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, HEIGHT // 2 + 15))

        pygame.display.flip()


if __name__ == "__main__":
    main()
