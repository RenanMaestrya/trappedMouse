import pygame
import sys
import time

def load_level(file_path):
    with open(file_path, 'r') as file:
        level_data = [line.strip() for line in file]

    width, height = map(int, level_data[0].split())
    level_matrix = [[int(tile) if tile.isdigit() else tile for tile in line] for line in level_data[1:]]
    
    return width, height, level_matrix

def load_images():
    wall_image = pygame.image.load("assets/wallsemFundo.png")
    path_image = pygame.image.load("assets/way32.png")
    finish_line_image = pygame.image.load("assets/island.png")

    player_up = pygame.image.load("assets/shipUp.png")
    player_down = pygame.image.load("assets/shipDown.png")
    player_left = pygame.image.load("assets/shipLeft.png")
    player_right = pygame.image.load("assets/shipRight.png")

    # Redimensiona as imagens do jogador para 32x32 pixels
    player_up = pygame.transform.scale(player_up, (32, 32))
    player_down = pygame.transform.scale(player_down, (32, 32))
    player_left = pygame.transform.scale(player_left, (32, 32))
    player_right = pygame.transform.scale(player_right, (32, 32))

    return wall_image, path_image, player_up, player_down, player_left, player_right, finish_line_image

def draw_finish_line(screen, level_matrix, images):
    block_size = min(screen.get_width() // len(level_matrix[0]), screen.get_height() // len(level_matrix))

    for y, row in enumerate(level_matrix):
        for x, tile in enumerate(row):
            rect = pygame.Rect(x * block_size, y * block_size, block_size, block_size)
            if tile == 'c':
                screen.blit(images[6], rect)  # Linha de chegada

def draw_level(screen, level_matrix, images):
    block_size = 32

    for y, row in enumerate(level_matrix):
        for x, tile in enumerate(row):
            rect = pygame.Rect(x * block_size, y * block_size, block_size, block_size)
            if tile == 1:
                screen.blit(images[0], rect)  # Parede
            elif tile == 0:
                screen.blit(images[1], rect)  # Caminho
            elif tile == 'm':
                direction = get_player_direction(level_matrix, x, y)
                if direction == 0:
                    screen.blit(images[2], rect)  # Jogador olhando para cima
                elif direction == 1:
                    screen.blit(images[3], rect)  # Jogador olhando para baixo
                elif direction == 2:
                    screen.blit(images[4], rect)  # Jogador olhando para a esquerda
                elif direction == 3:
                    screen.blit(images[5], rect)  # Jogador olhando para a direita
    draw_finish_line(screen, level_matrix, images)  # Desenha a linha de chegada

def get_player_direction(level_matrix, x, y):
    if y > 0 and level_matrix[y - 1][x] == 'm':
        return 0  # Direção para cima
    elif y < len(level_matrix) - 1 and level_matrix[y + 1][x] == 'm':
        return 1  # Direção para baixo
    elif x > 0 and level_matrix[y][x - 1] == 'm':
        return 2  # Direção para a esquerda
    elif x < len(level_matrix[y]) - 1 and level_matrix[y][x + 1] == 'm':
        return 3  # Direção para a direita
    else:
        return 0  # Caso padrão (para cima)

def move_player(level_matrix, current_pos, new_pos):
    if level_matrix[new_pos[1]][new_pos[0]] == 0:
        level_matrix[current_pos[1]][current_pos[0]] = 0
        level_matrix[new_pos[1]][new_pos[0]] = 'm'
        return True
    return False

block_size = 32

level_width, level_height, level_matrix = load_level("maze16x16.txt")
pygame.init()
screen = pygame.display.set_mode((level_width * block_size, level_height * block_size))
block_size = min(screen.get_width() // level_width, screen.get_height() // level_height)
screen.fill((0, 0, 255))

def main():
    clock = pygame.time.Clock()
    running = True
    dt = 0

    wall_image, path_image, player_up, player_down, player_left, player_right, finish_line_image = load_images()

    player_pos = pygame.Vector2(0, 0) 
    player_speed = 1 

    for y, row in enumerate(level_matrix):
        for x, tile in enumerate(row):
            if tile == 'm':
                player_pos = pygame.Vector2(x, y)  

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((59, 187, 255))  # Preenche a tela com a cor azul

        draw_level(screen, level_matrix, [wall_image, path_image, player_up, player_down, player_left, player_right, finish_line_image])

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            new_pos = player_pos - pygame.Vector2(0, player_speed)
            if move_player(level_matrix, (int(player_pos.x), int(player_pos.y)), (int(new_pos.x), int(new_pos.y))):
                player_pos = new_pos
        if keys[pygame.K_s]:
            new_pos = player_pos + pygame.Vector2(0, player_speed)
            if move_player(level_matrix, (int(player_pos.x), int(player_pos.y)), (int(new_pos.x), int(new_pos.y))):
                player_pos = new_pos
        if keys[pygame.K_a]:
            new_pos = player_pos - pygame.Vector2(player_speed, 0)
            if move_player(level_matrix, (int(player_pos.x), int(player_pos.y)), (int(new_pos.x), int(new_pos.y))):
                player_pos = new_pos
        if keys[pygame.K_d]:
            new_pos = player_pos + pygame.Vector2(player_speed, 0)
            if move_player(level_matrix, (int(player_pos.x), int(player_pos.y)), (int(new_pos.x), int(new_pos.y))):
                player_pos = new_pos

        if level_matrix[int(player_pos.y)][int(player_pos.x)] == 'c':
            print("Parabéns! Você chegou à linha de chegada!")
            time.sleep(4)  # Aguarda 4 segundos
            running = False  # Encerra o jogo

        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
