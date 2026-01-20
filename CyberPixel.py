import pygame
import sys
import os
import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image as PilImage

# Define a classe da janela antes do Pygame iniciar
try:
    os.environ['SDL_VIDEO_X11_WMCLASS'] = "CyberPixelApp"
except:
    pass

# --- Inicialização do Tkinter ---
root = tk.Tk()
root.withdraw() 

# --- Configurações Iniciais ---
LARGURA_TELA_TOTAL = 480
ALTURA_TELA_TOTAL = 320
CANVAS_SIZE = 320 
TAMANHO_GRID = 16 
TAMANHO_PIXEL = CANVAS_SIZE // TAMANHO_GRID

# --- PALETA DB32 ---
DB32 = [
    (0,0,0), (34,32,52), (69,40,60), (102,57,49), (143,86,59), (223,113,38), (217,160,102), (238,195,154),
    (251,242,54), (153,229,80), (106,190,48), (55,148,110), (75,105,47), (82,75,36), (50,60,57), (63,63,116),
    (48,96,130), (91,110,225), (99,155,255), (95,205,228), (203,219,252), (255,255,255), (155,173,183), (132,126,135),
    (105,106,106), (89,86,82), (118,66,138), (172,50,50), (217,87,99), (215,123,186), (143,151,74), (138,111,48)
]
PALETA = DB32
cor_atual_index = 21

# Cores UI
COR_BG_SIDEBAR = (40, 40, 50)
COR_TEXTO = (200, 200, 200)
COR_TEXTO_DESTAQUE = (255, 255, 0)
# Cores do Xadrez (Transparência)
CHECKER_1 = (60, 60, 60)
CHECKER_2 = (90, 90, 90)

# --- Inicialização Pygame ---
pygame.init()

try:
    if os.path.exists("CyberPixelLogo.png"):
        icone = pygame.image.load("CyberPixelLogo.png")
        pygame.display.set_icon(icone)
except: pass

tela = pygame.display.set_mode((LARGURA_TELA_TOTAL, ALTURA_TELA_TOTAL))
pygame.display.set_caption("CyberPixel v7.1 (Alpha)")

fonte = pygame.font.SysFont("monospace", 11, bold=True)
fonte_grande = pygame.font.SysFont("monospace", 14, bold=True)
clock = pygame.time.Clock()

# --- Estrutura de Dados ---
# ATENÇÃO: Agora iniciamos com None (Transparente) em vez de PALETA[0]
def criar_grid_vazio(tamanho):
    return [[None for _ in range(tamanho)] for _ in range(tamanho)]

frames = [criar_grid_vazio(TAMANHO_GRID)]
frame_atual = 0
cursor_x, cursor_y = 0, 0
historico_undo = []
MAX_UNDO = 30

def salvar_estado():
    # Copia profunda manual para lidar com None
    copia = [linha[:] for linha in frames[frame_atual]]
    historico_undo.append((copia, TAMANHO_GRID)) 
    if len(historico_undo) > MAX_UNDO: historico_undo.pop(0)

