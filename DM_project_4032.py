import pygame
import asyncio
import platform
import random
from enum import Enum
from typing import List, Tuple
from collections import deque
import heapq

# Screen and grid constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
TILE_SIZE = 40
ROWS = SCREEN_HEIGHT // TILE_SIZE
COLS = SCREEN_WIDTH // TILE_SIZE
FPS = 15
WALL_NUM = 35

PLAYER_COLOR = (0, 0, 255)  # Blue
TARGET_COLOR = (255, 0, 0)  # Red
WALL_COLOR = (50, 50, 50)   # Dark gray
GRID_COLOR = (200, 200, 200)  # Light gray
BACKGROUND_COLOR = (240, 240, 240)  # Very light gray
VICTORY_COLOR = (0, 255, 0)  # Green

# Define cell states
class CellState(Enum):
    EMPTY = 0
    WALL = 1
    PLAYER = 2
    TARGET = 3

# Initialize grid and walls
grid = [[CellState.EMPTY for _ in range(COLS)] for _ in range(ROWS)]
walls = []

# Pygame globals
screen = None
player_image = None
target_image = None
wall_image = None
victory_image = None

#########
######### TODO FUNCTIONS:
#########

# search algorithm functions (replace with your actual implementations)

def dfs_make_move(grid: List[List[CellState]],player_pos: Tuple[int, int],target_pos: Tuple[int, int]) -> Tuple[int, int]:
    
    if not hasattr(dfs_make_move, 'path'):
        dfs_make_move.path = []
        dfs_make_move.visited = set()
    
    path = dfs_make_move.path
    visited = dfs_make_move.visited
    
    if not path_exists(grid, player_pos, target_pos):
        print("The target is unavailable!")
        return player_pos
    
    if path and player_pos != path[-1] and target_pos!=path[0]:
        path.clear()
        visited.clear()

    if not path:
        path.append(player_pos)
        visited.add(player_pos)
    
    current = path[-1]

    neighbors = [(current[0]-1, current[1]),(current[0], current[1]+1),(current[0]+1, current[1]),(current[0], current[1]-1)]

    next_pos = None
    for neighbor in neighbors:
        if (0 <= neighbor[0] < ROWS and 
            0 <= neighbor[1] < COLS and
            grid[neighbor[0]][neighbor[1]] != CellState.WALL and 
            neighbor not in visited):
            next_pos = neighbor
            break
    if next_pos:
        visited.add(next_pos)
        path.append(next_pos)
    else:
        if len(path) > 1:
            path.pop() 
            next_pos = path[-1] 
        else:
            next_pos = current
    
    return next_pos



def bfs_make_move(grid: List[List[CellState]],player_pos: Tuple[int, int],target_pos: Tuple[int, int]) -> Tuple[int, int]:
    if not hasattr(bfs_make_move, 'queue'):
        bfs_make_move.queue = deque()
        bfs_make_move.visited = set()
        bfs_make_move.parent = {}
        bfs_make_move.path = []
        bfs_make_move.last_player_pos = player_pos
    
    queue = bfs_make_move.queue
    visited = bfs_make_move.visited
    parent = bfs_make_move.parent
    path = bfs_make_move.path
    last_player_pos = bfs_make_move.last_player_pos


    if not path_exists(grid, player_pos, target_pos):
        print("The target is unavailable!")
        return player_pos

    if player_pos != last_player_pos:
        queue.clear()
        visited.clear()
        parent.clear()
        path.clear()
        bfs_make_move.last_player_pos = player_pos
    
    if not queue:
        queue.append(player_pos)
        visited.add(player_pos)
        parent[player_pos] = None
    
    if path:
        return path.pop(0)
    
    while queue:
        current = queue.popleft()
        if current == target_pos:
            temp = current
            full_path = []
            while temp != player_pos:
                full_path.append(temp)
                temp = parent[temp]
            full_path.reverse()
            bfs_make_move.path = full_path
            
            if path:
                return path.pop(0)
            return player_pos

        neighbors = [(current[0]-1, current[1]),(current[0], current[1]+1),(current[0]+1, current[1]),(current[0], current[1]-1)]

        for neighbor in neighbors:
            if (0 <= neighbor[0] < ROWS and 
                0 <= neighbor[1] < COLS and
                grid[neighbor[0]][neighbor[1]] != CellState.WALL and
                neighbor not in visited):
                visited.add(neighbor)
                queue.append(neighbor)
                parent[neighbor] = current
    
    return player_pos



