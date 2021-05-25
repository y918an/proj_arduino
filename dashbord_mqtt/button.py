import pygame
class Button:
    def __init__(self, color, x,y,width,height, text='', font_size = 50,font_name = None):
        self.color = color
        self.draw_color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.font = font_name

    #desenha botão
    def draw(self,win,outline=None, ):
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.draw_color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont(None, self.font_size) if self.font is None else pygame.font.Font(self.font,self.font_size)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

    #muda a cor do botão caso o cursor esteja sobre ele
    def react_to_mouse(self,pos):
        if self.isOver(pos):
            self.draw_color = tuple(1/2 * (255-x) for x in self.color)
        else:
            self.draw_color = self.color