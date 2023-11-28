import sys
import random
import pygame
from math import sqrt

pygame.init()
clock = pygame.time.Clock()

# Functions concerned with MOVING anything.
# --------------------------------------------------------------------------------- #
def move_player_paddle(keys):
    if keys[pygame.K_s] and player_rect.bottom <= SCREEN_HEIGHT:
        player_rect.y = player_rect.y + PADDLE_VEL
    elif keys[pygame.K_w] and player_rect.top >= 0:
        player_rect.y = player_rect.y - PADDLE_VEL

def move_second_paddle(single_player_chosen, two_player_chosen, ball_vel_y, enemy_vel):
    if single_player_chosen:
        single_player(ball_vel_y, enemy_vel)
    elif two_player_chosen:
        two_player()

# FINALLY MADE THE AI WORK
def single_player(ball_vel_y, enemy_vel):
    if abs(ball_vel_y) < abs(enemy_vel):  # The paddle exactly follows ball speeds less than enemy_vel, to eliminate stuttering/jittering
        enemy_rect.y = enemy_rect.y + ball_vel_y
    else:
        if ball_rect.bottom < enemy_rect.top:
            enemy_rect.y = enemy_rect.y - enemy_vel  # enemy_vel passed determines speed of enemy paddle for determining difficulty.
        elif ball_rect.top > enemy_rect.bottom:
            enemy_rect.y = enemy_rect.y + enemy_vel 

    # This section is responsible for not allowing the enemy paddle to exceed the screen.
    if enemy_rect.bottom > SCREEN_HEIGHT:
        enemy_rect.bottom = SCREEN_HEIGHT
    elif enemy_rect.top < 0:
        enemy_rect.top = 0

def two_player():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN] and enemy_rect.bottom <= SCREEN_HEIGHT:
        enemy_rect.y = enemy_rect.y + PADDLE_VEL
    if keys[pygame.K_UP] and enemy_rect.top >= 0:
        enemy_rect.y = enemy_rect.y - PADDLE_VEL

def move_ball_horizontally(ball_vel_x, ball_vel_y):
    # This code randomly chooses where the ball goes to initially.
    ball_vel_x_list = [6, -6]
    ball_vel_x = random.choice(ball_vel_x_list)
    ball_rect.x = ball_rect.x + ball_vel_x
    ball_vel_y = 0  # y-velocity is zero because to make it easier at the start of each round.

    ball_velocities = (ball_vel_x, ball_vel_y)

    return ball_velocities

def move_ball_at_angle(ball_vel_x, ball_vel_y):
    # After the ball bounces of a paddle it does so at certain angles.
    ball_rect.x = ball_rect.x + ball_vel_x
    ball_rect.y = ball_rect.y + ball_vel_y
# --------------------------------------------------------------------------------- #


# Functions concerned with checking if a paddle wins the game. 
# ----------------------------------------------------------------- #
def check_player_win():
    player_win = False
    if ball_rect.left >= SCREEN_WIDTH and ball_rect.left <= SCREEN_WIDTH + 10:
        score_sound.play()

    if ball_rect.left > (SCREEN_WIDTH + 750):
        player_win = True

    return player_win

def check_enemy_win():
    enemy_win = False
    if ball_rect.right <= 0 and ball_rect.right >= -10:
        score_sound.play()

    if ball_rect.right < -750:
        enemy_win = True

    return enemy_win
# ----------------------------------------------------------------- #


# Functions concerned with resetting game state.
# ----------------------------------------------------------------- #
def reset_player_pos():
    player_rect.left = 20
    player_rect.top = (SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)

def reset_enemy_pos():
    enemy_rect.left = (SCREEN_WIDTH - PADDLE_WIDTH - 20)
    enemy_rect.top = (SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)

