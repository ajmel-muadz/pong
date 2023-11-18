import sys
import random
import pygame
from math import sqrt

pygame.init()
clock = pygame.time.Clock()


def move_paddle(keys):
    # Move the player.
    # -------------------------------------- #
    if keys[pygame.K_s] and player_rect.bottom <= SCREEN_HEIGHT:
        player_rect.y = player_rect.y + PADDLE_VEL
    if keys[pygame.K_w] and player_rect.top >= 0:
        player_rect.y = player_rect.y - PADDLE_VEL
    # -------------------------------------- #

    # Move the enemy.
    # -------------------------------------- #
    if keys[pygame.K_DOWN] and enemy_rect.bottom <= SCREEN_HEIGHT:         
        enemy_rect.y = enemy_rect.y + PADDLE_VEL
    if keys[pygame.K_UP] and enemy_rect.top >= 0:                   
        enemy_rect.y = enemy_rect.y - PADDLE_VEL                
    # -------------------------------------- #


def check_player_win():
    player_win = False
    if ball_rect.left > (SCREEN_WIDTH + 10):
        player_win = True

    return player_win


def check_enemy_win():
    enemy_win = False
    if ball_rect.right < -10:
        enemy_win = True

    return enemy_win


def reset_player_pos():
    player_rect.left = 20
    player_rect.top = (SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)


def reset_enemy_pos():
    enemy_rect.left = (SCREEN_WIDTH - PADDLE_WIDTH - 20)
    enemy_rect.top = (SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)


def reset_ball_pos():
    ball_rect.left = (SCREEN_WIDTH // 2 - BALL_WIDTH // 2)
    ball_rect.top = (SCREEN_HEIGHT // 2 - BALL_HEIGHT // 2)


# This block of code is for the screen.
# --------------------------------------------------- #
FPS = 60
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong Game")
# --------------------------------------------------- #


# This block of code is for the colours.
# ------------------------------------- #
GREY = "#363738"
GREEN = "#7fdb98"
RED = "#cf624c"
WHITE = "#cacccf"
# ------------------------------------- #


# This block of code is for declaring the object rects.
# ------------------------------------------------------------------------------------------------------------------------------------------- #
PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_VEL = 40, 150, 8
BALL_WIDTH, BALL_HEIGHT = 25, 25
DISCREPANCY_CONST = 0.1

player_rect = pygame.Rect(20, (SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2), PADDLE_WIDTH, PADDLE_HEIGHT)
enemy_rect = pygame.Rect((SCREEN_WIDTH - PADDLE_WIDTH - 20), (SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2), PADDLE_WIDTH, PADDLE_HEIGHT)
ball_rect = pygame.Rect((SCREEN_WIDTH // 2 - BALL_WIDTH // 2), (SCREEN_HEIGHT // 2 - BALL_HEIGHT // 2), BALL_WIDTH, BALL_HEIGHT)
# ------------------------------------------------------------------------------------------------------------------------------------------- #

ball_vel_x_list = [8, -8]

def main():
    # Choose random velocities for ball initially towards either the player or enemy paddle.
    ball_vel_x = random.choice(ball_vel_x_list)

    round_starts = True

    player_win = False
    enemy_win = False

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # Code responsible for drawing objects on the screen.
        # --------------------------------------------------- #
        SCREEN.fill(GREY)
        pygame.draw.rect(SCREEN, GREEN, player_rect)
        pygame.draw.rect(SCREEN, RED, enemy_rect)
        pygame.draw.ellipse(SCREEN, WHITE, ball_rect)
        # --------------------------------------------------- #

        # Code responsible for moving the player and enemy paddles vertically.
        # ------------------------------------------------------------------- #
        keys = pygame.key.get_pressed()
        move_paddle(keys)

        # ------------------------------------------------------------------- #

        # Code responsible for moving the ball and its related physics.
        # ------------------------------------------------------------------- #

        # This code determines if the ball goes horizontal for the start of each round.
        if round_starts:
            ball_rect.x = ball_rect.x + ball_vel_x
        else:
            ball_rect.x = ball_rect.x + ball_vel_x
            ball_rect.y = ball_rect.y + ball_vel_y

        # Check if ball collides with the top/bottom walls and bounce it.
        if (ball_rect.bottom >= SCREEN_HEIGHT) or (ball_rect.top <= 0):
            if ball_rect.bottom >= SCREEN_HEIGHT:
                ball_rect.bottom = SCREEN_HEIGHT
            elif ball_rect.top <= 0:
                ball_rect.top = 0
                
            ball_vel_y = ball_vel_y * -1
        
        # Check if ball collides with player paddle
        if ball_rect.colliderect(player_rect) or ball_rect.colliderect(enemy_rect):
            if ball_rect.colliderect(player_rect):
                discrepancy = (ball_rect.center[1] - player_rect.center[1])
            elif ball_rect.colliderect(enemy_rect):
                discrepancy = (ball_rect.center[1] - enemy_rect.center[1])

            ball_vel_y = (discrepancy * DISCREPANCY_CONST)  # Change the angle of ball based on where it hits paddle

            ball_vel_x = sqrt(((8 * sqrt(2)) ** 2) - ((ball_vel_y) ** 2))  # Adjust ball x-velocity so that ball is always fast

            # If ball collides with enemy its x-velocity must become negative to reflect.
            if ball_rect.colliderect(enemy_rect):
                ball_vel_x = ball_vel_x * -1
            # ball_vel_x *= -1

            round_starts = False

        # Check if the ball passes either paddles (player/enemy wins).
        # ------------------------------------------------------------ #
        player_win = check_player_win()
        enemy_win = check_enemy_win()
        # ------------------------------------------------------------ #

        if player_win or enemy_win:
            reset_player_pos()
            reset_enemy_pos()
            reset_ball_pos()

            round_starts = True

        pygame.display.update()
        clock.tick(FPS)
    
    pygame.quit()


if __name__ == "__main__":
    main()