def a_star_make_move(grid: List[List[CellState]], player_pos: Tuple[int, int], target_pos: Tuple[int, int]) -> Tuple[int, int]:
    if not hasattr(a_star_make_move, 'path'):
        a_star_make_move.path = []
        a_star_make_move.parent = {}
        a_star_make_move.open_set = []
        a_star_make_move.closed_set = set()
        a_star_make_move.g_score = {}
        a_star_make_move.f_score = {}
        a_star_make_move.last_player_pos = player_pos
    
    path = a_star_make_move.path
    parent = a_star_make_move.parent
    open_set = a_star_make_move.open_set
    closed_set = a_star_make_move.closed_set
    g_score = a_star_make_move.g_score 
    f_score = a_star_make_move.f_score
    last_player_pos = a_star_make_move.last_player_pos

    if not path_exists(grid, player_pos, target_pos):
        print("The target is unavalible!")
        return player_pos

    if player_pos != last_player_pos:
        path.clear()
        parent.clear()
        open_set.clear()
        closed_set.clear()
        g_score.clear()
        f_score.clear()
        a_star_make_move.last_player_pos = player_pos
    
    if path:
        return path.pop(0)
    
    if not open_set:
        g_score[player_pos] = 0
        f_score[player_pos] = h(player_pos, target_pos)
        heapq.heappush(open_set, (f_score[player_pos], player_pos))
        parent[player_pos] = None
    
    if open_set:
        current_node = heapq.heappop(open_set)
        current = current_node[1]
        if current == target_pos:
            full_path = []
            temp = current
            while temp != player_pos:
                full_path.append(temp)
                temp = parent[temp]
            full_path.reverse()
            a_star_make_move.path = full_path

            if full_path:
                return full_path.pop(0)
            return player_pos
        
        closed_set.add(current)

        neighbors = [(current[0]-1, current[1]), (current[0], current[1]+1),(current[0]+1, current[1]),(current[0], current[1]-1) ]

        for neighbor in neighbors:
            if (0 <= neighbor[0] < ROWS and
                0 <= neighbor[1] < COLS and
                grid[neighbor[0]][neighbor[1]] != CellState.WALL and 
                neighbor not in closed_set):

                if neighbor not in g_score.keys() or g_score.get(current) + 1<g_score.get(neighbor):
                    parent[neighbor] = current
                    g_score[neighbor] = g_score.get(current) + 1
                    neighbor_fscore = (g_score.get(current) + 1) + h(neighbor, target_pos)
                    f_score[neighbor] = neighbor_fscore
                    heapq.heappush(open_set, (neighbor_fscore, neighbor))
    

    return player_pos


