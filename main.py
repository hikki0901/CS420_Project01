from queue import PriorityQueue
from queue import Queue
import pygame

pygame.init()

WIDTH = 600
HEIGHT= 600


RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (15, 10, 222)
GREY = (128, 128, 128)
IRISBLUE = (0,181,204)

window = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Move your step")
font = pygame.font.Font('freesansbold.ttf',18)

# draw button to click algorithm
class Button:
    def __init__(self, x,y, text,click):
        self.x = x
        self.y = y
        self.text = text
        self.click = click
        self.draw()
        
    def draw(self):
        text_button = font.render(self.text,True,BLACK)
        button = pygame.rect.Rect((self.x,self.y),(120,50))
        if self.click:
            pygame.draw.rect(window,GREEN,button,0,5)
        else:
            pygame.draw.rect(window,IRISBLUE,button,0,5)
        window.blit(text_button,(self.x +20, self.y + 15))
    
    def is_click(self) -> bool:
        mouse = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        button = pygame.rect.Rect(self.x,self.y,120,50)
        if(left_click and button.collidepoint(mouse)):
            return True
        else:
            return False
        
    def set_click(self):
        self.click = True
        
    def remove_click(self):
        self.click = False
        
    def return_click(self) -> bool:
        return self.click
        

class Node:
    def __init__(self,irow,jcol, width, height, total_row, total_col) -> None:
        self.color = WHITE
        self.neighbor=[]
        self.width = width
        self.total_row = total_row
        self.x = irow
        self.y = jcol
        self.width = width
        self.height = height
        self.visited =[]
        self.total_col = total_col
    
    def get_pos(self):
        return self.x,self.y
        
    def draw(self, window):
        pygame.draw.rect(window,self.color,(self.y * self.width,self.x*self.height+100,self.width,self.height+100))
        
    def set_barrier_color(self):
        self.color = BLACK
    
    def set_end_color(self):
        self.color = BLUE
        
    def set_start_color(self):
        self.color = RED
    
    def set_nodeOpen_color(self):
        self.color = GREEN
        
    def set_nodeVisited_color(self):
        self.color = YELLOW
        
    def set_path_color(self):
        self.color = RED
    
    def set_unvisible(self):
        self.color =IRISBLUE
        
    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == RED
    
    def is_end(self):
        return self.color == BLUE
    
    def neighbors(self,grid):
        self.neighbor = []
        # move right - left - up - down
        if(self.x < self.total_row -1 and not grid[self.x+1][self.y].is_barrier()):
            self.neighbor.append(grid[self.x+1][self.y])
        if(self.x > 0 and not grid[self.x -1][self.y].is_barrier()):
            self.neighbor.append(grid[self.x -1][self.y])  
        if(self.y >0 and not grid[self.x][self.y -1].is_barrier()):
            self.neighbor.append(grid[self.x][self.y-1])
        if(self.y < self.total_col -1 and not grid[self.x][self.y + 1].is_barrier()):
            self.neighbor.append(grid[self.x][self.y+1])
        
        #   moving diagonally  
        if(self.x < self.total_row-1 and self.y >0 and not grid[self.x+1][self.y].is_barrier() and not grid[self.x][self.y-1].is_barrier() and not grid[self.x +1][self.y-1].is_barrier()):
            self.neighbor.append(grid[self.x+1][self.y-1])
        if(self.x < self.total_row-1 and self.y < self.total_col -1 and not grid[self.x+1][self.y].is_barrier() and not grid[self.x][self.y+1].is_barrier() and not grid[self.x +1][self.y+1].is_barrier()):
            self.neighbor.append(grid[self.x+1][self.y+1])
        if(self.x >0 and self.y > 0 and not grid[self.x-1][self.y].is_barrier() and not grid[self.x][self.y-1].is_barrier() and not grid[self.x -1][self.y-1].is_barrier()):
            self.neighbor.append(grid[self.x-1][self.y-1])
        if(self.x >0 and self.y <self.total_col -1 and not grid[self.x-1][self.y].is_barrier() and not grid[self.x][self.y+1].is_barrier() and not grid[self.x -1][self.y+1].is_barrier()):
            self.neighbor.append(grid[self.x-1][self.y+1])
            
    def __lt__(self,other):
        return False


