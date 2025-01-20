import pygame
import random
import sys

# Pygameの初期化
pygame.init()

# 画面設定
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rocket Game")

# 色設定
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# クロックとFPS設定
clock = pygame.time.Clock()
FPS = 60

# ロケットの設定
ROCKET_WIDTH, ROCKET_HEIGHT = 50, 30
rocket = pygame.Rect(WIDTH // 2, HEIGHT - 50, ROCKET_WIDTH, ROCKET_HEIGHT)
rocket_speed = 5

# 弾の設定
BULLET_WIDTH, BULLET_HEIGHT = 5, 10
bullets = []
bullet_speed = -7

# 降ってくる物体の設定
OBJ_WIDTH, OBJ_HEIGHT = 30, 30
objects = []
object_speed = 3
spawn_interval = 30  # フレーム間隔で生成

# スキルアップアイテムの設定
SKILL_WIDTH, SKILL_HEIGHT = 40, 40
skills = []
skill_active = False
skill_timer = 0
skill_duration = 300  # フレーム数で持続時間を設定

# スコア
score = 0
font = pygame.font.Font(None, 36)

# メインゲームループ
running = True
frame_count = 0
while running:
  screen.fill(BLACK)

  # イベント処理
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
      bullets.append(pygame.Rect(rocket.centerx - BULLET_WIDTH //
                     2, rocket.top, BULLET_WIDTH, BULLET_HEIGHT))

  # キー入力処理
  keys = pygame.key.get_pressed()
  if keys[pygame.K_LEFT] or keys[pygame.K_a]:
    rocket.x -= rocket_speed
  if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
    rocket.x += rocket_speed

  # ロケットを画面内に留める
  rocket.x = max(0, min(WIDTH - ROCKET_WIDTH, rocket.x))

  # 弾の更新
  for bullet in bullets[:]:
    bullet.y += bullet_speed
    if bullet.y < 0:
      bullets.remove(bullet)

  # 降ってくる物体の生成
  if frame_count % spawn_interval == 0:
    objects.append(pygame.Rect(random.randint(
        0, WIDTH - OBJ_WIDTH), 0, OBJ_WIDTH, OBJ_HEIGHT))
    if random.random() < 0.1:  # 10%の確率でスキルアップアイテムを生成
      skills.append(pygame.Rect(random.randint(
          0, WIDTH - SKILL_WIDTH), 0, SKILL_WIDTH, SKILL_HEIGHT))

  # 物体の更新
  for obj in objects[:]:
    obj.y += object_speed
    if obj.y > HEIGHT:
      objects.remove(obj)

  # スキルアップアイテムの更新
  for skill in skills[:]:
    skill.y += object_speed
    if skill.y > HEIGHT:
      skills.remove(skill)

  # 弾と物体の衝突判定
  for bullet in bullets[:]:
    for obj in objects[:]:
      if bullet.colliderect(obj):
        bullets.remove(bullet)
        objects.remove(obj)
        score += 10 if not skill_active else 20
        break

  # 弾とスキルアップアイテムの衝突判定
  for bullet in bullets[:]:
    for skill in skills[:]:
      if bullet.colliderect(skill):
        bullets.remove(bullet)
        skills.remove(skill)
        skill_active = True
        skill_timer = skill_duration
        break

  # スキルタイマーの更新
  if skill_active:
    skill_timer -= 1
    if skill_timer <= 0:
      skill_active = False

  # ロケットを描画
  pygame.draw.rect(screen, RED, rocket)

  # 弾を描画
  for bullet in bullets:
    pygame.draw.rect(screen, WHITE, bullet)

  # 物体を描画
  for obj in objects:
    pygame.draw.rect(screen, BLUE, obj)

  # スキルアップアイテムを描画
  for skill in skills:
    pygame.draw.rect(screen, GREEN, skill)

  # スコアを描画
  score_text = font.render(f"Score: {score}", True, WHITE)
  screen.blit(score_text, (10, 10))

  # 画面を更新
  pygame.display.flip()

  # フレームレートを維持
  clock.tick(FPS)
  frame_count += 1

# Pygameの終了
pygame.quit()
sys.exit()