def bidi_a_star_make_move(grid: List[List[CellState]], player_pos: Tuple[int, int],target_pos: Tuple[int, int]) -> Tuple[Tuple[int, int], Tuple[int, int]]:

    if not hasattr(bidi_a_star_make_move, 'forward_open'):
        #for player
        bidi_a_star_make_move.forward_open = []
        bidi_a_star_make_move.forward_closed = set()
        bidi_a_star_make_move.forward_g = {}
        bidi_a_star_make_move.forward_f = {}
        bidi_a_star_make_move.forward_parent = {}
        bidi_a_star_make_move.player_path = []
        bidi_a_star_make_move.last_player_pos = player_pos
        
        #for target
        bidi_a_star_make_move.backward_open = []
        bidi_a_star_make_move.backward_closed = set()
        bidi_a_star_make_move.backward_g = {}
        bidi_a_star_make_move.backward_f = {}
        bidi_a_star_make_move.backward_parent = {}
        bidi_a_star_make_move.target_path = []
        bidi_a_star_make_move.last_target_pos = target_pos
        
        #common
        bidi_a_star_make_move.meeting_point = None
        bidi_a_star_make_move.met = False


    forward_open=bidi_a_star_make_move.forward_open
    forward_closed=bidi_a_star_make_move.forward_closed
    forward_g=bidi_a_star_make_move.forward_g
    forward_f=bidi_a_star_make_move.forward_f
    forward_parent=bidi_a_star_make_move.forward_parent
    backward_open=bidi_a_star_make_move.backward_open
    backward_closed=bidi_a_star_make_move.backward_closed
    backward_g=bidi_a_star_make_move.backward_g
    backwaed_f=bidi_a_star_make_move.backward_f
    backward_parent=bidi_a_star_make_move.backward_parent
    player_path=bidi_a_star_make_move.player_path
    target_path=bidi_a_star_make_move.target_path
    last_player_pos=bidi_a_star_make_move.last_player_pos 
    last_target_pos=bidi_a_star_make_move.last_target_pos 
    

    if not path_exists(grid, player_pos, target_pos):
        print("The target is unavailable!")
        return player_pos
    
    if (player_pos != last_player_pos or
        target_pos != last_target_pos):
        forward_open.clear()
        forward_closed.clear()
        forward_g.clear()
        forward_f.clear()
        forward_parent.clear()
        backward_open.clear()
        backward_closed.clear()
        backward_g.clear()
        backwaed_f.clear()
        backward_parent.clear()
        bidi_a_star_make_move.meeting_point = None
        player_path.clear()
        target_path.clear()
        bidi_a_star_make_move.last_player_pos = player_pos
        bidi_a_star_make_move.last_target_pos = target_pos
        bidi_a_star_make_move.met = False
    
    if bidi_a_star_make_move.met:
        return player_pos, target_pos
    
    if player_path and target_path:
        next_player = player_path.pop(0)
        next_target = target_path.pop(0)
        
        if next_player == next_target:
            bidi_a_star_make_move.met = True
        return next_player, next_target
    
    if not forward_open:
        forward_g[player_pos] = 0
        forward_f[player_pos] = h(player_pos, target_pos)
        heapq.heappush(forward_open, (forward_f[player_pos], player_pos))
        forward_parent[player_pos] = None
        
        backward_g[target_pos] = 0
        backwaed_f[target_pos] = h(target_pos, player_pos)
        heapq.heappush(backward_open, (backwaed_f[target_pos], target_pos))
        backward_parent[target_pos] = None
    
    if forward_open and backward_open:
        current_nodef = heapq.heappop(forward_open)
        f_current = current_nodef[1]
        
        current_nodeb = heapq.heappop(backward_open)
        b_current=current_nodeb[1]

        common = forward_closed & backward_closed
        if common:
            bidi_a_star_make_move.meeting_point = min(common, 
                key=lambda pos: 
                    forward_g.get(pos) + 
                    backward_g.get(pos))
            
        if bidi_a_star_make_move.meeting_point:
            full_pathf = []
            current = bidi_a_star_make_move.meeting_point
            while current != player_pos:
                full_pathf.append(current)
                current = forward_parent[current]
            full_pathf.reverse()
            bidi_a_star_make_move.player_path=full_pathf

            full_pathb = []
            current = bidi_a_star_make_move.meeting_point
            while current != target_pos:
                full_pathb.append(current)
                current = backward_parent[current]
            full_pathb.reverse()
            bidi_a_star_make_move.target_path=full_pathb

            if full_pathf and full_pathb:
                next_player = full_pathf.pop(0)
                next_target = full_pathb.pop(0)
                
                if next_player == next_target:
                    bidi_a_star_make_move.met = True
                return next_player, next_target
    
        forward_closed.add(f_current)
        backward_closed.add(b_current)

        neighbors = [(f_current[0]-1, f_current[1]), (f_current[0], f_current[1]+1),(f_current[0]+1, f_current[1]),(f_current[0], f_current[1]-1) ]

        for neighbor in neighbors:
            if (0 <= neighbor[0] < ROWS and
                0 <= neighbor[1] < COLS and
                grid[neighbor[0]][neighbor[1]] != CellState.WALL and
                neighbor not in forward_closed):

                if neighbor not in forward_g.keys() or forward_g.get(f_current) + 1<forward_g.get(neighbor):
                    forward_parent[neighbor] = f_current
                    forward_g[neighbor] =forward_g.get(f_current) + 1
                    neighbor_fscore=(forward_g.get(f_current) + 1) + h(neighbor, target_pos)
                    forward_f[neighbor] = neighbor_fscore
                    heapq.heappush(forward_open, (neighbor_fscore, neighbor))
        
        neighbors = [(b_current[0]-1, b_current[1]), (b_current[0], b_current[1]+1),(b_current[0]+1, b_current[1]),(b_current[0], b_current[1]-1) ]

        for neighbor in neighbors:
            if (0 <= neighbor[0] < ROWS and
                0 <= neighbor[1] < COLS and
                grid[neighbor[0]][neighbor[1]] != CellState.WALL and
                neighbor not in backward_closed):

                if neighbor not in backward_g.keys() or backward_g.get(b_current) + 1<backward_g.get(neighbor):
                    backward_parent[neighbor] = b_current
                    backward_g[neighbor] =backward_g.get(b_current) + 1
                    neighbor_fscore=(backward_g.get(b_current) + 1) + h(neighbor, target_pos)
                    backwaed_f[neighbor] = neighbor_fscore
                    heapq.heappush(backward_open, (neighbor_fscore, neighbor))


    return player_pos, target_pos