def read_grid_from_file(file_path):
    grid = []
    with open(file_path,'r') as file:
        row , coloumn = map(int, file.readline().strip().split(','))
        
        floor = file.readline().strip().split(',')
        

        for i in range(row):
            data = file.readline().strip().split(',')
            grid.append(data)
            
    return row, coloumn,floor, grid
    
def make_grid_color(row,col,width,height, grid):
    grid_color =[]
    start = None
    end =None
    for i in range(row):
        grid_color.append([])
        for j in range(col):
            node = Node(i,j,width//col,height//row,row,col)

            if(grid[i][j] == "A1"):
                node.set_start_color()
                start = node
            if(grid[i][j] == "T1"):
                node.set_end_color()
                end = node
            if(grid[i][j] == "-1"):
                node.set_barrier_color()

            grid_color[i].append(node)
            
    return grid_color,start,end    

def draw_grid_line(window,rows, cols,width, height):
    gap1 = height // rows
    gap2 = width // cols
        
    for i in range(rows):
        pygame.draw.line(window, GREY, (0, i * gap1 + 100), (width, i * gap1 +100))
        for j in range(cols):
            pygame.draw.line(window, GREY, (j * gap2, 100), (j * gap2, height+100))

def draw_update(window, grid, rows, cols, width, height):
    
    
    for i in grid:
        for node in i:
            node.draw(window)
            
    draw_grid_line(window,rows,cols,width,height)
    pygame.display.update()

def draw_solution(come,current,draw,start):
    path = {}
    while current in come:   
        path[come[current]] = current
        current = come[current]

    while start in path:
        pygame.time.delay(100)
        start.set_unvisible()
        start = path[start]
        start.set_path_color()
        draw()

# support for A* algorithm
def heuristic(start,end):
    x1,y1 = start
    x2,y2 = end
    return abs(x1-x2) + abs(y1-y2)

def astar_algorithm(draw, grid, start,end):
    count = 0
    frontier = PriorityQueue()
    frontier.put((0,count,start))
    come = {}
    g_cost ={node: float("inf") for i in grid for node in i}
    g_cost[start] =0
    f_cost = {node: float("inf") for i in grid for node in i}
    f_cost[start] = heuristic(start.get_pos(), end.get_pos())
    
    explored = {start}
    
    while not frontier.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current_node = frontier.get()[2]
        explored.remove(current_node)
        
        # check current node is an end => draw
        if current_node == end:
            draw_solution(come,end,draw,start)
            # start.set_start_color()
            # end.set_end_color()
            return True
        
        for neighbor in current_node.neighbor:
            temp_g_cost = g_cost[current_node] +1
            
            if temp_g_cost < g_cost[neighbor]:
                come[neighbor] = current_node
                g_cost[neighbor] = temp_g_cost
                f_cost[neighbor] = temp_g_cost + heuristic(neighbor.get_pos(),end.get_pos())
                if neighbor not in explored:
                    count+=1
                    frontier.put((f_cost[neighbor], count, neighbor))
                    explored.add(neighbor)
                    neighbor.set_nodeOpen_color()
                    
        
        draw()
        
        if(current_node != start):
            current_node.set_nodeVisited_color()
            
    return False

# uniform cost search algorithm
def ucs_algorithm(draw, grid, start,end):
    count = 0
    frontier = PriorityQueue()
    frontier.put((0,count,start))
    come = {}
    g_cost ={node: float("inf") for i in grid for node in i}
    g_cost[start] =0
    
    explored = {start}
    
    while not frontier.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current_node = frontier.get()[2]
        explored.remove(current_node)
        
        # check current node is an end => draw
        if current_node == end:
            draw_solution(come,end,draw,start)
            # start.set_start_color()
            # end.set_end_color()
            return True
        
        for neighbor in current_node.neighbor:
            temp_g_cost = g_cost[current_node] +1
            
            if temp_g_cost < g_cost[neighbor]:
                come[neighbor] = current_node
                g_cost[neighbor] = temp_g_cost
                if neighbor not in explored:
                    count+=1
                    frontier.put((g_cost[neighbor], count, neighbor))
                    explored.add(neighbor)
                    neighbor.set_nodeOpen_color()
                    
        
        draw()
        
        if(current_node != start):
            current_node.set_nodeVisited_color()
            
    return False       

# breath first search  
def bfs_algorithm(draw, grid, start,end):
    count = 0
    frontier = Queue()
    frontier.put(start)
    come = {}
    is_end_exist =False
    explored = []
    
    while not frontier.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        if(is_end_exist == False):
            current_node = frontier.get()
            explored.append(current_node)
        
        # check current node is an end => draw
        if is_end_exist:
            print("OK")
            draw_solution(come,end,draw,start)
            # start.set_start_color()
            # end.set_end_color()
            return True
        
        for neighbor in current_node.neighbor:
            if neighbor not in explored:
                come[neighbor] = current_node
                if(neighbor ==end):
                    is_end_exist = True
                    break
                count+=1
                frontier.put(neighbor)
                neighbor.set_nodeOpen_color()            
        
        draw()
        
        if(current_node != start):
            current_node.set_nodeVisited_color()
            
    return False

def dfs_algorithm(draw, grid, start,end):
    count = 0
    frontier = Queue()
    frontier.put(start)
    come = {}
    is_end_exist =False
    explored = []
    
    while not frontier.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        if(is_end_exist == False):
            current_node = frontier.get()
            explored.append(current_node)
        
        # check current node is an end => draw
        if is_end_exist:
            print("OK")
            draw_solution(come,end,draw,start)
            # start.set_start_color()
            # end.set_end_color()
            return True
        
        for neighbor in current_node.neighbor:
            if neighbor not in explored:
                come[neighbor] = current_node
                if(neighbor ==end):
                    is_end_exist = True
                    break
                count+=1
                frontier.put(neighbor)
                neighbor.set_nodeOpen_color()            
        
        draw()
        
        if(current_node != start):
            current_node.set_nodeVisited_color()
            
    return False


def main(window, width, height):
    file = 'grid.txt'
    row, col,floor, temp_grid = read_grid_from_file(file)
    grid,start,end = make_grid_color(row,col,width,height,temp_grid)
    click1 = False
    click2 = False
    click3 = False
    click4 = False
    one_press = True
    
    run = True
    while run:
        window.fill(WHITE)
        astar_button = Button(10, 10,"A* algo",click1)
        ucs_button = Button(140,10, "UCS algo",click2)
        bfs_button = Button(270, 10,"BFS algo",click3)
        clear_button = Button(400, 10,"clear",click4)
        draw_update(window,grid,row,col,width,height)     
        
        if(pygame.mouse.get_pressed()[0]) and one_press:
            one_press = False
            if(bfs_button.is_click()):
                click3= True
                click1 = click2 = click4= False
                astar_button.remove_click()
                astar_button.draw()
                ucs_button.remove_click()
                ucs_button.draw()
                clear_button.remove_click()
                clear_button.draw()
                
            if(astar_button.is_click()):
                click1 = True
                click2 = click3 = click4 =False
                bfs_button.remove_click()
                bfs_button.draw()
                ucs_button.remove_click()
                ucs_button.draw()
                clear_button.remove_click()
                clear_button.draw()
                
            if(ucs_button.is_click()):
                click2= True
                click1 = click3 = click4= False
                astar_button.remove_click()
                astar_button.draw()
                bfs_button.remove_click()
                bfs_button.draw()
                clear_button.remove_click()
                clear_button.draw()
                
            if(clear_button.is_click()):
                click4= True
                click1 = click2 = click3= False
                astar_button.remove_click()
                astar_button.draw()
                bfs_button.remove_click()
                bfs_button.draw()
                ucs_button.remove_click()
                ucs_button.draw()
                grid,start,end = make_grid_color(row,col,width,height,temp_grid)
            
            if((click1 or click2 or click3)):
                for i in grid:
                    for node in i:
                        node.neighbors(grid)
                if(click1): 
                    astar_button.set_click()
                    astar_button.draw()
                    astar_algorithm(lambda: draw_update(window, grid, row, col,width,height), grid, start, end)
                if(click2):
                    ucs_button.set_click()
                    ucs_button.draw()
                    ucs_algorithm(lambda: draw_update(window, grid, row, col,width,height), grid, start, end)
                if(click3): 
                    bfs_button.set_click()
                    bfs_button.draw()
                    bfs_algorithm(lambda: draw_update(window, grid, row, col,width,height), grid, start, end)
            
        if(not pygame.mouse.get_pressed()[0]) and not one_press:
            one_press =True
            
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
                    
        
        

    pygame.quit()
    
if __name__ == "__main__":
    main(window, WIDTH,HEIGHT-100)
