import pygame
from tools.utility import string_tocolor,text_spaces,int_tostring
import time
import io
import cv2 as cv
import urllib
from graphics.video import play_clip

def initialize_graphics(screen_setting):
    pygame.init()
    screen = pygame.display.set_mode()
    x,y = screen.get_size()
    if screen_setting.lower() == 'fullscreen':
        display_surface = pygame.display.set_mode((x, y), pygame.FULLSCREEN)
    else:
        display_surface = pygame.display.set_mode((x, y))
        y = y - (y//14)
    caption = "Beerio"
    pygame.display.set_caption(caption)
    specialeffects_dict= {'TitleScreen':Special_Effects(blue=0,green=0,red=0,count=0),
                          'SongIntro':Special_Effects(blue=0,green=0,red=0,count=0),
                          'CountdownScreen':Special_Effects(blue=255,green=255,red=255,count=0)}
    countdown_songs = [line.strip().split(',') for line in open('audio/playlists/countdown.csv')][0]
    graphics = Graphics(display_surface=display_surface,X=x,Y=y,caption=caption,special_effects=specialeffects_dict,
                        time = time.time(),volume=100,songs=countdown_songs)
    return graphics

class Special_Effects():
    def __init__(self,blue=None,green=None,red=None,count=None):
        self.blue = blue
        self.green = green
        self.red = red
        self.count = count
    def FadeIn(self,strength,max_value):
        new_blue = max(0,self.blue + strength[2])
        new_green = max(0,self.green + strength[1])
        new_red = max(0,self.red + strength[0])
        if max(new_blue,new_green,new_red) < max_value:
            self.blue = new_blue
            self.green = new_green
            self.red = new_red
    def count_up(self):
        if self.count <= 99:
            self.count += 1

class Graphics():
    def __init__(self,display_surface=None,X=None,Y=None,caption=None,special_effects=None,time=None,volume=None,songs=None):
        self.display_surface = display_surface
        self.X = X
        self.Y = Y
        self.caption = caption
        self.special_effect = special_effects
        self.time = time
        self.volume = volume
        self.songs = songs
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
        max_value = 73
        stats = [[],[],[],[],[],[],[]]
        bottom = self.Y-(y_buffer//2)
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
            txt,txtRect = self.create_text('Arial',32,labels[i],(255,255,255),(xc,bottom + ((self.Y-bottom)//2)),'center')
            texts.append([txt,txtRect])
            for j in range(len(stats[i])):
                rgb = gp_info.rgb_colors[j]
                x0 = left + (j*rect_width) + (graph_margin*i) + (graph_width*i)
                y0 = bottom
                stats_value = max(1,int(stats[i][j]))
                rect_height = max(int((stats_value/max_value)*(self.Y//2-(y_buffer//2))),1)
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
        course = sp.playlist[sp.course_queued]
        course_name = course.course_name
        color = course.txtcolor
        texts = []
        txt, txtRect = self.create_text('impact', 74, text_spaces(course_name), string_tocolor(color),
                                        (self.X // 45, self.Y // 20), 'left')
        txt2, txtRect2 = self.create_text('impact', 24, course.CPI, string_tocolor(color),
                                          (self.X // 200, self.Y // 40), 'left')
        text3 = '(Length: ' + str(course.length_rank) + '/AP: ' + str(course.AP) + ')'
        txt3, txtRect3 = self.create_text('avenirnextcondensed', 32, text3, string_tocolor(color),
                                          (self.X // 45, self.Y // 8.5),'left')
        texts.append([txt, txtRect])
        texts.append([txt2, txtRect2])
        texts.append([txt3, txtRect3])
        self.write_text(texts)
        pygame.display.update()
    def song_intro(self,sp):
        self.display_surface.fill((0, 0, 0))
        width, height = 640, 640
        x_start, y_start = self.X // 2 - (width // 2), self.Y // 2 - (height // 2)
        image_file = io.BytesIO(sp.img_str)
        initial_pic = pygame.image.load(image_file)
        desired_size = (width,height)
        pic = pygame.transform.smoothscale(initial_pic, desired_size)
        txt, txtRect = self.create_text('impact', 74,sp.song_queued.song_name,string_tocolor('white'),
                                        (self.X // 2, self.Y - self.Y//16),'center')
        texts = [[txt,txtRect]]
        self.write_text(texts)
        self.display_surface.blit(pic, (x_start,y_start))
        pygame.display.update()
    def scoreboard(self,gp_info,sp):
        self.display_surface.fill((0, 0, 0))
        texts = []
        x_buffer = self.X//64
        y_buffer = self.Y//16
        size = (self.Y-(3*y_buffer))/len(gp_info.scoreboard)
        desired_size = (size,size)
        img_directory = 'graphics/characterpictures/'
        labeltxt,labeltxtRect = self.create_text('impact',72,'SCOREBOARD', string_tocolor('white'),
                                        (self.X//2,y_buffer),'center')
        texts.append([labeltxt,labeltxtRect])
        for i in range(len(gp_info.scoreboard)):
            character_index = gp_info.scoreboard[i][0]
            character_name = gp_info.character_stats[character_index+1].name
            character_score = gp_info.scoreboard[i][1]
            img_path = img_directory+character_name+'.png'
            pic = pygame.image.load(img_path)
            pic = pygame.transform.smoothscale(pic, desired_size)
            top_left = (2*y_buffer)+(size*i)
            self.display_surface.blit(pic, (x_buffer,top_left))
            txt,txtRect = self.create_text('impact',32,character_name, string_tocolor('white'),
                                        ((x_buffer*2)+size,top_left+(size//2)),'left')
            txt2, txtRect2 = self.create_text('impact', 32, str(character_score), string_tocolor('white'),
                                            (self.X//3, top_left + (size // 2)), 'left')
            texts.append([txt,txtRect])
            texts.append([txt2,txtRect2])
        ### Course History
        length,height = self.X//2-(2*x_buffer),(self.Y-(3*y_buffer))//8
        for i in range(len(gp_info.gp_courses)):
            course_index = gp_info.gp_courses[i]
            img_path,course_name = sp.playlist[course_index].img,sp.playlist[course_index].course_name
            pic = pygame.image.load(img_path)
            pic = pygame.transform.smoothscale(pic,(length,height))
            x0,y0 = self.X//2+x_buffer,(height*i)+(2*y_buffer)
            self.display_surface.blit(pic, (x0,y0))
            txt,txtRect = self.create_text('impact',48,text_spaces(course_name),string_tocolor('white'),
                                        (x0 + length//2,y0 + height//2),'center')
            texts.append([txt,txtRect])
        self.write_text(texts)
        pygame.display.update()
    def song_info(self,sp):
        self.display_surface.fill((0, 0, 0))
        width, height = 80, 80
        x_end, y_end = self.X // 64, self.Y - (self.Y // 64) - height
        image_file = io.BytesIO(sp.img_str)
        initial_pic = pygame.image.load(image_file)
        desired_size = (width, height)
        pic = pygame.transform.smoothscale(initial_pic, desired_size)
        txt, txtRect = self.create_text('impact', 24, sp.song_queued.song_name, string_tocolor('white'),
                                        (x_end+width+width//4,y_end+(height//2)), 'left')
        texts = [[txt, txtRect]]
        self.write_text(texts)
        self.display_surface.blit(pic, (x_end, y_end))
        pygame.display.update()
    def race(self,gp_info,sp):
        t2 = time.time()
        time_diff = t2-gp_info.time
        if time_diff <= 10:
            self.song_intro(sp)
        elif time_diff%10 <= 5:
            self.scoreboard(gp_info,sp)
        else:
            self.song_info(sp)
        pygame.display.update()
    def racing_graphics(self,gp_info,sp):
        if not gp_info.started:
            self.course_intro(sp)
        if gp_info.started:
            self.race(gp_info,sp)
    def not_connected(self):
        txt, txtRect = self.create_text('impact', 192, 'Disconnected',(255,255,255),
                                        [self.X // 2, self.Y *2 // 5], 'center')
        self.display_surface.fill((0, 0, 0))
        self.display_surface.blit(txt, txtRect)
        pygame.display.update()
    def run_graphics(self,gp_info,sp,ret):
        if not ret:
            self.not_connected()
        if (gp_info.menu_screen <= 2):
            self.draw_titlescreen()
        elif ((gp_info.menu_screen >= 3)and(sp.course_queued==0)):
            self.draw_playerselectionscreen(gp_info)
        elif (gp_info.racing and not gp_info.read_menu):
            self.racing_graphics(gp_info,sp)
        self.exit()
    def play_movie(self):
        play_clip(video_file="/Users/bradygess/Documents/SigEpGunGame.mp4",x = self.X,y = self.Y)
    def countdown_audio(self,sp,time_left):
        switch = [13.5,11.5,9.5,7,5,3,.5,0]
        song = sp.song_queued
        for i in range(len(switch)-1):
            if (switch[i]*60)>time_left>(switch[i+1]*60):
                new_song = sp.get_song(self.songs[i])
                if song != new_song:
                    sp.spotify.add_to_queue(uri=new_song.uri, device_id=None)
                    sp.song_queued = new_song
                    sp.skip_tosong(new_song.uri)
    def countdown(self,sp):
        quit = False
        t1 = time.time()
        time_left = ((.4*60) - (t1 - self.time))
        self.countdown_audio(sp, time_left)
        if time_left > 1:
            fill_color = (255,255,255)
            txt_color = (0,0,0)
            text_size = 192
            if time_left < 10:
                text_size = int(192 + (1000*(time_left-int(time_left))))
            texts = []
            txt, txtRect = self.create_text('impact', 172, 'Sig Ep Gun Game', txt_color,
                                            (self.X // 2, self.Y*2//10), 'center')
            texts.append([txt, txtRect])
            txt, txtRect = self.create_text('impact', 68, 'A Tier Finals', txt_color,
                                            (self.X * 7.5 // 10, self.Y*3.5 // 10), 'center')
            texts.append([txt, txtRect])
            txt, txtRect = self.create_text('impact', text_size, int_tostring(time_left),txt_color,
                                        [self.X // 2, self.Y * 6 // 10], 'center')
            texts.append([txt, txtRect])
            self.display_surface.fill(fill_color)
            self.write_text(texts)
        elif -6 <= time_left <= 1:
            if self.volume == 100:
                sp.spotify.volume(volume_percent=50,device_id=None)
                self.volume = 50
            txt_color = (0,0,0)
            texts = []
            txt, txtRect = self.create_text('impact', 172, 'Sig Ep Gun Game', txt_color,
                                            (self.X // 2, self.Y * 2 // 10), 'center')
            texts.append([txt, txtRect])
            txt, txtRect = self.create_text('impact', 68, 'A Tier Finals', txt_color,
                                            (self.X * 7.5 // 10, self.Y * 3.5 // 10), 'center')
            texts.append([txt, txtRect])
            color = self.special_effect['CountdownScreen']
            color.FadeIn(strength=[-1,-1,-1], max_value=255)
            time.sleep(0.01)
            fill_color = (color.red,color.green,color.blue)
            self.display_surface.fill(fill_color)
            self.write_text(texts)
            pygame.display.update()
            if ((fill_color == (0,0,0)) and (self.volume == 50)):
                sp.min_volume()
                self.volume = 0
        else:
            if self.volume != 0:
                sp.min_volume()
            self.play_movie()
            sp.max_volume()
            quit = True
        pygame.display.update()
        return quit
    def final_graphics(self,sp):
        quit = self.countdown(sp)
        self.exit()
        if quit:
            return True
        return False
    def exit(self):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()