def path_exists(grid, start, end):
    visited = set()
    queue = deque([start])
    
    while queue:
        current = queue.popleft()
        if current == end:
            return True
            
        neighbors = [(current[0]-1, current[1]), (current[0], current[1]+1),(current[0]+1, current[1]),(current[0], current[1]-1) ]
        for neighbor in neighbors:
            
            if (0 <= neighbor[0] < ROWS and 
                0 <= neighbor[1] < COLS and
                grid[neighbor[0]][neighbor[1]] != CellState.WALL and
                neighbor not in visited):
                visited.add(neighbor)
                queue.append(neighbor)
                
    return False

def h(pos1: Tuple[int, int], pos2: Tuple[int, int]):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


#########
#########
#########

# Array of move functions
move_funcs = [dfs_make_move, bfs_make_move, a_star_make_move]

def get_random_int(min_val: int = 0, max_val: int = 200) -> int:
    return random.randint(min_val, max_val)

def init_grid(num_walls: int) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    global grid, walls
    # Reset grid
    grid = [[CellState.EMPTY for _ in range(COLS)] for _ in range(ROWS)]
    walls = []

    # Place walls
    while num_walls > 0:
        p = (get_random_int(0, ROWS-1), get_random_int(0, COLS-1))
        if grid[p[0]][p[1]] == CellState.EMPTY:
            walls.append(p)
            grid[p[0]][p[1]] = CellState.WALL
            num_walls -= 1

    # Place player
    player_pos = None
    while not player_pos:
        p = (get_random_int(0, ROWS-1), get_random_int(0, COLS-1))
        if grid[p[0]][p[1]] == CellState.EMPTY:
            grid[p[0]][p[1]] = CellState.PLAYER
            player_pos = p

    # Place target
    target_pos = None
    while not target_pos:
        p = (get_random_int(0, ROWS-1), get_random_int(0, COLS-1))
        if grid[p[0]][p[1]] == CellState.EMPTY:
            grid[p[0]][p[1]] = CellState.TARGET
            target_pos = p

    return player_pos, target_pos

def valid_move(pos: Tuple[int, int], next_pos: Tuple[int, int]) -> bool:
    if (pos[0] >= ROWS or pos[0] < 0 or pos[1] >= COLS or pos[1] < 0 or
        next_pos[0] >= ROWS or next_pos[0] < 0 or next_pos[1] >= COLS or next_pos[1] < 0):
        return False

    if grid[pos[0]][pos[1]] == CellState.WALL or grid[next_pos[0]][next_pos[1]] == CellState.WALL:
        return False

    if (pos[0] - next_pos[0])**2 + (pos[1] - next_pos[1])**2 > 1:
        return False
    return True

