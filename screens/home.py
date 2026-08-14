# -*- coding: utf-8 -*-
import math
import pygame
from screens.base import Screen
from ui import theme
from ui.widgets import draw_background, draw_title, draw_menu_list

# O menu agora unifica a lista superior e os itens do cubo!
# Itens 0 a 3: Lista superior padrão
# Itens 4 a 8: Interações dentro do cubo
MENU_ITEMS = [
    ("Léptons e Quarks", "leptons_quarks"),
    ("Antimatéria", "antimatter"),
    ("Jogo dos Hádrons", "hadron_game"),
    ("Quiz", "quiz"),
    ("Massa", "massa"),          
    ("Carga", "carga"),           
    ("Spin", "spin"),         
    ("Tempo de vida", "vida"),   
    ("Forças", "forces"),     
]

class HomeScreen(Screen):
    def on_enter(self):
        super().on_enter()
        self.selected = 0

    def handle_input(self, action):
        if action == "UP":
            self.selected = (self.selected - 1) % len(MENU_ITEMS)
        elif action == "DOWN":
            self.selected = (self.selected + 1) % len(MENU_ITEMS)
        elif action == "A":
            target = MENU_ITEMS[self.selected][1]
            if target:
                self.next_screen = target

    def on_cube_placed(self, particle):
        self.next_screen = "cube_reader"

    def draw(self, surface, t):
        draw_background(surface, self.starfield, t)
        
        # --- ESPAÇAMENTOS CORRIGIDOS ---
        title_y = int(self.height * 0.05)
        ctrl_y = int(self.height * 0.15) 
        menu_y = int(self.height * 0.19) 
        item_h = int(self.height * 0.045) 

        # 1. TÍTULO ANIMADO
        pulso = abs(math.sin(t * 3))
        cor_titulo = (255, 255, int(100 + 155 * pulso))
        
        f_titulo = theme.font(64)
        linha1 = f_titulo.render("PARTÍCULAS", True, cor_titulo)
        linha2 = f_titulo.render("ELEMENTARES", True, cor_titulo)
        
        surface.blit(linha1, linha1.get_rect(center=(self.width // 2, title_y)))
        surface.blit(linha2, linha2.get_rect(center=(self.width // 2, title_y + 70)))

        # 2. CONTROLES DESENHADOS
        f_ctrl = theme.font(26) 
        
        joy_txt = f_ctrl.render("Mover", True, theme.WHITE)
        btn_a_txt = f_ctrl.render("Avançar", True, theme.WHITE)
        btn_b_txt = f_ctrl.render("Voltar", True, theme.WHITE)

        center_x = self.width // 2
        offset = int(self.width * 0.28)

        # JOYSTICK
        joy_x = center_x - offset
        pygame.draw.rect(surface, theme.WHITE, (joy_x - 40, ctrl_y, 10, 24))
        pygame.draw.rect(surface, theme.WHITE, (joy_x - 47, ctrl_y + 7, 24, 10))
        surface.blit(joy_txt, (joy_x - 15, ctrl_y - 2))

        # BOTÃO VERDE (Avançar)
        pygame.draw.circle(surface, (0, 220, 0), (center_x - 30, ctrl_y + 12), 16)
        pygame.draw.circle(surface, theme.WHITE, (center_x - 30, ctrl_y + 12), 16, 2)
        surface.blit(btn_a_txt, (center_x - 5, ctrl_y - 2))

        # BOTÃO VERMELHO (Voltar)
        btn_b_x = center_x + offset
        pygame.draw.circle(surface, (220, 0, 0), (btn_b_x - 30, ctrl_y + 12), 16)
        pygame.draw.circle(surface, theme.WHITE, (btn_b_x - 30, ctrl_y + 12), 16, 2)
        surface.blit(btn_b_txt, (btn_b_x - 5, ctrl_y - 2))

        # 3. LISTA DE MENU (4 primeiros itens)
        list_labels = [name for name, _ in MENU_ITEMS[:4]]
        margin = int(self.width * 0.08) 
        list_w = self.width - (margin * 2)
        
        list_selected = self.selected if self.selected < 4 else -1
        draw_menu_list(surface, list_labels, list_selected, margin, menu_y, list_w, item_h=item_h, size=30)

        # 4. O CUBO INTERATIVO
        cube_y = menu_y + (4 * item_h) + int(self.height * 0.05)
        cube_w = int(self.width * 0.8) 
        cube_h = cube_w                
        cube_x = center_x - (cube_w // 2)

        # Bordas do Cubo 
        pygame.draw.rect(surface, theme.WHITE, (cube_x, cube_y, cube_w, cube_h), 4)
        pygame.draw.rect(surface, theme.WHITE, (cube_x + 12, cube_y + 12, cube_w - 24, cube_h - 24), 2)

        # Grande "X" centralizado no meio
        f_x = theme.font(int(cube_w * 0.55))
        img_x = f_x.render("X", True, theme.WHITE)
        surface.blit(img_x, img_x.get_rect(center=(center_x, cube_y + cube_h // 2)))

        # "Nome" puxado mais para cima (18% da altura do cubo em relação à base) para ficar colado ao X
        f_nome = theme.font(int(cube_w * 0.06))
        img_nome = f_nome.render("Nome", True, theme.WHITE)
        surface.blit(img_nome, img_nome.get_rect(midbottom=(center_x, cube_y + cube_h - int(cube_h * 0.18))))

        # --- TEXTOS SELECIONÁVEIS DENTRO DO CUBO ---
        def get_color(idx):
            return theme.GOLD if self.selected == idx else theme.WHITE
        
        def get_text(idx, text):
            return f"> {text}" if self.selected == idx else text

        f_prop = theme.font(int(cube_w * 0.045)) 
        
        # 4.1 Canto Superior Esquerdo
        lbl_massa = f_prop.render(get_text(4, "Massa"), True, get_color(4))
        surface.blit(lbl_massa, (cube_x + 25, cube_y + 25))

        lbl_carga = f_prop.render(get_text(5, "Carga"), True, get_color(5))
        surface.blit(lbl_carga, (cube_x + 25, cube_y + 25 + int(cube_h * 0.08)))

        lbl_spin = f_prop.render(get_text(6, "Spin"), True, get_color(6))
        surface.blit(lbl_spin, (cube_x + 25, cube_y + 25 + int(cube_h * 0.16)))

        # 4.2 Canto Inferior Esquerdo
        lbl_tempo = f_prop.render(get_text(7, "Tempo de vida"), True, get_color(7))
        surface.blit(lbl_tempo, (cube_x + 15, cube_y + cube_h - 20 - lbl_tempo.get_height()))

        # 4.3 Canto Superior Direito (FORÇAS)
        forcas_text = "FORÇAS"
        forcas_x = cube_x + cube_w - 45 
        forcas_y = cube_y + 25
        c_forcas = get_color(8)
        
        if self.selected == 8:
            ind = f_prop.render(">", True, theme.GOLD)
            surface.blit(ind, (forcas_x - 20, forcas_y))
            
        for i, letter in enumerate(forcas_text):
            lbl_l = f_prop.render(letter, True, c_forcas)
            surface.blit(lbl_l, lbl_l.get_rect(midtop=(forcas_x, forcas_y + i * int(cube_h * 0.065))))
