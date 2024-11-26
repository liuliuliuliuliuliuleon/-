import pygame
import random

# 游戏参数
b_s = 15  # 棋盘大小 15x15
c_s = 40  # 每个格子的像素大小
w_s = b_s * c_s  # 窗口大小，等于棋盘的尺寸
l_c = (0, 0, 0)  # 棋盘线颜色：黑色
b_g_c = (240, 217, 181)  # 背景颜色：浅棕色
b_c = (0, 0, 0)  # 黑棋颜色
w_c = (255, 255, 255)  # 白棋颜色

# 初始化pygame
pygame.init()
screen = pygame.display.set_mode((w_s, w_s))  # 设置游戏窗口大小
pygame.display.set_caption("简易五子棋")  # 设置窗口标题

# 加载背景图片（不加载棋盘图片）
b_g = pygame.image.load('E:\code\Gomoku.py\yuan_hui.png')  # 自定义背景图片，路径假设为当前目录下的 'background.png'

# 创建棋盘
board = [[0] * b_s for _ in range(b_s)]  # 创建 15x15 的棋盘，初始化为全 0，表示所有格子为空

# 绘制棋盘背景和网格
def d_b():
    """绘制棋盘背景和网格"""
    screen.fill(b_g_c)  # 填充背景颜色
    # 绘制背景图片（确保图片填充整个屏幕）
    b_g_scaled = pygame.transform.scale(b_g, (w_s, w_s))  # 将背景图片缩放为与屏幕尺寸相同
    screen.blit(b_g_scaled, (0, 0))  # 使用缩放后的背景图片填充整个窗口
    
    # 绘制棋盘网格线
    for i in range(1, b_s):
        pygame.draw.line(screen, l_c, (i * c_s, 0), (i * c_s, w_s), 2)  # 画垂直线
        pygame.draw.line(screen, l_c, (0, i * c_s), (w_s, i * c_s), 2)  # 画水平线

# 绘制棋子（黑棋和白棋）
def d_p():
    """绘制棋子"""
    for x in range(b_s):  # 遍历棋盘的每一行
        for y in range(b_s):  # 遍历棋盘的每一列
            if board[x][y] == 1:  # 如果该格子是黑棋
                pygame.draw.circle(screen, b_c, (c_s * (y + 1), c_s * (x + 1)), c_s // 3)  # 绘制黑棋
            elif board[x][y] == -1:  # 如果该格子是白棋
                pygame.draw.circle(screen, w_c, (c_s * (y + 1), c_s * (x + 1)), c_s // 3)  # 绘制白棋

def c_w(p):
    """检查是否有玩家获胜"""
    for x in range(b_s):  # 遍历棋盘的每一行
        for y in range(b_s):  # 遍历棋盘的每一列
            if board[x][y] == p:
                # 水平、垂直、斜线方向检查五子连珠
                if x + 4 < b_s and all(board[x + i][y] == p for i in range(5)):  # 水平
                    return True
                if y + 4 < b_s and all(board[x][y + i] == p for i in range(5)):  # 垂直
                    return True
                if x + 4 < b_s and y + 4 < b_s and all(board[x + i][y + i] == p for i in range(5)):  # 主对角线
                    return True
                if x + 4 < b_s and y - 4 >= 0 and all(board[x + i][y - i] == p for i in range(5)):  # 副对角线
                    return True
    return False

def ai_m():
    """AI 随机下棋，并尝试堵路"""
    
    # 步骤1：先找出空位
    empty_cells = [(x, y) for x in range(b_s) for y in range(b_s) if board[x][y] == 0]

    # 步骤2：AI 堵路：优先选择能阻止对方胜利的位置
    for x, y in empty_cells:
        board[x][y] = -1  # 模拟放置白棋
        if c_w(-1):  # 如果此位置能让白棋获胜
            board[x][y] = 0  # 恢复该格子为空
            return (x, y)  # 返回此位置，堵住对方
        board[x][y] = 0  # 恢复该格子为空
    
    # 步骤3：如果没有找到能堵路的位置，随机选择一个空位
    return random.choice(empty_cells)  # 随机选择一个空位置

def main():
    """主程序"""
    running = True
    current_player = 1  # 黑棋先手
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                pos = pygame.mouse.get_pos()
                x, y = (pos[1] - c_s // 2) // c_s, (pos[0] - c_s // 2) // c_s
                if 0 <= x < b_s and 0 <= y < b_s and board[x][y] == 0:
                    board[x][y] = current_player
                    if c_w(current_player):
                        print("玩家获胜！" if current_player == 1 else "AI获胜！")
                        game_over = True
                    current_player = -current_player  # 切换玩家

        # AI 落子（玩家对 AI 时）
        if not game_over and current_player == -1:
            x, y = ai_m()  # 调用 AI 的随机落子 + 堵路策略
            if x is not None and y is not None:
                board[x][y] = current_player
                if c_w(current_player):
                    print("玩家获胜！" if current_player == 1 else "AI获胜！")
                    game_over = True
                current_player = -current_player  # 切换玩家

        d_b()  # 绘制棋盘背景和网格
        d_p()  # 绘制棋子
        pygame.display.flip()  # 更新屏幕

    pygame.quit()

if __name__ == "__main__":
    main()