def load_image(path: str, size: Tuple[int, int], fallback_color: Tuple[int, int, int]) -> pygame.Surface:
    try:
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, size)
        return image
    except pygame.error as e:
        print(f"Unable to load image {path}! Pygame Error: {e}")
        surf = pygame.Surface(size)
        surf.fill(fallback_color)
        return surf

def init_pygame():
    global screen, player_image, target_image, wall_image, victory_image
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Discrete Mathematics Project")

    # Load and scale images
    player_image = load_image("Player.png", (TILE_SIZE, TILE_SIZE), PLAYER_COLOR)
    target_image = load_image("Target.png", (TILE_SIZE, TILE_SIZE), TARGET_COLOR)
    wall_image = load_image("Wall.png", (TILE_SIZE, TILE_SIZE), WALL_COLOR)
    victory_image = load_image("Victory.png", (490, SCREEN_HEIGHT), VICTORY_COLOR)

    return True

def close_pygame():
    global screen, player_image, target_image, wall_image, victory_image
    player_image = None
    target_image = None
    wall_image = None
    victory_image = None
    pygame.quit()

async def main():
    global grid, walls
    if not init_pygame():
        print("Pygame could not initialize!")
        return

    # Get algorithm choice
    print("Which algorithm do you want to run? press the corresponding number:")
    print("1. DFS\n2. BFS\n3. A*\n4. Bidirectional A*")
    alg_num = int(input()) - 1
    print("Thanks! Now let's see how your algorithm in action!")

    player_pos, target_pos = init_grid(WALL_NUM)
    clock = pygame.time.Clock()

    running = True
    while running:
        start_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear screen
        screen.fill(BACKGROUND_COLOR)

        # Draw grid lines
        for row in range(ROWS):
            for col in range(COLS):
                rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, GRID_COLOR, rect, 1)

        # Draw walls
        for w in walls:
            wall_rect = pygame.Rect(w[1] * TILE_SIZE, w[0] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            screen.blit(wall_image, wall_rect)

        # Draw player
        player_rect = pygame.Rect(player_pos[1] * TILE_SIZE, player_pos[0] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        screen.blit(player_image, player_rect)

        # Draw target
        target_rect = pygame.Rect(target_pos[1] * TILE_SIZE, target_pos[0] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        screen.blit(target_image, target_rect)

        pygame.display.flip()

        if player_pos == target_pos:
            print("NICE JOB! Maybe you can pass this class after all.")
            victory_rect = pygame.Rect(70, 0, 490, SCREEN_HEIGHT)
            screen.blit(victory_image, victory_rect)
            pygame.display.flip()
            await asyncio.sleep(0.8)  # 800ms delay

            # Start anew
            player_pos, target_pos = init_grid(WALL_NUM)
            continue

        # Make move
        new_player_pos = player_pos
        new_target_pos = target_pos
        if alg_num < 3:
            new_player_pos = move_funcs[alg_num](grid, player_pos, target_pos)
        else:
            new_player_pos, new_target_pos = bidi_a_star_make_move(grid, player_pos, target_pos)

        # Validate moves
        if valid_move(player_pos, new_player_pos):
            grid[player_pos[0]][player_pos[1]] = CellState.EMPTY
            player_pos = new_player_pos
            grid[player_pos[0]][player_pos[1]] = CellState.PLAYER
        else:
            print(f"Player: Invalid move! Can't make this move {player_pos} -> {new_player_pos}! I'm going to stay here for this turn!")

        if valid_move(target_pos, new_target_pos):
            grid[target_pos[0]][target_pos[1]] = CellState.EMPTY
            target_pos = new_target_pos
            grid[target_pos[0]][target_pos[1]] = CellState.TARGET
        else:
            print(f"Target: Invalid move! Can't make this move {target_pos} -> {new_target_pos}! I'm going to stay here for this turn!")

        # Cap frame rate
        elapsed = pygame.time.get_ticks() - start_time
        delay = max(0, (1000 / FPS) - elapsed)
        await asyncio.sleep(delay / 1000)

    close_pygame()

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())
