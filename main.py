import pygame
import random
import sys
from config import WIDTH, HEIGHT, FPS, BLACK, WHITE, font
from game_objects import Rocket, Bullet, FallingObject

# Pygameの初期化
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rocket Game")
clock = pygame.time.Clock()

# ゲームオブジェクトの初期化
rocket = Rocket("rocket.png")
bullets = []
falling_objects = []
skills = []

# スコアと時間
score = 0
time_limit = 30  # ゲームの制限時間 (秒)
game_start_ticks = pygame.time.get_ticks()

# 降ってくる物体用の画像リスト
falling_object_images = ["hanba-ga-.png", "itigopafe.png", "kakigoori.png",
                         "ke-ki.png", "meron.png", "ra-men.png", "tomato.png", "warabimoti.png"]

# メインゲームループ
running = True
while running:
  screen.fill(BLACK)

  # イベント処理
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
      bullets.append(Bullet(rocket.rect.centerx - 2.5, rocket.rect.top))

  # キー入力処理
  keys = pygame.key.get_pressed()
  rocket.move(keys)

  # 弾の更新
  for bullet in bullets[:]:
    bullet.move()
    if bullet.rect.y < 0:
      bullets.remove(bullet)

  # 降ってくる物体の生成
  if random.randint(1, 30) == 1:
    falling_objects.append(FallingObject(random.randint(
        0, WIDTH - 30), 0, image_paths=falling_object_images))

  # スキルアイテムの生成
  if random.randint(1, 100) == 1:  # スキルアイテムは低確率で生成
    skills.append(FallingObject(random.randint(0, WIDTH - 40),
                  0, image_path="star.png", width=50, height=50))

  # 弾と物体の衝突判定
  for bullet in bullets[:]:
    for obj in falling_objects[:]:
      if bullet.rect.colliderect(obj.rect):
        bullets.remove(bullet)
        falling_objects.remove(obj)
        score += 10
        break

  # 弾とスキルアイテムの衝突判定
  for bullet in bullets[:]:
    for skill in skills[:]:
      if bullet.rect.colliderect(skill.rect):
        bullets.remove(bullet)
        skills.remove(skill)
        score += 50
        break

  # 物体の更新
  for obj in falling_objects[:]:
    obj.move()
    if obj.rect.y > HEIGHT:
      falling_objects.remove(obj)

  for skill in skills[:]:
    skill.move()
    if skill.rect.y > HEIGHT:
      skills.remove(skill)

  # 描画
  rocket.draw(screen)
  for bullet in bullets:
    bullet.draw(screen)
  for obj in falling_objects:
    obj.draw(screen)
  for skill in skills:
    skill.draw(screen)

  # スコア表示
  score_text = font.render(f"Score: {score}", True, WHITE)
  screen.blit(score_text, (10, 10))

  # 残り時間表示
  elapsed_time = (pygame.time.get_ticks() - game_start_ticks) / 1000
  remaining_time = max(0, time_limit - int(elapsed_time))
  time_text = font.render(f"Time: {remaining_time}s", True, WHITE)
  screen.blit(time_text, (WIDTH - 150, 10))

  # ゲーム終了判定
  if remaining_time <= 0:
    running = False

  # 画面を更新
  pygame.display.flip()
  clock.tick(FPS)

# 終了メッセージ
screen.fill(BLACK)
end_text = font.render(f"Time up! Score: {score}", True, WHITE)
screen.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 2))
pygame.display.flip()
pygame.time.wait(3000)

# Pygameの終了
pygame.quit()
sys.exit()
