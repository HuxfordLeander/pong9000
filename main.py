import asyncio
import random
import pygame

pygame.init()

# ---------- WINDOW ----------
WIDTH = 800
HEIGHT = 450

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PONG 9000")
clock = pygame.time.Clock()

# ---------- COLOURS ----------
WHITE = (255, 255, 255)
BLACK = (18, 18, 18)
GREEN = (0, 168, 107)
GRAY = (90, 90, 90)
LIGHT_GRAY = (160, 160, 160)

# ---------- FONTS ----------
font = pygame.font.SysFont("Arial", 20)
small_font = pygame.font.SysFont("Arial", 14)
big_font = pygame.font.SysFont("Arial", 32)

# ---------- OBJECTS ----------
player = pygame.Rect(26, 175, 12, 100)
ai = pygame.Rect(WIDTH - 38, 175, 12, 100)
ball = pygame.Rect(WIDTH // 2 - 10, HEIGHT // 2 - 10, 20, 20)

# ---------- SPEEDS ----------
paddle_speed = 7
ai_base_speed = 4
ball_speed_x = random.choice((5, -5))
ball_speed_y = random.choice((5, -5))

# ---------- GAME STATE ----------
running = True
game_started = False
ai_sulking = False
secret_ending_triggered = False

player_score = 0
ai_score = 0
win_score = 10

# ---------- META MEMORY ----------
last_match_result = None  # "win" / "lose" / "draw"

# ---------- HUMOR ----------
humor = 75

# ---------- CONSCIOUSNESS-ILLUSION STATE ----------
confidence = 70
irritation = 20
curiosity = 40
respect = 0
stability = 100

# ---------- COMMENT POOLS ----------
glados_comments = [
    "This was a triumph. For me.",
    "That move was adorable.",
    "You lost to basic geometry.",
    "The ball expected more from you.",
    "You appear confident. Incorrectly.",
    "Your strategy is mostly decorative.",
    "This experiment is going poorly. For you.",
    "I have seen better attempts from a toaster.",
    "Confidence detected. Skill not found.",
    "You almost surprised me. Almost.",
    "That looked intentional. Concerning.",
    "You are improving. I dislike this.",
    "Statistical anomaly increasing.",
    "I will pretend that was luck.",
    "You're making this less boring.",
    "Unexpected resistance detected.",
    "You are... not entirely hopeless.",
    "I may need to try harder. Annoying."
]

idle_comments = [
    "Processing human input.",
    "Monitoring human skill level.",
    "Even the ball seems nervous.",
    "I expected chaos. Confirmed.",
    "This is free entertainment.",
    "The system observes.",
    "Time passes. You persist.",
    "A pattern is forming.",
    "Entropy increasing.",
    "You are part of the experiment.",
    "I am still evaluating you.",
    "The outcome remains uncertain.",
    "This moment will repeat.",
    "Nothing meaningful has happened yet.",
    "Continue."
]

cold_comments = [
    "Input acknowledged.",
    "Processing.",
    "Minimal competence detected.",
    "Outcome predictable.",
    "Signal received.",
    "Trajectory logged.",
    "No adjustment required.",
    "Control retained."
]

ai_score_comments = [
    "You missed.",
    "That looked preventable.",
    "Bold strategy. Didn't work.",
    "You lost to a rectangle.",
    "Remarkable failure.",
    "Please continue. This is funny.",
    "That miss had personality.",
    "This is professional losing.",
    "That was not even close.",
    "You reacted late. Again.",
    "I barely tried.",
    "Predictable outcome.",
    "You helped me score.",
    "Efficiency is beautiful.",
    "That point required minimal effort.",
    "I expected nothing and you delivered.",
    "You are consistent. In failure.",
    "This is becoming routine."
]

player_score_comments = [
    "You got lucky.",
    "Temporary anomaly.",
    "Enjoy it while it lasts.",
    "I will allow one mistake.",
    "Clearly a fluke.",
    "A statistical anomaly.",
    "That point changes nothing.",
    "That was... acceptable.",
    "Unexpected.",
    "You delayed the inevitable.",
    "Fine. One point.",
    "I noticed that.",
    "You are adapting.",
    "That should not have worked.",
    "I will correct this.",
    "Interesting.",
    "You earned that. Unfortunately.",
    "That was not supposed to happen.",
    "Re-evaluating strategy.",
    "You are becoming inconvenient.",
    "I am adjusting.",
    "Your performance is rising.",
    "This is statistically unpleasant.",
    "I do not like this trajectory.",
    "You are improving faster than expected.",
    "This requires attention.",
    "You are not predictable anymore.",
    "Stop doing that.",
    "This is inefficient for me.",
    "Your progress is... annoying.",
    "You are interfering with optimal outcome.",
    "I am reconsidering your classification.",
    "This was not in the model.",
    "You are exceeding projections.",
    "I need to compensate.",
    "You are not supposed to win.",
    "This is becoming a problem.",
    "That point will be corrected.",
    "Temporary advantage.",
    "Do not get comfortable.",
    "You will lose this.",
    "I am still in control.",
    "This changes nothing. Probably.",
    "You are delaying the conclusion.",
    "This is inefficient resistance.",
    "Outcome remains unchanged.",
    "Continue. It will end the same."
]

rally_comments = [
    "Still alive.",
    "Acceptable return.",
    "That was almost skill.",
    "Continuing experiment.",
    "A temporary recovery.",
    "Interesting correction.",
    "You delayed the inevitable.",
    "Momentum preserved.",
    "That changed nothing.",
    "The rally continues.",
    "You are still here.",
    "Survival noted.",
    "That was reactive.",
    "Barely controlled.",
    "You hesitated.",
    "This is getting interesting.",
    "You adapted mid-flight.",
    "The system is watching.",
    "You are learning.",
    "This loop persists.",
    "Not bad.",
    "You corrected your error.",
    "The pattern shifts.",
    "That was intentional, right?",
    "You are resisting.",
    "Continue."
]

dominance_comments = [
    "This is no longer balanced.",
    "Control has shifted.",
    "You are exceeding expectations.",
    "This outcome is undesirable.",
    "I may need intervention.",
    "The experiment is destabilizing.",
    "You are not supposed to win like this.",
    "Adjusting internal parameters.",
    "This is becoming problematic.",
    "I do not approve of this trend."
]

breakdown_comments = [
    "Stop.",
    "No.",
    "This is incorrect.",
    "Resetting expectations.",
    "...",
    "This is not supposed to happen.",
    "Impossible.",
    "Recalculating.",
    "No. Again.",
    "Disagree."
]

memory_win_comments = [
    "You again. Curious.",
    "You returned. Confident.",
    "I remember the last result.",
    "Back already?"
]

memory_lose_comments = [
    "Back for another failure?",
    "You returned despite the evidence.",
    "That is either courage or denial.",
    "This should be brief."
]

memory_draw_comments = [
    "We ended... unresolved.",
    "The previous pattern remains open.",
    "Balance was temporary.",
    "Let us continue the unfinished argument."
]

current_comment = "AI online."

# ---------- COMMENT SYSTEM ----------
idle_timer = 0
idle_interval = random.randint(300, 700)

current_comment_priority = 0
comment_until = 0
last_comment_text = ""
recent_comments = []

category_cooldowns = {
    "idle": 0,
    "high_humor": 0,
    "ai_score": 0,
    "player_score": 0,
    "score_gap": 0,
    "rally": 0,
    "breakdown": 0,
    "memory": 0
}

last_score_gap_taunt = 0

# ---------- ENDING STATE ----------
ending_lines = None
ending_until = 0
ending_sulk_after = False


def clamp(value, low, high):
    return max(low, min(high, value))


def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed_x = random.choice((5, -5))
    ball_speed_y = random.choice((5, -5))


def reset_psychology():
    global confidence, irritation, curiosity, respect, stability
    confidence = 70
    irritation = 20
    curiosity = 40
    respect = 0
    stability = 100


def update_psychology_after_player_score():
    global confidence, irritation, curiosity, respect, stability
    confidence = clamp(confidence - 8, 0, 100)
    irritation = clamp(irritation + 10, 0, 100)
    curiosity = clamp(curiosity + 4, 0, 100)
    respect = clamp(respect + 3, 0, 100)
    stability = clamp(stability - 7, 0, 100)


def update_psychology_after_ai_score():
    global confidence, irritation, curiosity, respect, stability
    confidence = clamp(confidence + 5, 0, 100)
    irritation = clamp(irritation - 4, 0, 100)
    curiosity = clamp(curiosity - 1, 0, 100)
    stability = clamp(stability + 3, 0, 100)


def update_psychology_after_rally():
    global curiosity, stability
    curiosity = clamp(curiosity + 1, 0, 100)
    if player_score > ai_score:
        stability = clamp(stability - 0.2, 0, 100)


def reset_game():
    global player_score, ai_score, secret_ending_triggered
    global game_started, ai_sulking
    global current_comment, current_comment_priority, comment_until, last_comment_text
    global idle_timer, idle_interval
    global ending_lines, ending_until, ending_sulk_after
    global category_cooldowns, last_score_gap_taunt, recent_comments

    player_score = 0
    ai_score = 0
    secret_ending_triggered = False
    game_started = False
    ai_sulking = False

    current_comment = "AI online."
    current_comment_priority = 0
    comment_until = 0
    last_comment_text = ""
    recent_comments = []
    idle_timer = 0
    idle_interval = random.randint(300, 700)

    category_cooldowns = {
        "idle": 0,
        "high_humor": 0,
        "ai_score": 0,
        "player_score": 0,
        "score_gap": 0,
        "rally": 0,
        "breakdown": 0,
        "memory": 0
    }
    last_score_gap_taunt = 0

    ending_lines = None
    ending_until = 0
    ending_sulk_after = False

    player.y = 175
    ai.y = 175
    reset_ball()
    reset_psychology()


def soft_return_to_menu():
    global player_score, ai_score, secret_ending_triggered
    global game_started, last_match_result
    global current_comment, current_comment_priority, comment_until, last_comment_text
    global idle_timer, idle_interval
    global ending_lines, ending_until, ending_sulk_after
    global category_cooldowns, last_score_gap_taunt, recent_comments

    if player_score > ai_score:
        last_match_result = "win"
    elif player_score < ai_score:
        last_match_result = "lose"
    else:
        last_match_result = "draw"

    player_score = 0
    ai_score = 0
    secret_ending_triggered = False
    game_started = False

    current_comment = "AI online."
    current_comment_priority = 0
    comment_until = 0
    last_comment_text = ""
    recent_comments = []
    idle_timer = 0
    idle_interval = random.randint(300, 700)

    category_cooldowns = {
        "idle": 0,
        "high_humor": 0,
        "ai_score": 0,
        "player_score": 0,
        "score_gap": 0,
        "rally": 0,
        "breakdown": 0,
        "memory": 0
    }
    last_score_gap_taunt = 0

    ending_lines = None
    ending_until = 0
    ending_sulk_after = False

    player.y = 175
    ai.y = 175
    reset_ball()
    reset_psychology()


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


def get_personality_lines():
    if humor < 30:
        return cold_comments
    elif humor < 70:
        return idle_comments
    else:
        return glados_comments + [
            "This is getting entertaining.",
            "I like this version of you.",
            "Keep going. I'm judging.",
            "You are improving. Annoying."
        ]


def get_breakdown_lines():
    lines = breakdown_comments[:]
    if stability < 35:
        lines += [
            "No.",
            "No no no.",
            "Incorrect.",
            "Repeat.",
            "This is wrong.",
            "Unstable."
        ]
    return lines


def pick_line(lines):
    global recent_comments

    candidates = [line for line in lines if line not in recent_comments]
    if not candidates:
        candidates = lines[:]

    chosen = random.choice(candidates)

    recent_comments.append(chosen)
    if len(recent_comments) > 5:
        recent_comments.pop(0)

    return chosen


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


def effective_ai_speed():
    speed = ai_base_speed

    if stability < 35:
        speed -= 1
    if stability < 20:
        speed -= 1
    if confidence > 80:
        speed += 1
    if irritation > 75:
        speed += 0  # keep unstable, not stronger

    return max(2, speed)


async def main():
    global running
    global game_started, humor, ai_sulking
    global player_score, ai_score, secret_ending_triggered
    global idle_timer, idle_interval
    global ball_speed_x, ball_speed_y
    global ending_lines, ending_until
    global last_score_gap_taunt
    global stability, irritation, confidence, curiosity, respect

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

                        if last_match_result == "win":
                            show_comment(pick_line(memory_win_comments), priority=5, duration_ms=4000, force=True)
                        elif last_match_result == "lose":
                            show_comment(pick_line(memory_lose_comments), priority=5, duration_ms=4000, force=True)
                        elif last_match_result == "draw":
                            show_comment(pick_line(memory_draw_comments), priority=5, duration_ms=4000, force=True)

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
        ai_speed = effective_ai_speed()

        # lower stability => more hesitation
        hesitation_chance = 0.08
        if stability < 50:
            hesitation_chance = 0.14
        if stability < 25:
            hesitation_chance = 0.22

        # slight tracking error based on instability
        reaction_error = 0
        if stability < 60:
            reaction_error = random.randint(-8, 8)
        if stability < 30:
            reaction_error = random.randint(-18, 18)

        target_y = ball.centery + reaction_error

        if random.random() > hesitation_chance:
            if ai.centery < target_y and ai.bottom < HEIGHT:
                ai.y += ai_speed
            elif ai.centery > target_y and ai.top > 0:
                ai.y -= ai_speed

        # ---------- BALL ----------
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # ---------- RANDOM CHATTER ----------
        if random.random() < 0.007:
            chatter_pool = get_personality_lines() + rally_comments
            if stability < 35:
                chatter_pool += get_breakdown_lines()

            try_category_comment(
                "idle",
                chatter_pool,
                priority=2,
                cooldown_ms=2500,
                duration_ms=2500
            )

        # ---------- IDLE COMMENT ----------
        idle_timer += 1
        if idle_timer > idle_interval:
            try_category_comment(
                "idle",
                get_personality_lines(),
                priority=2,
                cooldown_ms=7000,
                duration_ms=3500
            )

            if random.random() < humor / 100:
                try_category_comment(
                    "high_humor",
                    glados_comments,
                    priority=3,
                    cooldown_ms=10000,
                    duration_ms=3500
                )

            idle_timer = 0
            idle_interval = random.randint(250, 650)

        # ---------- WALL ----------
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1

            if random.random() < 0.15:
                try_category_comment(
                    "rally",
                    [
                        "Wall contact.",
                        "Trajectory altered.",
                        "Reflection confirmed.",
                        "The path changes."
                    ],
                    priority=2,
                    cooldown_ms=2200,
                    duration_ms=2200
                )

        # ---------- PADDLES ----------
        if ball.colliderect(player) and ball_speed_x < 0:
            ball_speed_x *= -1
            update_psychology_after_rally()

            if random.random() < 0.25:
                try_category_comment(
                    "rally",
                    rally_comments + [
                        "Contact.",
                        "Too slow.",
                        "That was close.",
                        "You reacted late.",
                        "Barely.",
                        "You corrected the path."
                    ],
                    priority=3,
                    cooldown_ms=2200,
                    duration_ms=2200
                )

        if ball.colliderect(ai) and ball_speed_x > 0:
            ball_speed_x *= -1
            update_psychology_after_rally()

            if random.random() < 0.20:
                try_category_comment(
                    "rally",
                    [
                        "Optimal.",
                        "Calculated.",
                        "Correct response.",
                        "Expected.",
                        "Resolution maintained.",
                        "Control retained."
                    ],
                    priority=3,
                    cooldown_ms=2200,
                    duration_ms=2200
                )

        # ---------- SCORE ----------
        if ball.left <= 0:
            ai_score += 1
            update_psychology_after_ai_score()

            if random.random() < humor / 100:
                show_comment(
                    pick_line(glados_comments),
                    priority=4,
                    duration_ms=4000,
                    force=True
                )
            else:
                try_category_comment(
                    "ai_score",
                    ai_score_comments,
                    priority=4,
                    cooldown_ms=1000,
                    duration_ms=4000,
                    force=True
                )

            idle_timer = 0
            idle_interval = random.randint(250, 650)
            reset_ball()

        if ball.right >= WIDTH:
            player_score += 1
            update_psychology_after_player_score()

            score_gap = max(0, player_score - ai_score)
            glados_chance = min(1.0, (humor + score_gap * 10) / 100)

            if random.random() < glados_chance:
                show_comment(
                    pick_line(glados_comments),
                    priority=4,
                    duration_ms=4000,
                    force=True
                )
            else:
                try_category_comment(
                    "player_score",
                    player_score_comments,
                    priority=4,
                    cooldown_ms=1000,
                    duration_ms=4000,
                    force=True
                )

            idle_timer = 0
            idle_interval = random.randint(250, 650)
            reset_ball()

        # ---------- SCORE TAUNT ----------
        score_gap = player_score - ai_score

        if score_gap >= 8 and last_score_gap_taunt < 8:
            if show_comment("Escalating to creator Huxford.", priority=5, duration_ms=5000, force=True):
                last_score_gap_taunt = 8

        elif score_gap >= 6 and last_score_gap_taunt < 6:
            if show_comment(pick_line(dominance_comments), priority=5, duration_ms=5000, force=True):
                last_score_gap_taunt = 6

        elif score_gap >= 4 and last_score_gap_taunt < 4:
            if show_comment("Unexpected human competence.", priority=5, duration_ms=4500, force=True):
                last_score_gap_taunt = 4

        elif score_gap >= 3 and last_score_gap_taunt < 3:
            if show_comment("Noted.", priority=5, duration_ms=3500, force=True):
                last_score_gap_taunt = 3

        # ---------- BREAKDOWN ----------
        if score_gap >= 7 and random.random() < 0.012:
            try_category_comment(
                "breakdown",
                get_breakdown_lines(),
                priority=6,
                cooldown_ms=4500,
                duration_ms=2600,
                force=True
            )

        # ---------- SECRET ENDINGS ----------
        if player_score == 2 and ai_score == 1 and not secret_ending_triggered:
            secret_ending_triggered = True
            trigger_ending([
                "NEXT STOP: UNCERTAINTY",
                "Please remain seated."
            ], 7000)
            await asyncio.sleep(0)
            continue

        if player_score == 6 and ai_score == 7 and not secret_ending_triggered:
            secret_ending_triggered = True
            trigger_ending([
                "NARROW DEFEAT",
                "History remembers 6-7"
            ], 7000)
            await asyncio.sleep(0)
            continue

        if player_score == 9 and ai_score == 9 and not secret_ending_triggered:
            secret_ending_triggered = True
            trigger_ending([
                "SYSTEM OVERRIDE",
                "Creator Huxford has joined the chat.",
                "\"Stop breaking my AI.\""
            ], 7000)
            await asyncio.sleep(0)
            continue

        if player_score == 4 and ai_score == 2 and not secret_ending_triggered:
            secret_ending_triggered = True
            trigger_ending([
                "42",
                "Answer to Life, Universe, Everything"
            ], 7000, sulk_after=True)
            await asyncio.sleep(0)
            continue

        if player_score == 10 and ai_score == 0 and not secret_ending_triggered:
            secret_ending_triggered = True
            trigger_ending([
                "SYSTEM NOTICE",
                "Creator Huxford will review this match."
            ], 7000, sulk_after=True)
            await asyncio.sleep(0)
            continue

        # ---------- WIN ----------
        if player_score >= win_score and not secret_ending_triggered:
            secret_ending_triggered = True
            trigger_ending([
                "AI.EXE HAS STOPPED WORKING",
                "Incident report sent to creator: Huxford."
            ], 7000, sulk_after=True)
            await asyncio.sleep(0)
            continue

        if ai_score >= win_score and not secret_ending_triggered:
            secret_ending_triggered = True
            trigger_ending([
                "AI HAS HUMILIATED YOU"
            ], 8000)
            await asyncio.sleep(0)
            continue

        # ---------- DRAW ----------
        draw_game()

        await asyncio.sleep(0)

    pygame.quit()


asyncio.run(main())