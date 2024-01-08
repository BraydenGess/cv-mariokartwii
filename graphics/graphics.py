import pygame
def initialize_graphics():
    pygame.init()
    screen = pygame.display.set_mode()
    x,y = screen.get_size()
    display_surface = pygame.display.set_mode((x, y))
    #display_surface = pygame.display.set_mode((x, y),pygame.FULLSCREEN)
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
    def write_rectangles(self,rectangles):
        for element in rectangles:
            [rect, rgb] = element
            pygame.draw.rect(self.display_surface,rgb,rect,10)

    def draw_titlescreen(self):
        color = self.special_effect['TitleScreen']
        txt,txtRect = self.create_text('chalkduster',192,'BeerioKart',(int(color.red),int(color.green),int(color.blue)),
                                         [self.X//2,self.Y*2//5],'center')
        color.FadeIn(strength=[0,2,4],max_value=200)
        self.display_surface.fill((0,0,0))
        self.display_surface.blit(txt,txtRect)
        pygame.display.update()
    def selectionscreen_coordinates(self,i,x_buffer,y_buffer):
        if i <= 1:
            y = y_buffer
        elif i >= 2:
            y = (2.5 * y_buffer)
        if i % 2 == 0:
            x = x_buffer
            anchor = 'left'
        elif i % 2 != 0:
            x = self.X - x_buffer
            anchor = 'right'
        return x,y,anchor
    def selectionscreen_subset(self,vehicle,player,anchor,y_buffer,y,gp_info):
        if vehicle != None:
            vehicle_name = gp_info.vehicle_stats[vehicle].name
            yv = y + (y_buffer // 2)
            if player == None:
                player = 'NA'
            if anchor == 'left':
                new_text = player + ' | ' + str(vehicle_name)
            else:
                new_text = str(vehicle_name) + ' | ' + player
        return yv,new_text
    def draw_selectionscreengraph(self,gp_info,y_buffer,x_buffer,texts):
        if gp_info.menu_screen <= 3:
            max_value = 8
        else:
            max_value = 73
        stats = [[],[],[],[],[],[],[]]
        bottom = self.Y-(y_buffer)
        left = x_buffer
        graph_width = self.X//8
        graph_margin = (self.X - ((graph_width*7)+(2*x_buffer)))//7
        rect_width = graph_width//gp_info.player_count
        rectangles = []
        for i in range(gp_info.player_count):
            p = gp_info.players[gp_info.colors[i]]
            if p.character != None:
                c = gp_info.character_stats[p.character]
                stats[0].append(int(c.sp))
                stats[1].append(int(c.wt))
                stats[2].append(int(c.ac))
                stats[3].append(int(c.hn))
                stats[4].append(int(c.dr))
                stats[5].append(int(c.off))
                stats[6].append(int(c.mt))
            if p.vehicle != None:
                v = gp_info.vehicle_stats[p.vehicle]
                stats[0][i] += int(v.sp)
                stats[1][i] += int(v.wt)
                stats[2][i] += int(v.ac)
                stats[3][i] += int(v.hn)
                stats[4][i] += int(v.dr)
                stats[5][i] += int(v.off)
                stats[6][i] += int(v.mt)
        labels = ['Speed','Weight','Acceleration','Handle','Drift','Off-Road','Mini-Turbo']
        for i in range(len(stats)):
            xc = left + (graph_width//2) + (graph_margin*i) + (graph_width*i)
            txt,txtRect = self.create_text('Arial',32,labels[i],(255,255,255),(xc,bottom + ((self.Y-bottom)//4)),'center')
            texts.append([txt,txtRect])
            for j in range(len(stats[i])):
                rgb = gp_info.rgb_colors[j]
                x0 = left + (j*rect_width) + (graph_margin*i) + (graph_width*i)
                y0 = bottom
                rect_height = max(int((stats[i][j]/max_value)*(self.Y//2-(y_buffer//2))),1)
                rect = pygame.Rect(x0,y0-rect_height,rect_width,rect_height)
                rectangles.append([rect,rgb])
        return texts,rectangles
    def draw_playerselectionscreen(self,gp_info):
        x_buffer = self.X // 32
        y_buffer = self.Y // 8
        texts = []
        for i in range(gp_info.player_count):
            p = gp_info.players[gp_info.colors[i]]
            if p.character != None:
                char,vehicle,player = gp_info.character_stats[p.character].name,p.vehicle,p.name
                rgb = gp_info.rgb_colors[i]
                x,y,anchor = self.selectionscreen_coordinates(i,x_buffer,y_buffer)
                txt,txtRect  = self.create_text('Arial',72,char,rgb,[x,y],anchor)
                texts.append([txt,txtRect])
                if vehicle != None:
                    yv,new_text = self.selectionscreen_subset(vehicle,player,anchor,y_buffer,y,gp_info)
                    txt, txtRect = self.create_text('Arial',24,new_text, rgb, [x, yv], anchor)
                    texts.append([txt, txtRect])
        self.display_surface.fill((0, 0, 0))
        texts,rectangles = self.draw_selectionscreengraph(gp_info, y_buffer,x_buffer,texts)
        self.write_rectangles(rectangles)
        self.write_text(texts)
        pygame.display.update()
    def course_intro(self,sp):
        self.display_surface.fill((0, 0, 0))
        img = sp.playlist[sp.course_queued].img
        if img != None:
            pic = pygame.image.load(img)
            pic = pygame.transform.scale(pic, (self.X, self.Y))
            self.display_surface.blit(pic,(0, 0))
            pygame.display.update()
    def run_graphics(self,gp_info,sp):
        if (gp_info.menu_screen <= 2):
            self.draw_titlescreen()
        elif ((gp_info.menu_screen >= 3)and(sp.course_queued==0)):
            self.draw_playerselectionscreen(gp_info)
        elif (gp_info.racing and not gp_info.read_menu):
            self.course_intro(sp)
        self.exit()
    def exit(self):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()


