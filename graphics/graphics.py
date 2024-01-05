import pygame

def initialize_graphics():
    pygame.init()
    screen = pygame.display.set_mode()
    x,y = screen.get_size()
    display_surface = pygame.display.set_mode((x, y),pygame.FULLSCREEN)
    caption = "Beerio"
    pygame.display.set_caption(caption)
    specialeffects_dict= {'TitleScreen':Special_Effects(blue=0,green=0,red=0)}
    graphics = Graphics(display_surface=display_surface,X=x,Y=y,caption=caption,special_effects=specialeffects_dict)
    return graphics

class Special_Effects():
    def __init__(self,blue=None,green=None,red=None):
        self.blue = blue
        self.green = green
        self.red = red
    def FadeIn(self,strength,max_value):
        new_blue = self.blue + strength[2]
        new_green = self.green + strength[1]
        new_red = self.red + strength[0]
        if max(new_blue,new_green,new_red) < max_value:
            self.blue = new_blue
            self.green = new_green
            self.red = new_red

class Graphics():
    def __init__(self,display_surface=None,X=None,Y=None,caption=None,special_effects=None):
        self.display_surface = display_surface
        self.X = X
        self.Y = Y
        self.caption = caption
        self.special_effect = special_effects
    def create_text(self,font,font_size,text,color,coordinates,anchor):
        font = pygame.font.SysFont(font,font_size)
        txt = font.render(text,True,color)
        txtRect = txt.get_rect()
        txtRect.center = (coordinates[0],coordinates[1])
        if anchor == 'left':
            txtRect.left = (coordinates[0])
        elif anchor == 'right':
            txtRect.right = (coordinates[0])
        return txt,txtRect
    def write_text(self,texts):
        for element in texts:
            [txt,txtRect] = element
            self.display_surface.blit(txt, txtRect)
    def draw_titlescreen(self):
        color = self.special_effect['TitleScreen']
        txt,txtRect = self.create_text('chalkduster',192,'BeerioKart',(int(color.red),int(color.green),int(color.blue)),
                                         [self.X//2,self.Y*2//5],'center')
        color.FadeIn(strength=[0,0.2,0.4],max_value=200)
        self.display_surface.fill((0,0,0))
        self.display_surface.blit(txt,txtRect)
        pygame.display.update()
    def draw_playerselectionscreen(self,gp_info):
        x_buffer = self.X//32
        y_buffer = self.Y//8
        texts = []
        for i in range(len(gp_info.colors)):
            p = gp_info.players[gp_info.colors[i]]
            char = p.character
            vehicle = p.vehicle
            player = p.name
            rgb = gp_info.rgb_colors[i]
            if i <= 1:
                y = y_buffer
            elif i >= 2:
                y = (2.5*y_buffer)
            if i%2 == 0:
                x = x_buffer
                anchor = 'left'
            elif i%2 != 0:
                x = self.X - x_buffer
                anchor = 'right'
            txt,txtRect = self.create_text('Arial',72,char,rgb,[x,y],anchor)
            texts.append([txt,txtRect])
            if vehicle != None:
                yv = y+(y_buffer//2)
                if player == None:
                    player = 'NA'
                new_text = player + ' | ' + vehicle
                txt, txtRect = self.create_text('Arial',24,new_text, rgb, [x, yv], anchor)
                texts.append([txt, txtRect])
        self.display_surface.fill((0, 0, 0))
        self.write_text(texts)
        pygame.display.update()

    def run_graphics(self,gp_info):
        if (gp_info.menu_screen <= 2):
            self.draw_titlescreen()
        if (gp_info.menu_screen >= 3):
            self.draw_playerselectionscreen(gp_info)
        self.exit()
    def exit(self):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()


