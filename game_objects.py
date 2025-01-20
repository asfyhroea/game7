import pygame
from config import WIDTH, HEIGHT, RED, WHITE, BLUE, GREEN

# ロケットクラス
class Rocket:
  def __init__(self, image_path):
    self.image = pygame.image.load(image_path)
    self.image = pygame.transform.scale(self.image, (80, 120))  # ロケット画像を拡大
    self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 100))
    self.speed = 5

  def move(self, keys):
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
      self.rect.x -= self.speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
      self.rect.x += self.speed
    self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))

  def draw(self, screen):
    screen.blit(self.image, self.rect.topleft)

# 弾クラス
class Bullet:
  def __init__(self, x, y):
    self.rect = pygame.Rect(x, y, 5, 10)
    self.speed = -7

  def move(self):
    self.rect.y += self.speed

  def draw(self, screen):
    pygame.draw.rect(screen, WHITE, self.rect)

# 降ってくる物体クラス
class FallingObject:
  def __init__(self, x, y, color, width=30, height=30):
    self.rect = pygame.Rect(x, y, width, height)
    self.speed = 3
    self.color = color

  def move(self):
    self.rect.y += self.speed

  def draw(self, screen):
    pygame.draw.rect(screen, self.color, self.rect)
