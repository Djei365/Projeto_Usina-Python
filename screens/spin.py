# -*- coding: utf-8 -*-
import math
import pygame
from screens.base import Screen
from ui import theme
from ui.widgets import draw_background, draw_title

class SpinScreen(Screen):
    def on_enter(self):
        super().on_enter()

    def handle_input(self, action):
        if action == "B":
            self.next_screen = "home"

    def draw(self, surface, t):
        draw_background(surface, self.starfield, t)
        
        # --- VIEWPORT RESPONSIVO ---
        is_landscape = self.width > self.height
        active_w = int(self.height * 0.5625) if is_landscape else self.width
        offset_x = (self.width - active_w) // 2
        center_x = offset_x + (active_w // 2)

        # 1. TÍTULO GERAL
        title_y = int(self.height * 0.035)
        draw_title(surface, "SPIN", center_x, title_y, size=int(active_w * 0.08))

        # 2. CONTROLE "VOLTAR"
        ctrl_y = title_y + int(self.height * 0.04)
        f_ctrl = theme.font(int(active_w * 0.03))
        btn_b_txt = f_ctrl.render("Voltar", True, theme.WHITE)
        
        total_w = 24 + 10 + btn_b_txt.get_width() 
        start_ctrl_x = center_x - (total_w // 2)
        
        pygame.draw.circle(surface, (220, 0, 0), (start_ctrl_x + 12, ctrl_y + 10), 12)
        pygame.draw.circle(surface, theme.WHITE, (start_ctrl_x + 12, ctrl_y + 10), 12, 2)
        surface.blit(btn_b_txt, (start_ctrl_x + 34, ctrl_y - 2))

        # 3. ANIMAÇÃO SUPERIOR (Giro Intrínseco)
        anim1_box_y = ctrl_y + int(self.height * 0.035)
        anim1_box_h = int(self.height * 0.14) 
        anim1_box_w = active_w - int(active_w * 0.16)
        anim_box_x = offset_x + int(active_w * 0.08)

        anim1_rect = pygame.Rect(anim_box_x, anim1_box_y, anim1_box_w, anim1_box_h)
        pygame.draw.rect(surface, (15, 20, 30), anim1_rect, border_radius=15)
        pygame.draw.rect(surface, (50, 150, 200), anim1_rect, width=3, border_radius=15)

        self._draw_spin_axis_animation(surface, t, center_x, anim1_box_y + anim1_box_h//2, active_w)

        # 4. CAIXA DE TEXTO DIDÁTICO (TEXTO SIMPLIFICADO PARA LEIGOS)
        texto_box_y = anim1_box_y + anim1_box_h + int(self.height * 0.015)
        
        paragrafos = [
            "O Spin (que significa 'giro') é uma característica invisível e natural das partículas. Para entender de forma simples, imagine que cada partícula funciona como um pequeno pião que nunca para de girar. Esse giro não é mecânico como no nosso mundo, mas sim uma regra misteriosa da física quântica.",
            "Na natureza, as partículas são divididas em dois grandes grupos por causa desse giro: os Férmions, que possuem um spin 'quebrado' (valores em frações, como ½), e os Bósons, que possuem um spin de número 'inteiro' (como 0, 1 e 2).",
            "Essa diferença muda tudo! Os Férmions são 'individualistas': duas dessas partículas nunca podem ocupar exatamente o mesmo espaço e estado ao mesmo tempo. É graças a essa regra de exclusão que a matéria sólida existe e você não afunda no chão! Já os Bósons são 'sociais' e podem se agrupar infinitamente.",
            "Toda a matéria que compõe você e as estrelas (Quarks e Léptons) é feita de Férmions. Por outro lado, as partículas que transmitem as forças do universo (como o Fóton, que compõe a luz) são Bósons, assim como o famoso Bóson de Higgs."
        ]
        
        f_texto = theme.font(int(active_w * 0.027)) 
        
        padding_topo = int(self.height * 0.02)
        altura_texto_total = padding_topo
        
        for p in paragrafos:
            altura_texto_total += self._get_text_height(p, anim1_box_w - 60, f_texto)
            altura_texto_total += int(self.height * 0.015) 
            
        altura_texto_total += int(self.height * 0.005)
        texto_box_h = altura_texto_total
        
        texto_rect = pygame.Rect(anim_box_x, texto_box_y, anim1_box_w, texto_box_h)
        pygame.draw.rect(surface, (15, 20, 30), texto_rect, border_radius=15)
        pygame.draw.rect(surface, (50, 150, 200), texto_rect, width=3, border_radius=15)
        
        cursor_y = texto_box_y + padding_topo 
        for p in paragrafos:
            cursor_y = self._draw_justified_text(surface, p, anim_box_x + 30, cursor_y, anim1_box_w - 60, f_texto)
            cursor_y += int(self.height * 0.015) 

        # 5. ANIMAÇÃO INFERIOR (Sincronizada com o limite inferior do Cubo da Home)
        anim2_box_y = texto_box_y + texto_box_h + int(self.height * 0.015)
        
        menu_y_home = int(self.height * 0.19)
        item_h_home = int(self.height * 0.045)
        cube_y_home = menu_y_home + (4 * item_h_home) + int(self.height * 0.05)
        cube_h_home = int(active_w * 0.8)
        base_home_y = cube_y_home + cube_h_home
        
        anim2_box_h = base_home_y - anim2_box_y
        
        if anim2_box_h < int(self.height * 0.12):
            anim2_box_h = int(self.height * 0.12)

        anim2_rect = pygame.Rect(anim_box_x, anim2_box_y, anim1_box_w, anim2_box_h)
        pygame.draw.rect(surface, (15, 20, 30), anim2_rect, border_radius=15)
        pygame.draw.rect(surface, (50, 150, 200), anim2_rect, width=3, border_radius=15)

        self._draw_pauli_animation(surface, t, anim_box_x, anim2_box_y, anim1_box_w, anim2_box_h, active_w)


    def _get_text_height(self, text, max_w, font):
        words = text.split(" ")
        if not words: return 0
        
        lines_count = 1
        current_w = 0
        space_w = font.size(" ")[0]
        
        for word in words:
            word_w = font.size(word)[0]
            if current_w + word_w <= max_w:
                current_w += word_w + space_w
            else:
                lines_count += 1
                current_w = word_w + space_w
                
        return lines_count * font.get_linesize()


    def _draw_justified_text(self, surface, text, x, y, max_w, font):
        words = text.split(" ")
        if not words: return y
        
        lines = []
        current_line = []
        current_w = 0
        space_w = font.size(" ")[0]
        
        for word in words:
            word_w = font.size(word)[0]
            if current_w + word_w <= max_w:
                current_line.append(word)
                current_w += word_w + space_w
            else:
                lines.append(current_line)
                current_line = [word]
                current_w = word_w + space_w
        if current_line:
            lines.append(current_line)
            
        current_y = y
        line_height = font.get_linesize()
        
        for i, line in enumerate(lines):
            if not line: continue
            
            if i == len(lines) - 1 or len(line) == 1:
                cursor_x = x
                for word in line:
                    img = font.render(word, True, theme.WHITE)
                    surface.blit(img, (cursor_x, current_y))
                    cursor_x += img.get_width() + space_w
            else:
                total_words_w = sum(font.size(w)[0] for w in line)
                total_spaces_w = max_w - total_words_w
                space_w_float = total_spaces_w / (len(line) - 1)
                
                cursor_x = float(x)
                for word in line:
                    img = font.render(word, True, theme.WHITE)
                    surface.blit(img, (int(cursor_x), current_y))
                    cursor_x += img.get_width() + space_w_float
                    
            current_y += line_height
            
        return current_y


    def _draw_spin_axis_animation(self, surface, t, cx, cy, active_w):
        radius = int(active_w * 0.055)
        
        pygame.draw.circle(surface, (30, 80, 150), (cx, cy), radius)
        pygame.draw.circle(surface, (100, 180, 255), (cx, cy), radius, 2)
        
        tilt = math.sin(t * 3) * (radius * 0.4) 
        if abs(tilt) > 1:
            ring_rect = pygame.Rect(cx - radius, cy - abs(tilt), radius * 2, abs(tilt) * 2)
            pygame.draw.ellipse(surface, (150, 220, 255), ring_rect, 2)
            
        top_y = cy - radius - 15 - (tilt * 0.5)
        bot_y = cy + radius + 15 + (tilt * 0.5)
        
        pygame.draw.line(surface, theme.GOLD, (cx, bot_y), (cx, top_y), 4)
        
        pygame.draw.polygon(surface, theme.GOLD, [
            (cx, top_y - 10), 
            (cx - 8, top_y + 5), 
            (cx + 8, top_y + 5)
        ])

        f_lbl = theme.font(int(active_w * 0.025))
        lbl = f_lbl.render("Giro Intrínseco", True, (150, 200, 255))
        surface.blit(lbl, lbl.get_rect(midleft=(cx + radius + 25, cy)))


    def _draw_pauli_animation(self, surface, t, box_x, box_y, box_w, box_h, active_w):
        cycle = t % 3.0
        
        mid_x = box_x + box_w // 2
        cy = box_y + box_h // 2 + 10 
        
        pygame.draw.line(surface, (40, 60, 90), (mid_x, box_y + 10), (mid_x, box_y + box_h - 10), 2)
        
        f_title = theme.font(int(active_w * 0.025))
        
        lbl_f = f_title.render("Férmions (Exclusão)", True, (255, 100, 100))
        surface.blit(lbl_f, lbl_f.get_rect(midtop=(box_x + box_w//4, box_y + 15))) 
        
        lbl_b = f_title.render("Bósons (Agrupamento)", True, (100, 255, 100))
        surface.blit(lbl_b, lbl_b.get_rect(midtop=(box_x + (box_w*3)//4, box_y + 15))) 
        
        p_rad = int(active_w * 0.035)
        dist_max = int(active_w * 0.12)
        
        cx_f = box_x + box_w // 4
        cx_b = box_x + (box_w * 3) // 4
        
        if cycle < 1.5:
            progresso = cycle / 1.5
            ease = progresso ** 2
            offset = dist_max - int(dist_max * ease)
            
            pygame.draw.circle(surface, (200, 50, 50), (cx_f - offset, cy), p_rad)
            pygame.draw.circle(surface, (200, 50, 50), (cx_f + offset, cy), p_rad)
            
            pygame.draw.circle(surface, (50, 200, 50), (cx_b - offset, cy), p_rad)
            pygame.draw.circle(surface, (50, 200, 50), (cx_b + offset, cy), p_rad)
            
        else:
            progresso = (cycle - 1.5) / 1.5
            ease = progresso ** 0.5 
            
            offset = int(dist_max * 0.8 * ease)
            pygame.draw.circle(surface, (255, 80, 80), (cx_f - offset, cy), p_rad)
            pygame.draw.circle(surface, (255, 80, 80), (cx_f + offset, cy), p_rad)
            
            if progresso < 0.3:
                pygame.draw.line(surface, theme.WHITE, (cx_f - 10, cy - 10), (cx_f + 10, cy + 10), 3)
                pygame.draw.line(surface, theme.WHITE, (cx_f - 10, cy + 10), (cx_f + 10, cy - 10), 3)

            s = pygame.Surface((p_rad * 4, p_rad * 4), pygame.SRCALPHA)
            alpha = int(abs(math.sin(t * 10)) * 150) 
            pygame.draw.circle(s, (100, 255, 100, alpha), (p_rad*2, p_rad*2), int(p_rad * 1.5))
            surface.blit(s, (cx_b - p_rad*2, cy - p_rad*2))
            
            pygame.draw.circle(surface, (100, 255, 100), (cx_b, cy), p_rad)
            pygame.draw.circle(surface, theme.WHITE, (cx_b, cy), p_rad, 2)