# --- FERRAMENTAS ---
def mudar_resolucao(novo_tamanho):
    global TAMANHO_GRID, TAMANHO_PIXEL, frames, frame_atual, cursor_x, cursor_y
    
    if novo_tamanho < 4 or novo_tamanho > 128:
        print("Tamanho invalido (min 4, max 128)")
        return

    print(f"Mudando resolução para {novo_tamanho}x{novo_tamanho}...")
    salvar_estado()

    novos_frames = []
    for grid_antigo in frames:
        # Converte grid para imagem PIL RGBA temporária
        img_temp = PilImage.new('RGBA', (TAMANHO_GRID, TAMANHO_GRID), (0,0,0,0))
        pix = img_temp.load()
        for y in range(TAMANHO_GRID):
            for x in range(TAMANHO_GRID):
                cor = grid_antigo[y][x]
                if cor is not None:
                    pix[x, y] = (cor[0], cor[1], cor[2], 255)
                else:
                    pix[x, y] = (0, 0, 0, 0) # Transparente
        
        # Redimensiona usando Nearest Neighbor (pixel art style)
        img_temp = img_temp.resize((novo_tamanho, novo_tamanho), PilImage.NEAREST)
        
        # Reconverte imagem PIL para Grid do CyberPixel
        novo_grid = criar_grid_vazio(novo_tamanho)
        pix_novo = img_temp.load()
        for y in range(novo_tamanho):
            for x in range(novo_tamanho):
                r, g, b, a = pix_novo[x, y]
                if a == 0:
                    novo_grid[y][x] = None
                else:
                    novo_grid[y][x] = (r, g, b)
        novos_frames.append(novo_grid)

    frames = novos_frames
    TAMANHO_GRID = novo_tamanho
    TAMANHO_PIXEL = max(1, CANVAS_SIZE // TAMANHO_GRID)
    cursor_x = TAMANHO_GRID // 2
    cursor_y = TAMANHO_GRID // 2
    
def flood_fill(grid, start_x, start_y, new_color):
    target_color = grid[start_y][start_x]
    if target_color == new_color: return
    
    stack = [(start_x, start_y)]
    while stack:
        cx, cy = stack.pop()
        if 0 <= cx < TAMANHO_GRID and 0 <= cy < TAMANHO_GRID:
            # Compara se é a mesma cor (lidando com None)
            if grid[cy][cx] == target_color:
                grid[cy][cx] = new_color
                stack.append((cx - 1, cy))
                stack.append((cx + 1, cy))
                stack.append((cx, cy - 1))
                stack.append((cx, cy + 1))

def shift_canvas(grid, dx, dy):
    novo_grid = criar_grid_vazio(TAMANHO_GRID)
    for y in range(TAMANHO_GRID):
        for x in range(TAMANHO_GRID):
            nx, ny = x + dx, y + dy
            if 0 <= nx < TAMANHO_GRID and 0 <= ny < TAMANHO_GRID:
                novo_grid[ny][nx] = grid[y][x]
    return novo_grid

# --- UI Helpers ---
def desenhar_texto(superficie, texto, x, y, cor=COR_TEXTO, fonte_usada=fonte):
    superficie.blit(fonte_usada.render(texto, True, cor), (x, y))

def acao_redimensionar():
    novo = simpledialog.askinteger("Redimensionar", "Novo tamanho (Ex: 32):", minvalue=4, maxvalue=128)
    if novo: mudar_resolucao(novo)

def acao_salvar():
    caminho = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png"), ("GIF", "*.gif")])
    if not caminho: return
    
    if caminho.endswith(".gif"):
        # Exportação GIF (Simplificada, fundo preto se transparente pois GIF tem limitações chatas com alpha parcial)
        lista_pil = []
        for f in frames:
            img = PilImage.new('RGBA', (TAMANHO_GRID, TAMANHO_GRID), (0,0,0,0))
            pix = img.load()
            for y in range(TAMANHO_GRID):
                for x in range(TAMANHO_GRID): 
                    c = f[y][x]
                    if c: pix[x, y] = (c[0], c[1], c[2], 255)
            # Remove alpha pro GIF ficar ok ou usa disposal method (aqui simplificado para RGB)
            bg = PilImage.new('RGB', img.size, (0,0,0))
            bg.paste(img, mask=img.split()[3])
            lista_pil.append(bg.resize((320, 320), PilImage.NEAREST))
        lista_pil[0].save(caminho, save_all=True, append_images=lista_pil[1:], duration=250, loop=0)
    else:
        # Exportação PNG com ALPHA (Transparência Real)
        surf = pygame.Surface((TAMANHO_GRID, TAMANHO_GRID), pygame.SRCALPHA)
        # Preenche com transparente
        surf.fill((0,0,0,0))
        
        grid = frames[frame_atual]
        for y in range(TAMANHO_GRID):
            for x in range(TAMANHO_GRID): 
                cor = grid[y][x]
                if cor is not None:
                    surf.set_at((x, y), cor)
                # Se for None, já está transparente (0,0,0,0)
                
        pygame.image.save(surf, caminho)

def acao_carregar():
    caminho = filedialog.askopenfilename(filetypes=[("Imagens", "*.png *.jpg *.gif")])
    if not caminho: return
    
    salvar_estado()
    global frames, frame_atual, TAMANHO_GRID, TAMANHO_PIXEL
    
    try:
        img_pil = PilImage.open(caminho)
        w, h = img_pil.size
        maior_lado = max(w, h)
        
        if maior_lado != TAMANHO_GRID:
            novo_tamanho = min(maior_lado, 128) 
            mudar_resolucao(novo_tamanho)
        
        frames_temp = []
        n_frames = getattr(img_pil, "n_frames", 1)
        
        for i in range(n_frames):
            img_pil.seek(i)
            # Converte para RGBA para ler transparência
            frame_rgba = img_pil.convert("RGBA").resize((TAMANHO_GRID, TAMANHO_GRID), PilImage.NEAREST)
            grid_frame = criar_grid_vazio(TAMANHO_GRID)
            
            pix = frame_rgba.load()
            for y in range(TAMANHO_GRID):
                for x in range(TAMANHO_GRID):
                    r, g, b, a = pix[x, y]
                    if a > 0: # Considera pixel se tiver alpha > 0
                        grid_frame[y][x] = (r, g, b)
                    else:
                        grid_frame[y][x] = None
                        
            frames_temp.append(grid_frame)
            
        frames = frames_temp
        frame_atual = 0
        
    except Exception as e:
        print(f"Erro ao carregar: {e}")

# --- Loop Principal ---
mostrando_seletor = False
mostrar_grade = True 
rodando = True
paleta_cursor_x, paleta_cursor_y = 0, 0

while rodando:
    clock.tick(30)
    
    grid_logica = frames[frame_atual] 
    
    keys = pygame.key.get_pressed()
    ctrl = keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT: rodando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE: rodando = False
            
            if ctrl and evento.key == pygame.K_r: acao_redimensionar()

            if mostrando_seletor:
                if evento.key in [pygame.K_c, pygame.K_SPACE, pygame.K_RETURN]: mostrando_seletor = False
                elif evento.key == pygame.K_UP: paleta_cursor_y = max(0, paleta_cursor_y - 1)
                elif evento.key == pygame.K_DOWN: paleta_cursor_y = min(3, paleta_cursor_y + 1)
                elif evento.key == pygame.K_LEFT: paleta_cursor_x = max(0, paleta_cursor_x - 1)
                elif evento.key == pygame.K_RIGHT: paleta_cursor_x = min(7, paleta_cursor_x + 1)
                cor_atual_index = paleta_cursor_y * 8 + paleta_cursor_x
            else:
                if not ctrl:
                    if evento.key == pygame.K_UP: cursor_y = max(0, cursor_y - 1)
                    elif evento.key == pygame.K_DOWN: cursor_y = min(TAMANHO_GRID - 1, cursor_y + 1)
                    elif evento.key == pygame.K_LEFT: cursor_x = max(0, cursor_x - 1)
                    elif evento.key == pygame.K_RIGHT: cursor_x = min(TAMANHO_GRID - 1, cursor_x + 1)
                
                # [Espaço] Pinta
                if evento.key == pygame.K_SPACE: 
                    salvar_estado()
                    grid_logica[cursor_y][cursor_x] = PALETA[cor_atual_index]
                
                # [E] Apaga (Torna None/Transparente)
                elif evento.key == pygame.K_e: 
                    salvar_estado()
                    grid_logica[cursor_y][cursor_x] = None # <--- AQUI ESTÁ A MÁGICA
                
                elif evento.key == pygame.K_g: 
                    salvar_estado()
                    flood_fill(grid_logica, cursor_x, cursor_y, PALETA[cor_atual_index])
                
                elif evento.key == pygame.K_z:
                    if ctrl and historico_undo: 
                        dados_undo = historico_undo.pop()
                        frames[frame_atual] = dados_undo[0]
                        if dados_undo[1] != TAMANHO_GRID: 
                            mudar_resolucao(dados_undo[1])
                            frames[frame_atual] = dados_undo[0]

                elif evento.key == pygame.K_c: 
                    mostrando_seletor = True
                    paleta_cursor_y, paleta_cursor_x = divmod(cor_atual_index, 8)
                
                elif evento.key == pygame.K_i:
                    # Conta-gotas (precisa checar se não é None)
                    cor_pick = grid_logica[cursor_y][cursor_x]
                    if cor_pick is not None:
                        try: cor_atual_index = PALETA.index(cor_pick)
                        except: pass
                        
                elif evento.key == pygame.K_TAB: mostrar_grade = not mostrar_grade
                elif evento.key == pygame.K_s: acao_salvar()
                elif evento.key == pygame.K_l: acao_carregar()
                
                # Copia frame precisa lidar com None também (l[:] funciona)
                elif evento.key == pygame.K_n: 
                    frames.insert(frame_atual + 1, [l[:] for l in grid_logica])
                    frame_atual += 1
                
                elif evento.key == pygame.K_x: 
                    if len(frames) > 1: frames.pop(frame_atual); frame_atual = min(frame_atual, len(frames)-1)
                elif evento.key == pygame.K_COMMA: frame_atual = max(0, frame_atual - 1)
                elif evento.key == pygame.K_PERIOD: frame_atual = min(len(frames) - 1, frame_atual + 1)

                if ctrl:
                    if evento.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                        salvar_estado()
                        dx, dy = 0, 0
                        if evento.key == pygame.K_UP: dy = -1
                        elif evento.key == pygame.K_DOWN: dy = 1
                        elif evento.key == pygame.K_LEFT: dx = -1
                        elif evento.key == pygame.K_RIGHT: dx = 1
                        frames[frame_atual] = shift_canvas(grid_logica, dx, dy)

    # --- DESENHO ---
    tela.fill(COR_BG_SIDEBAR)
    
    grid_desenho = frames[frame_atual] 
    
    for y in range(TAMANHO_GRID):
        for x in range(TAMANHO_GRID):
            rx, ry = x * TAMANHO_PIXEL, y * TAMANHO_PIXEL
            rect = (rx, ry, TAMANHO_PIXEL, TAMANHO_PIXEL)
            
            cor = grid_desenho[y][x]
            
            if cor is None:
                # Desenha padrão Xadrez (Checkerboard) para representar transparência
                half = TAMANHO_PIXEL // 2
                # Fundo base (escuro)
                pygame.draw.rect(tela, CHECKER_1, rect)
                # Quadrados claros
                if half > 0:
                    pygame.draw.rect(tela, CHECKER_2, (rx, ry, half, half))
                    pygame.draw.rect(tela, CHECKER_2, (rx+half, ry+half, half, half))
            else:
                # Desenha a cor sólida
                pygame.draw.rect(tela, cor, rect)
                
            if mostrar_grade and TAMANHO_PIXEL > 4: 
                pygame.draw.rect(tela, (30,30,30), rect, 1)

    # Cursor
    if not mostrando_seletor:
        cor_c = (255,255,255) if pygame.time.get_ticks() % 600 < 300 else (0,0,0)
        espessura = max(1, TAMANHO_PIXEL // 8)
        if cursor_x < TAMANHO_GRID and cursor_y < TAMANHO_GRID:
            pygame.draw.rect(tela, cor_c, (cursor_x*TAMANHO_PIXEL, cursor_y*TAMANHO_PIXEL, TAMANHO_PIXEL, TAMANHO_PIXEL), espessura)

    # Sidebar
    sx, sy = CANVAS_SIZE + 10, 10
    desenhar_texto(tela, "CYBERPIXEL v7.1", sx, sy, COR_TEXTO_DESTAQUE, fonte_grande); sy += 25
    pygame.draw.rect(tela, PALETA[cor_atual_index], (sx, sy, 30, 30))
    pygame.draw.rect(tela, (255,255,255), (sx, sy, 30, 30), 2)
    desenhar_texto(tela, f"Cor: {cor_atual_index}", sx + 38, sy + 8); sy += 40
    
    desenhar_texto(tela, f"RES: {TAMANHO_GRID}x{TAMANHO_GRID}", sx, sy, (0, 255, 0)); sy += 15
    desenhar_texto(tela, f"FRAME: {frame_atual + 1}/{len(frames)}", sx, sy, COR_TEXTO_DESTAQUE); sy += 20
    
    cmds = [
        "[Space] Pintar", "[E] Borracha", 
        "[Ctrl+Z] Undo", "[Ctrl+R] Resize", 
        "[G] Balde", "[I] Conta-gotas", 
        "[C] Paleta", "[Tab] Grade",
        "[S] Salvar", "[L] Abrir", 
        "[N] Novo Frame", "[X] Del Frame",
        "[<] [>] Navegar"
    ]
    for c in cmds:
        desenhar_texto(tela, c, sx, sy)
        sy += 14

    if mostrando_seletor:
        ov = pygame.Surface((CANVAS_SIZE, CANVAS_SIZE)); ov.set_alpha(200); ov.fill((0,0,0)); tela.blit(ov, (0,0))
        stx, sty = (CANVAS_SIZE - (8*35))//2, (CANVAS_SIZE - (4*35))//2
        for i in range(32):
            cy, cx = divmod(i, 8); rx, ry = stx+cx*35, sty+cy*35
            pygame.draw.rect(tela, PALETA[i], (rx, ry, 30, 30))
            if i == cor_atual_index: pygame.draw.rect(tela, (255,255,255), (rx-2, ry-2, 34, 34), 2)
        pygame.draw.rect(tela, (255,255,0), (stx + paleta_cursor_x * 35 - 2, sty + paleta_cursor_y * 35 - 2, 34, 34), 3)

    pygame.display.flip()

pygame.quit(); sys.exit()
