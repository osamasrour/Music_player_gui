import pygame
pygame.init()

class Button:
    COLORS = {
        "white" : (255, 255, 255),
        "black" : (0, 0, 0),
        "purple" : (127, 0, 255),
        "pink" : (255, 51, 255),
        "red" : (255, 51, 51),
        "cyan" : (0, 255, 255),
        "aqua" : (0, 255, 255),
        "olive" : (128, 128, 0),
        "gold" : (255, 215, 0),
        "darkgray" : (110, 110, 110),
        "gray" : (180, 180, 180),
        "blue" : (51, 51, 255)
    }
    def __init__(self, text: str, pos: tuple, size: int, TextColor: str="white",
                bgcolor1: str="darkgray", bgcolor2: str="gray") -> None:
        self.x = pos[0]
        self.y = pos[1]
        self.text = text
        self.color = TextColor
        self.bgcolor1 = bgcolor1
        self.bgcolor2 = bgcolor2
        self.font = pygame.font.SysFont("Arial", size, bold=True)
        self.lable = self.font.render(self.text, True, Button.COLORS["white"])
        self.rect = (self.x, self.y, self.lable.get_width() + 20, self.lable.get_height() + 20)
        self.width = self.lable.get_width() + 20
        self.height = self.lable.get_height() + 20
        self.clicked = False


    def draw(self, surface):
        pos = pygame.mouse.get_pos()
        # ask for a collision between mouse and Button
        lable = self.font.render(self.text, True, Button.COLORS[self.color])
        if self.x <= pos[0] <= (self.x + self.width) and self.y <= pos[1] <= (self.y + self.height):
            pygame.draw.rect(surface, Button.COLORS[self.bgcolor2], self.rect, border_radius=5)
            surface.blit(lable, (self.x + 10, self.y + 10))
        else:
            pygame.draw.rect(surface, Button.COLORS[self.bgcolor1], self.rect, border_radius=5)
            surface.blit(lable, (self.x + 10, self.y + 10))

    def isclicked(self):
        action = False
        # get the mouse position
        pos = pygame.mouse.get_pos()
        # ask for a collision between mouse and Button
        if self.x <= pos[0] <= (self.x + self.width) and self.y <= pos[1] <= (self.y + self.height):
            # check if the butten get clicked
            if pygame.mouse.get_pressed()[0] is True and self.clicked == False:
                self.clicked = True
                action = True
        # release the button after every triger
        if pygame.mouse.get_pressed()[0] is False and self.clicked == True:
            self.clicked = False
        return action
