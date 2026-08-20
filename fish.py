import math
import pygame
import random
import numpy as np

# 1. تهيئة اللعبة والصوت
pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()

WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("24/7 Live Stream - Musical Fish")
clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.SysFont('tahoma', 36, bold=True)

# --- نظام توليد الموسيقى البسيطة (النغمات) ---
# الترددات الأساسية لبعض النوتات الموسيقية (مقياس خماسي - Pentatonic Scale - لضمان تناغم الأصوات)
PENTATONIC_FREQS = [261.63, 293.66, 329.63, 392.00, 440.00, 523.25, 587.33, 659.25]

def generate_tone(frequency, duration=1.5, volume=0.1, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # توليد الموجة الصوتية الأساسية
    wave = np.sin(2 * np.pi * frequency * t)
    
    # إضافة تلاشي للصوت (Fade out) ليكون مثل الجرس
    envelope = np.exp(-3.0 * t / duration) 
    wave = wave * envelope
    
    # تحجيم الصوت
    audio_array = np.int16(wave * 32767 * volume)
    
    # تحويله لمسارين (Stereo)
    stereo_array = np.column_stack((audio_array, audio_array))
    
    return pygame.sndarray.make_sound(stereo_array)

# حدث مؤقت لعزف النغمات
MUSIC_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(MUSIC_EVENT, 1200) # عزف نغمة كل 1.2 ثانية
# ---------------------------------------------

# الألوان
COLOR_WATER_TOP = (135, 206, 235)
COLOR_WATER_BOTTOM = (10, 40, 70)
COLOR_BUBBLE = (173, 216, 230)
COLOR_FOOD = (255, 215, 0)
COLOR_TEXT = (255, 255, 255)

def create_gradient_surface(width, height, color1, color2):
    surface = pygame.Surface((width, height))
    for y in range(height):
        ratio = y / height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (width, y))
    return surface

background_gradient = create_gradient_surface(WIDTH, HEIGHT, COLOR_WATER_TOP, COLOR_WATER_BOTTOM)

def create_fish_surface(scale_factor=1.0):
    w, h = int(120 * scale_factor), int(60 * scale_factor)
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    def scale(val): return int(val * scale_factor)
    
    pygame.draw.polygon(surf, (0, 0, 0), [(scale(30), scale(30)), (scale(0), scale(10)), (scale(15), scale(30)), (scale(0), scale(50))])
    pygame.draw.polygon(surf, (0, 0, 0), [(scale(70), scale(15)), (scale(60), scale(2)), (scale(50), scale(15))])
    pygame.draw.polygon(surf, (0, 0, 0), [(scale(70), scale(45)), (scale(60), scale(58)), (scale(50), scale(45))])
    pygame.draw.ellipse(surf, (0, 0, 0), (scale(20), scale(15), scale(75), scale(30)))
    pygame.draw.lines(surf, (255, 255, 255), False, [(scale(35), scale(20)), (scale(60), scale(17)), (scale(85), scale(22))], scale(4))
    pygame.draw.lines(surf, (255, 255, 255), False, [(scale(35), scale(40)), (scale(60), scale(43)), (scale(85), scale(38))], scale(4))
    pygame.draw.lines(surf, (0, 100, 255), False, [(scale(35), scale(20)), (scale(60), scale(17)), (scale(85), scale(22))], scale(2))
    pygame.draw.lines(surf, (0, 100, 255), False, [(scale(35), scale(40)), (scale(60), scale(43)), (scale(85), scale(38))], scale(2))
    pygame.draw.circle(surf, (0, 0, 255), (scale(85), scale(20)), scale(4))
    pygame.draw.circle(surf, (0, 255, 255), (scale(85), scale(20)), scale(2))
    pygame.draw.circle(surf, (0, 0, 255), (scale(85), scale(40)), scale(4))
    pygame.draw.circle(surf, (0, 255, 255), (scale(85), scale(40)), scale(2))
    return surf

class Bubble:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(HEIGHT // 2, HEIGHT + 100)
        self.radius = random.randint(3, 10)
        self.speed = random.uniform(0.5, 2.5)

    def update(self):
        self.y -= self.speed
        if self.y < -self.radius * 2:
            self.x = random.randint(0, WIDTH)
            self.y = HEIGHT + random.randint(10, 100)

    def draw(self, surface):
        width = 1 if self.radius < 7 else 2
        pygame.draw.circle(surface, COLOR_BUBBLE, (int(self.x), int(self.y)), self.radius, width)

class Food:
    def __init__(self):
        self.spawn()
        self.size = 8
        
    def spawn(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = random.randint(50, HEIGHT - 50)
        
    def draw(self, surface):
        pygame.draw.polygon(surface, COLOR_FOOD, [
            (self.x, self.y - self.size), (self.x + self.size, self.y), 
            (self.x, self.y + self.size), (self.x - self.size, self.y)
        ])

class Fish:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 4.0 
        self.scale = 1.0 
        self.original_image = create_fish_surface(self.scale)
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def grow(self):
        if self.scale < 2.0: 
            self.scale += 0.05
            self.original_image = create_fish_surface(self.scale)
            
    def reset_size(self):
        self.scale = 1.0
        self.original_image = create_fish_surface(self.scale)

    def update(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.hypot(dx, dy)
        target_angle = math.degrees(math.atan2(-dy, dx))

        if distance > 10:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed

        self.image = pygame.transform.rotate(self.original_image, target_angle)
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

bubbles = [Bubble() for _ in range(35)]
fish = Fish(WIDTH // 2, HEIGHT // 2)
food = Food()
score = 0

running = True
pygame.mouse.set_visible(False) 

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        
        # عند إطلاق الحدث الزمني، قم بعزف نغمة عشوائية
        if event.type == MUSIC_EVENT:
            try:
                freq = random.choice(PENTATONIC_FREQS)
                tone = generate_tone(freq, duration=2.0, volume=0.08)
                tone.play()
            except Exception:
                pass # تجاهل الأخطاء إذا حدثت لكي لا يتوقف البث

    target_x, target_y = food.x, food.y

    for bubble in bubbles:
        bubble.update()
        
    fish.update(target_x, target_y)
    
    dist_to_food = math.hypot(fish.x - food.x, fish.y - food.y)
    capture_radius = 30 * fish.scale 
    
    if dist_to_food < capture_radius:
        score += 1
        fish.grow()
        food.spawn()
        
        if score > 1000:
            score = 0
            fish.reset_size()

    screen.blit(background_gradient, (0, 0))
    for bubble in bubbles:
        bubble.draw(screen)
    food.draw(screen)
    fish.draw(screen)

    score_text = font.render(f"Score: {score}", True, COLOR_TEXT)
    screen.blit(score_text, (20, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()