def reset_ball_pos():
    ball_rect.left = (SCREEN_WIDTH // 2 - BALL_WIDTH // 2)
    ball_rect.top = (SCREEN_HEIGHT // 2 - BALL_HEIGHT // 2)
# ----------------------------------------------------------------- #


# Functions that are concerned with ball COLLISIONS with paddles or walls.
# ---------------------------------------------------------------------------------------------------- #
def wall_collision(ball_vel_y):
    if (ball_rect.bottom >= SCREEN_HEIGHT) or (ball_rect.top <= 0):
        # In case ball bottom/top exceeds the screen, place it so that it can bounce correctly.
        if ball_rect.bottom >= SCREEN_HEIGHT:
            ball_rect.bottom = SCREEN_HEIGHT
        elif ball_rect.top <= 0:
            ball_rect.top = 0

        ball_vel_y = ball_vel_y * -1

    if (ball_rect.bottom >= SCREEN_HEIGHT) or (ball_rect.top <= 0):
        if ball_rect.left > 0 and ball_rect.right < SCREEN_WIDTH:
            wall_sound.play()

    return ball_vel_y

def paddle_collision(ball_vel_x, ball_vel_y):
    # NOTE: The ball's speed when facing any direction is sqrt(200)

    if ball_rect.colliderect(player_rect):
        discrepancy = (ball_rect.center[1] - player_rect.center[1])
        player_paddle_sound.play()
    elif ball_rect.colliderect(enemy_rect):
        discrepancy = (ball_rect.center[1] - enemy_rect.center[1])
        enemy_paddle_sound.play()

    ball_vel_y = (discrepancy * ANGLE_FACTOR)  # Change the angle of ball based on where it hits paddle

    ball_vel_x = sqrt(((10 * sqrt(2)) ** 2) - ((ball_vel_y) ** 2))  # Adjust ball x-velocity so that ball is always fast

    # If ball collides with enemy its x-velocity must become negative to reflect.
    if ball_rect.colliderect(enemy_rect):
        ball_vel_x = ball_vel_x * -1

    ball_velocities = (ball_vel_x, ball_vel_y)

    return ball_velocities
# ---------------------------------------------------------------------------------------------------- #


# Functions concerned with the player score.
# ---------------------------------------------------------------------------------------------------- #
def display_player_score(player_score):
    score_surf = score_font.render(f"{player_score}", False, GREEN)
    score_rect = score_surf.get_rect(center = (320, 50))
    SCREEN.blit(score_surf, score_rect)

def display_enemy_score(enemy_score):
    score_surf = score_font.render(f"{enemy_score}", False, RED)
    score_rect = score_surf.get_rect(center = (960, 50))
    SCREEN.blit(score_surf, score_rect)
# ---------------------------------------------------------------------------------------------------- #


# Functions concerned with the main and pause menu.
# ---------------------------------------------------------------------------------------------------- #
def button_rect(text, position):
    text_surf = score_font.render(text, False, BLACK)
    text_rect = text_surf.get_rect(center = position)

    rect_width = text_rect.width + 20
    rect_height = text_rect.height + 20

    bg_rect = pygame.Rect(text_rect.left, text_rect.top, rect_width, rect_height)
    bg_rect.center = text_rect.center

    pygame.draw.rect(SCREEN, WHITE, bg_rect)
    SCREEN.blit(text_surf, text_rect)

    return bg_rect

def one_player_text():
    bg_rect = button_rect("One Player", (SCREEN_WIDTH * 0.25, SCREEN_HEIGHT // 2))

    return bg_rect

def two_player_text():
    bg_rect = button_rect("Two Player", (SCREEN_WIDTH * 0.75, SCREEN_HEIGHT // 2))

    return bg_rect

def divider_line():
    divider_rect = pygame.Rect(SCREEN_WIDTH // 2, 0, DIVIDER_WIDTH, SCREEN_HEIGHT)
    pygame.draw.rect(SCREEN, BLACK, divider_rect)

def pause_bg():
    pause_bg_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    pygame.draw.rect(SCREEN, TURQUOISE, pause_bg_rect)

def resume_button():
    bg_rect = button_rect("RESUME", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))

    return bg_rect

def restart_button():
    bg_rect = button_rect("RESTART", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    return bg_rect

def quit_button():
    bg_rect = button_rect("QUIT", (SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4))
    
    return bg_rect

def easy_mode():
    bg_rect = button_rect("EASY", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))

    return bg_rect

def medium_mode():
    bg_rect = button_rect("MEDIUM", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    return bg_rect

def hard_mode():
    bg_rect = button_rect("HARD", (SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4))

    return bg_rect

def go_back():
    bg_rect = button_rect("Go Back", (SCREEN_WIDTH // 10, SCREEN_HEIGHT - 45))

    return bg_rect

def back_to_menu():
    bg_rect = button_rect("Back to Menu", (SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4))

    return bg_rect

def mouse_pos_in(rect, pos):
    mouse_in_rect = False
    if (pos[0] >= rect.left and pos[0] <= rect.right) and (pos[1] >= rect.top and pos[1] <= rect.bottom):
        mouse_in_rect = True

    return mouse_in_rect
# ---------------------------------------------------------------------------------------------------- #

# Code used to display the help screen.
# ---------------------------------------------------------------------------------------------------- #
def display_help_screen():
    line1_surf = smaller_score_font.render("The objective of the game is to score 5 points.", False, BLACK)
    line1_rect = line1_surf.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))

    line2_surf = smaller_score_font.render("Press 'ESC' to pause the game at any point.", False, BLACK)
    line2_rect = line2_surf.get_rect(center = (SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) + 25))

    line3_surf = smaller_score_font.render("(Click anywhere on the screen to start the game)", False, BLACK)
    line3_rect = line3_surf.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4))

    SCREEN.blit(line1_surf, line1_rect)
    SCREEN.blit(line2_surf, line2_rect)
    SCREEN.blit(line3_surf, line3_rect)
# ---------------------------------------------------------------------------------------------------- #

# Code used to determine who wins the game.
# ---------------------------------------------------------------------------------------------------- #
def display_winner(player_score, enemy_score):
    text = ""
    if player_score == GAME_WIN_SCORE:
        text = "Green Paddle Wins!"
    elif enemy_score == GAME_WIN_SCORE:
        text = "Red Paddle Wins!"

    text_surf = score_font.render(text, False, BLACK)
    text_rect = text_surf.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    SCREEN.blit(text_surf, text_rect)
# ---------------------------------------------------------------------------------------------------- #


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
PEARL_WHITE = "#cacccf"
WHITE = "#f5f5f5"
TURQUOISE = "#64c5e8"
BLACK = "#000000"
# ------------------------------------- #


# This block of code is for declaring the object rects.
# ------------------------------------------------------------------------------------------------------------------------------------------- #
PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_VEL = 40, 150, 8
BALL_WIDTH, BALL_HEIGHT = 25, 25
ANGLE_FACTOR = 0.125  # Constant responsible for ball angles.

GAME_WIN_SCORE = 5
DIVIDER_WIDTH = 10

score_font = pygame.font.Font("fonts/gamer_font.ttf", 50)
smaller_score_font = pygame.font.Font("fonts/gamer_font.ttf", 40)

player_rect = pygame.Rect(20, (SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2), PADDLE_WIDTH, PADDLE_HEIGHT)
enemy_rect = pygame.Rect((SCREEN_WIDTH - PADDLE_WIDTH - 20), (SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2), PADDLE_WIDTH, PADDLE_HEIGHT)
ball_rect = pygame.Rect((SCREEN_WIDTH // 2 - BALL_WIDTH // 2), (SCREEN_HEIGHT // 2 - BALL_HEIGHT // 2), BALL_WIDTH, BALL_HEIGHT)
# ------------------------------------------------------------------------------------------------------------------------------------------- #


# Code responsible for the game music.
# --------------------------------------------------------------------------------------- #
menu_music = pygame.mixer.Sound("audio/bit-shift.mp3")
menu_music.set_volume(0.25)

player_paddle_sound = pygame.mixer.Sound("audio/player_paddle_hit.wav")
enemy_paddle_sound = pygame.mixer.Sound("audio/enemy_paddle_hit.wav")
wall_sound = pygame.mixer.Sound("audio/wall_hit.wav")

score_sound = pygame.mixer.Sound("audio/game_score.wav")
win_music = pygame.mixer.Sound("audio/win_music.mp3")
# --------------------------------------------------------------------------------------- #

def main():
    menu_music_plays = 0
    whole_game_runs = True

    # Whole game loop
    # ------------------------------------------------------------------------------------------------ #
    while whole_game_runs:
        start_menu_runs = True  # Boolean that controls the main menu loop.
        difficulty_menu_runs = True  # Boolean that controls the menu for choosing difficulty.
        help_screen = True
        game_runs = True  # Boolean that controls the main game loop.
        game_end = True

        reset_player_pos()
        reset_enemy_pos()
        reset_ball_pos()

        ball_vel_x = 0
        ball_vel_y = 0  # Initialise the y-velocity.

        round_starts = True

        player_win = False
        player_score = 0
        enemy_win = False
        enemy_score = 0

        pause = False

        single_player_chosen = False
        two_player_chosen = False

        easy_chosen = False
        medium_chosen = False
        hard_chosen = False

        if menu_music_plays == 0:
            menu_music.play(loops=-1)
            menu_music_plays += 1

        while start_menu_runs:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    if mouse_pos_in(one_player_text(), pos):
                        if pygame.mouse.get_pressed()[0]:
                            single_player_chosen = True
                            start_menu_runs = False
                    
                    elif mouse_pos_in(two_player_text(), pos):
                        if pygame.mouse.get_pressed()[0]:
                            two_player_chosen = True
                            start_menu_runs = False

            # Background colour of the main menu.
            SCREEN.fill(TURQUOISE)
            # Display the option for one player
            one_player_text()
            # Display the option for two player
            two_player_text()
            # Draw a divider line in the middle of the screen
            divider_line()
            
            pygame.display.update()
            clock.tick(FPS)
        # ------------------------------------------------------------------------------------------------ #

        while difficulty_menu_runs and single_player_chosen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    if mouse_pos_in(easy_mode(), pos):
                        if pygame.mouse.get_pressed()[0]:
                            easy_chosen = True
                            difficulty_menu_runs = False
                    
                    elif mouse_pos_in(medium_mode(), pos):
                        if pygame.mouse.get_pressed()[0]:
                            medium_chosen = True
                            difficulty_menu_runs = False

                    elif mouse_pos_in(hard_mode(), pos):
                        if pygame.mouse.get_pressed()[0]:
                            hard_chosen = True
                            difficulty_menu_runs = False

                    elif mouse_pos_in(go_back(), pos):
                        if pygame.mouse.get_pressed()[0]:
                            difficulty_menu_runs = False
                            help_screen = False
                            game_runs = False
                            game_end = False
                            start_menu_runs = True

            # Background colour of the difficulty menu.
            SCREEN.fill(TURQUOISE)
            # Display the option for easy mode
            easy_mode()
            # Display the option for medium mode
            medium_mode()
            # Display the option for hard mode
            hard_mode()
            # Display the option to go back to main menu from 'difficulty' menu
            go_back()

            pygame.display.update()
            clock.tick(FPS)

        
        while help_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        help_screen = False

            SCREEN.fill(TURQUOISE)
            display_help_screen()

            pygame.display.update()
            clock.tick(FPS)


        # Main game loop.
        # ------------------------------------------------------------------------------------------------ #
        while game_runs:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pause = not pause
                elif event.type == pygame.MOUSEBUTTONDOWN and pause == True:
                    pos = pygame.mouse.get_pos()

                    if mouse_pos_in(resume_button(), pos):
                        if pygame.mouse.get_pressed()[0]:
                            pause = not pause

                    elif mouse_pos_in(restart_button(), pos):
                        if pygame.mouse.get_pressed()[0]:
                            reset_player_pos()
                            reset_enemy_pos()
                            reset_ball_pos()
                            player_score = 0
                            enemy_score = 0
                            round_starts = True

                            pause = not pause

                    elif mouse_pos_in(quit_button(), pos):
                        if pygame.mouse.get_pressed()[0]:
                            main()  # Calling the main function again means the whole 'game' restarts.

            menu_music.stop()  # Stop menu music when game starts playing.

            # If pause == False means if the player did not click 'ESC' to pause the game.
            if pause == False:
                # Code responsible for drawing objects on the screen.
                # --------------------------------------------------- #
                SCREEN.fill(GREY)
                pygame.draw.rect(SCREEN, GREEN, player_rect)
                pygame.draw.rect(SCREEN, RED, enemy_rect)
                pygame.draw.ellipse(SCREEN, PEARL_WHITE, ball_rect)
                # --------------------------------------------------- #


                # Code responsible for moving the player and enemy paddles vertically.
                # ------------------------------------------------------------------- #
                keys = pygame.key.get_pressed()
                move_player_paddle(keys)

                # The difficulty chosen dictates how fast the enemy paddle is.
                if easy_chosen:
                    enemy_vel = 6
                elif medium_chosen:
                    enemy_vel = 8
                elif hard_chosen:
                    enemy_vel = 10
                else:
                    enemy_vel = 0
                
                move_second_paddle(single_player_chosen, two_player_chosen, ball_vel_y, enemy_vel)
                # ------------------------------------------------------------------- #


                # Code responsible for moving the ball and its related physics.
                # ------------------------------------------------------------------- #
                if round_starts:
                    # If the round starts, the ball is moved horizontally to either paddle or player.
                    ball_vel_x, ball_vel_y = move_ball_horizontally(ball_vel_x, ball_vel_y)
                    round_starts = False
                else:
                    # After the ball hits any paddle horizontally, it will bounce at a certain angle.
                    move_ball_at_angle(ball_vel_x, ball_vel_y)
                # ------------------------------------------------------------------- #

                # Check if ball collides with the top/bottom walls and bounce it.
                # -------------------------------------------------------------- #
                ball_vel_y = wall_collision(ball_vel_y)
                # -------------------------------------------------------------- #


                # Responsible for ball angles when colliding with player or enemy paddle.
                # ----------------------------------------------------------------------------------------------------------------------------- #
                if ball_rect.colliderect(player_rect) or ball_rect.colliderect(enemy_rect):
                    ball_vel_x, ball_vel_y = paddle_collision(ball_vel_x, ball_vel_y)
                    round_starts = False
                # ----------------------------------------------------------------------------------------------------------------------------- #


                # Check if the ball passes either paddles (player/enemy wins).
                # ------------------------------------------------------------ #
                player_win = check_player_win()
                enemy_win = check_enemy_win()
                # ------------------------------------------------------------ #


                # Code responsible for the player and enemy scores.
                # ------------------------------------------------- #
                display_player_score(player_score)
                display_enemy_score(enemy_score)
                # ------------------------------------------------- #


                # Code executed if either player or enemy wins
                # ------------------------------------------------------- #
                if player_win or enemy_win:
                    if player_win:
                        player_score = player_score + 1
                    elif enemy_win:
                        enemy_score = enemy_score + 1

                    reset_player_pos()
                    reset_enemy_pos()
                    reset_ball_pos()

                    round_starts = True

                    if player_score == GAME_WIN_SCORE:
                        game_runs = False
                    elif enemy_score == GAME_WIN_SCORE:
                        game_runs = False
                # ------------------------------------------------------- #
            else:
                pause_bg()  # Display the colour of the pause menu background (turquoise)
                resume_button()
                restart_button()
                quit_button()

            pygame.display.update()
            clock.tick(FPS)
        # ------------------------------------------------------------------------------------------------ #

        win_music_plays = 0
        while game_end:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    if mouse_pos_in(back_to_menu(), pos):
                        if pygame.mouse.get_pressed()[0]:
                            main()

            if win_music_plays == 0:
                win_music.play()
                win_music_plays += 1

            SCREEN.fill(TURQUOISE)
            display_winner(player_score, enemy_score)
            back_to_menu()

            pygame.display.update()
            clock.tick(FPS)
    
    pygame.quit()


if __name__ == "__main__":
    main()