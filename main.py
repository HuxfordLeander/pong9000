import asyncio
import random
import pygame

pygame.init()

# Better browser-friendly size
WIDTH = 800
HEIGHT = 450

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PONG 9000")
clock = pygame.time.Clock()

# Colours
WHITE = (255, 255, 255)
BLACK = (18, 18, 18)
GREEN = (0, 168, 107)
GRAY = (90, 90, 90)
LIGHT_GRAY = (160, 160, 160)

# Fonts
font = pygame.font.SysFont("Arial", 20)
small_font = pygame.font.SysFont("Arial", 14)
big_font = pygame.font.SysFont("Arial", 32)

# Game objects
player = pygame.Rect(26, 175, 12, 100)
ai = pygame.Rect(WIDTH - 38, 175, 12, 100)
ball = pygame.Rect(WIDTH // 2 - 10, HEIGHT // 2 - 10, 20, 20)

# Speeds
paddle_speed = 7
ai_speed = 4
ball_speed_x = random.choice((5, -5))
ball_speed_y = random.choice((5, -5))

# State
running = True
game_started = False
ai_sulking = False
secret_ending_triggered = False

player_score = 0
ai_score = 0
win_score = 10

# Humor setting
humor = 75

# Comments
glados_comments = [
    "This was a triumph. For me.",
    "That move was adorable.",
    "You lost to basic geometry.",
    "The ball expected more from you.",
    "You appear confident. Incorrectly.",
    "Your strategy is mostly decorative.",
    "This experiment is going poorly. For you.",
    "I have seen better attempts from a toaster."
]

idle_comments = [
    "Processing human input.",
    "Monitoring human skill level.",
    "Even the ball seems nervous.",
    "I expected chaos. Confirmed.",
    "This is free entertainment."
]

ai_score_comments = [
    "You missed.",
    "That looked preventable.",
    "Bold strategy. Didn't work.",
    "You lost to a rectangle.",
    "Remarkable failure.",
    "Please continue. This is funny.",
    "That miss had personality.",
    "This is professional losing."
]

player_score_comments = [
    "You got lucky.",
    "Temporary anomaly.",
    "Enjoy it while it lasts.",
    "I will allow one mistake.",
    "Clearly a fluke.",
    "A statistical anomaly.",
    "That point changes nothing."
]

current_comment = "AI online."

# Self-talk timer
idle_timer = 0
idle_interval = random.randint(900, 1500)

# Unified comment system
current_comment_priority = 0
comment_until = 0
last_comment_text = ""

category_cooldowns = {
    "idle": 0,
    "high_humor": 0,
    "ai_score": 0,
    "player_score": 0,
    "score_gap": 0
}

# Score-gap milestone tracker
last_score_gap_taunt = 0

# Ending overlay state
ending_lines = None
ending_until = 0
ending_sulk_after = False


def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed_x = random.choice((5, -5))
    ball_speed_y = random.choice((5, -5))


def reset_game():
    global player_score, ai_score, secret_ending_triggered
    global game_started, ai_sulking
    global current_comment, current_comment_priority, comment_until, last_comment_text
    global idle_timer, idle_interval
    global ending_lines, ending_until, ending_sulk_after
    global category_cooldowns, last_score_gap_taunt

    player_score = 0
    ai_score = 0
    secret_ending_triggered = False
    game_started = False
    ai_sulking = False

    current_comment = "AI online."
    current_comment_priority = 0
    comment_until = 0
    last_comment_text = ""
    idle_timer = 0
    idle_interval = random.randint(900, 1500)

    category_cooldowns = {
        "idle": 0,
        "high_humor": 0,
        "ai_score": 0,
        "player_score": 0,
        "score_gap": 0
    }
    last_score_gap_taunt = 0

    ending_lines = None
    ending_until = 0
    ending_sulk_after = False

    player.y = 175
    ai.y = 175
    reset_ball()


def soft_return_to_menu():
    global player_score, ai_score, secret_ending_triggered
    global game_started
    global current_comment, current_comment_priority, comment_until, last_comment_text
    global idle_timer, idle_interval
    global ending_lines, ending_until, ending_sulk_after
    global category_cooldowns, last_score_gap_taunt

    player_score = 0
    ai_score = 0
    secret_ending_triggered = False
    game_started = False

    current_comment = "AI online."
    current_comment_priority = 0
    comment_until = 0
    last_comment_text = ""
    idle_timer = 0
    idle_interval = random.randint(900, 1500)

    category_cooldowns = {
        "idle": 0,
        "high_humor": 0,
        "ai_score": 0,
        "player_score": 0,
        "score_gap": 0
    }
    last_score_gap_taunt = 0

    ending_lines = None
    ending_until = 0
    ending_sulk_after = False

    player.y = 175
    ai.y = 175
    reset_ball()


def trigger_ending(lines, duration_ms=3000, sulk_after=False):
    global ending_lines, ending_until, ending_sulk_after
    ending_lines = lines
    ending_until = pygame.time.get_ticks() + duration_ms
    ending_sulk_after = sulk_after


def draw_centered_text(y, text, use_big=False, colour=WHITE):
    f = big_font if use_big else font
    surface = f.render(text, True, colour)
    screen.blit(surface, (WIDTH // 2 - surface.get_width() // 2, y))


def draw_start_screen():
    screen.fill(BLACK)

    draw_centered_text(70, "PONG 9000", use_big=True)
    draw_centered_text(124, "PONG 9000 ONLINE", colour=GREEN)

    init_surface = small_font.render(
        "Creator: Huxford | Human test subject detected.",
        True,
        LIGHT_GRAY
    )
    screen.blit(init_surface, (WIDTH // 2 - init_surface.get_width() // 2, 156))

    if not ai_sulking:
        draw_centered_text(215, "SPACE to start")
        draw_centered_text(252, "W / S to move")
        draw_centered_text(286, "R restart reality")
        draw_centered_text(330, "A / D (or LEFT / RIGHT) adjust HUMOR")
        draw_centered_text(366, f"TARS HUMOR: {humor}%", colour=GREEN)
    else:
        draw_centered_text(215, "REMATCH DENIED", use_big=True)
        draw_centered_text(284, "The AI is pretending your victory was a bug.", colour=GREEN)
        draw_centered_text(328, "Press R to reset reality.")

    pygame.display.flip()


def draw_ending_overlay(lines):
    screen.fill(BLACK)

    if len(lines) == 1:
        draw_centered_text(200, lines[0], use_big=True)

    elif len(lines) == 2:
        draw_centered_text(178, lines[0], use_big=True)
        draw_centered_text(248, lines[1])

    elif len(lines) == 3:
        draw_centered_text(150, lines[0], use_big=True)
        draw_centered_text(225, lines[1])
        draw_centered_text(260, lines[2])

    pygame.display.flip()


def draw_game():
    screen.fill(BLACK)

    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))
    pygame.draw.rect(screen, WHITE, player)
    pygame.draw.rect(screen, WHITE, ai)
    pygame.draw.ellipse(screen, GREEN, ball)

    player_text = font.render(str(player_score), True, WHITE)
    ai_text = font.render(str(ai_score), True, WHITE)

    screen.blit(player_text, (WIDTH // 4, 16))
    screen.blit(ai_text, (WIDTH * 3 // 4, 16))

    humor_text = small_font.render(f"HUMOR {humor}%", True, GREEN)
    screen.blit(humor_text, (WIDTH - 95, 16))

    pygame.draw.rect(screen, GRAY, (430, 392, 340, 40), 1)
    comment_surface = small_font.render(current_comment, True, GREEN)
    screen.blit(comment_surface, (440, 405))

    pygame.display.flip()


def pick_line(lines):
    global last_comment_text
    candidates = [line for line in lines if line != last_comment_text]
    if not candidates:
        candidates = lines
    return random.choice(candidates)


def show_comment(text, priority=1, duration_ms=4500, force=False):
    global current_comment, current_comment_priority, comment_until, last_comment_text

    now = pygame.time.get_ticks()

    if not force and now < comment_until and priority < current_comment_priority:
        return False

    current_comment = text
    current_comment_priority = priority
    comment_until = now + duration_ms
    last_comment_text = text
    return True


def try_category_comment(category, lines, priority, cooldown_ms, duration_ms=4500, force=False):
    global category_cooldowns
    now = pygame.time.get_ticks()

    if now < category_cooldowns[category]:
        return False

    text = pick_line(lines)
    ok = show_comment(text, priority=priority, duration_ms=duration_ms, force=force)

    if ok:
        category_cooldowns[category] = now + cooldown_ms

    return ok


async def main():
    global running
    global game_started, humor, ai_sulking
    global player_score, ai_score, secret_ending_triggered
    global idle_timer, idle_interval
    global ball_speed_x, ball_speed_y
    global ending_lines, ending_until
    global last_score_gap_taunt

    while running:
        clock.tick(60)

        # ---------- ENDING OVERLAY ----------
        if ending_lines is not None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            draw_ending_overlay(ending_lines)

            if pygame.time.get_ticks() >= ending_until:
                sulk = ending_sulk_after
                soft_return_to_menu()
                if sulk:
                    ai_sulking = True

            await asyncio.sleep(0)
            continue

        # ---------- START SCREEN ----------
        if not game_started:
            draw_start_screen()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not ai_sulking:
                        game_started = True
                    elif event.key == pygame.K_r:
                        reset_game()
                    elif (event.key == pygame.K_a or event.key == pygame.K_LEFT) and not ai_sulking:
                        humor = max(0, humor - 5)
                    elif (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and not ai_sulking:
                        humor = min(100, humor + 5)

            await asyncio.sleep(0)
            continue

        # ---------- INPUT ----------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and player.top > 0:
            player.y -= paddle_speed

        if keys[pygame.K_s] and player.bottom < HEIGHT:
            player.y += paddle_speed

        if keys[pygame.K_r]:
            reset_game()
            await asyncio.sleep(0)
            continue

        # ---------- AI ----------
        if random.random() > 0.08:
            if ai.centery < ball.centery and ai.bottom < HEIGHT:
                ai.y += ai_speed
            elif ai.centery > ball.centery and ai.top > 0:
                ai.y -= ai_speed

        # ---------- BALL ----------
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # ---------- IDLE COMMENT ----------
        idle_timer += 1
        if idle_timer > idle_interval:
            try_category_comment(
                "idle",
                idle_comments,
                priority=2,
                cooldown_ms=18000,
                duration_ms=4000
            )

            if humor > 80 and random.random() < 0.5:
                try_category_comment(
                    "high_humor",
                    glados_comments,
                    priority=3,
                    cooldown_ms=12000,
                    duration_ms=4500
                )

            idle_timer = 0
            idle_interval = random.randint(900, 1500)

        # ---------- WALL ----------
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1

        # ---------- PADDLES ----------
        if ball.colliderect(player) and ball_speed_x < 0:
            ball_speed_x *= -1

        if ball.colliderect(ai) and ball_speed_x > 0:
            ball_speed_x *= -1

        # ---------- SCORE ----------
        if ball.left <= 0:
            ai_score += 1

            if humor > 80 and random.random() < 0.35:
                show_comment(pick_line(glados_comments), priority=4, duration_ms=4500, force=True)
            else:
                try_category_comment(
                    "ai_score",
                    ai_score_comments,
                    priority=4,
                    cooldown_ms=1000,
                    duration_ms=4500,
                    force=True
                )

            idle_timer = 0
            idle_interval = random.randint(900, 1500)
            reset_ball()

        if ball.right >= WIDTH:
            player_score += 1

            if humor > 80 and random.random() < 0.2:
                show_comment(pick_line(glados_comments), priority=4, duration_ms=4500, force=True)
            else:
                try_category_comment(
                    "player_score",
                    player_score_comments,
                    priority=4,
                    cooldown_ms=1000,
                    duration_ms=4500,
                    force=True
                )

            idle_timer = 0
            idle_interval = random.randint(900, 1500)
            reset_ball()

        # ---------- SCORE TAUNT ----------
        score_gap = player_score - ai_score

        if score_gap >= 8 and last_score_gap_taunt < 8:
            if show_comment("Escalating to creator Huxford.", priority=5, duration_ms=5000, force=True):
                last_score_gap_taunt = 8

        elif score_gap >= 6 and last_score_gap_taunt < 6:
            if show_comment("This experiment is degrading.", priority=5, duration_ms=5000, force=True):
                last_score_gap_taunt = 6

        elif score_gap >= 4 and last_score_gap_taunt < 4:
            if show_comment("Unexpected human competence.", priority=5, duration_ms=5000, force=True):
                last_score_gap_taunt = 4

        elif score_gap >= 3 and last_score_gap_taunt < 3:
            if show_comment("Noted.", priority=5, duration_ms=4000, force=True):
                last_score_gap_taunt = 3

        # ---------- SECRET ENDINGS ----------
        if player_score == 3 and ai_score == 3 and not secret_ending_triggered:
            secret_ending_triggered = True
            trigger_ending([
                "BALANCE ACHIEVED",
                "I'm sorry, player.",
                "This match is too balanced."
            ], 10000)
            await asyncio.sleep(0)
            continue

        if player_score == 6 and ai_score == 7 and not secret_ending_triggered:
            secret_ending_triggered = True
            trigger_ending([
                "NARROW DEFEAT",
                "History remembers 6-7"
            ], 10000)
            await asyncio.sleep(0)
            continue

        if player_score == 9 and ai_score == 9:
            trigger_ending([
                "SYSTEM OVERRIDE",
                "Creator Huxford has joined the chat.",
                "\"Stop breaking my AI.\""
            ], 10000)
            await asyncio.sleep(0)
            continue

        if player_score == 4 and ai_score == 2:
            trigger_ending([
                "42",
                "Answer to Life, Universe, Everything"
            ], 10000, sulk_after=True)
            await asyncio.sleep(0)
            continue

        if player_score == 10 and ai_score == 0:
            trigger_ending([
                "SYSTEM NOTICE",
                "Creator Huxford will review this match."
            ], 10000, sulk_after=True)
            await asyncio.sleep(0)
            continue

        # ---------- WIN ----------
        if player_score >= win_score:
            trigger_ending([
                "AI.EXE HAS STOPPED WORKING",
                "Incident report sent to creator: Huxford."
            ], 10000, sulk_after=True)
            await asyncio.sleep(0)
            continue

        if ai_score >= win_score:
            trigger_ending([
                "AI HAS HUMILIATED YOU"
            ], 10000)
            await asyncio.sleep(0)
            continue

        # ---------- DRAW ----------
        draw_game()

        await asyncio.sleep(0)

    pygame.quit()


asyncio.run(main())