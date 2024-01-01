import pygame

def countdown(sp,display_surface,x,y,time):
    time = 14 - time
    font_size = 192
    if time<11:
        font_size = int(font_size*(8*(time-int(time))))
    font1 = pygame.font.SysFont('arialrounded', font_size)
    text1 = font1.render(str(int(time)), True, (200, 100, 50))
    textRect1 = text1.get_rect()
    textRect1.center = (x // 2, y * 2 // 5)
    display_surface.fill((255,255,255))
    display_surface.blit(text1, textRect1)
    pygame.display.update()

def champ_graphics(sp,display_surface,x,y,time):
    countdown(sp,display_surface,x,y,time)



