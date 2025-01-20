import pygame
import random
from config import WIDTH, HEIGHT

# ロケットクラス
class Rocket:
  def __init__(self, image_path):
    self.image = pygame.image.load(image_path)
    self.image = pygame.transform.scale(self.image, (80, 100))
    self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 70))
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
    self.rect = pygame.Rect(x, y, 10, 20)
    self.speed = -7

  def move(self):
    self.rect.y += self.speed

  def draw(self, screen):
    pygame.draw.rect(screen, (255, 255, 255), self.rect)


# 降ってくる物体クラス
class FallingObject:
  def __init__(self, x, y, color=None, width=60, height=60, image_paths=None, image_path=None):
    if image_path:  # 単一の画像を使用する場合
      self.image = pygame.image.load(image_path)
      self.image = pygame.transform.scale(self.image, (width, height))
      self.rect = self.image.get_rect(topleft=(x, y))
      self.has_image = True
    elif image_paths:  # 複数の画像リストが指定された場合
      chosen_image = random.choice(image_paths)
      self.image = pygame.image.load(chosen_image)
      self.image = pygame.transform.scale(self.image, (width, height))
      self.rect = self.image.get_rect(topleft=(x, y))
      self.has_image = True
    else:  # 画像が指定されていない場合
      self.rect = pygame.Rect(x, y, width, height)
      self.color = color if color else (random.randint(
          0, 255), random.randint(0, 255), random.randint(0, 255))
      self.has_image = False
    self.speed = 3

  def move(self):
    self.rect.y += self.speed

  def draw(self, screen):
    if self.has_image:
      screen.blit(self.image, self.rect.topleft)
    else:
      pygame.draw.rect(screen, self.color, self.rect)
