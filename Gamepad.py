import pygame

BUTTON_STATE_UP = 0
BUTTON_STATE_DOWN = 1
EVENT_BUTTON_UP = pygame.USEREVENT + 1
EVENT_BUTTON_DOWN = pygame.USEREVENT + 2

class Button:
    def __init__(self, image, overlay, x, y):
        self.state = BUTTON_STATE_UP
        self.image = pygame.image.load(image)
        self.image = self.image.convert_alpha()
        
        if overlay:
            overlaySurface = pygame.image.load(overlay)
            overlaySurface = overlaySurface.convert_alpha()
            
            overlayWidth = overlaySurface.get_width()
            overlayHeight = overlaySurface.get_height()
            
            imageWidth = self.image.get_width()
            imageHeight = self.image.get_height()
            
            deltaWidth = imageWidth - overlayWidth
            deltaHeight = imageHeight - overlayHeight

            if deltaWidth < 0:
                deltaWidth = 0
            if deltaHeight < 0:
                deltaHeight = 0

            deltaWidth = deltaWidth / 2
            deltaHeight = deltaHeight / 2
            
            self.image.blit(overlaySurface, (deltaWidth, deltaHeight))
        
        self.x = x
        self.y = y
        self.x2 = self.image.get_width() + self.x
        self.y2 = self.image.get_height() + self.y
    # end __init__(self, image, overlay, x, y)

    def render(self, surface):
        surface.blit(self.image, (self.x, self.y))
    # end render(self, surface)
    
    def pointInButton(self, point):
        x = point[0]
        y = point[1]

        if x < self.x:
            return False
        if x > self.x2:
            return False
        if y < self.y:
            return False
        if y > self.y2:
            return False
        
        return True
    # end pointInButton(self, point)

    def getState(self):
        return self.state
    # end getState(self)

    def resetClickCount(self):
        self.clickCount = 0
    # end resetClickCount(self)

    def incrementClickCount(self):
        self.clickCount = self.clickCount + 1
    # end incrementClickCount(self)

    def setStateFromClickCount(self):
        if self.clickCount > 0:
            if self.state == BUTTON_STATE_UP:
                self.state = BUTTON_STATE_DOWN
                event = pygame.event.Event(EVENT_BUTTON_DOWN,
                            dict([('button', self)]))
                pygame.event.post(event)
        else:
            if self.state == BUTTON_STATE_DOWN:
                self.state = BUTTON_STATE_UP
                event = pygame.event.Event(EVENT_BUTTON_UP,
                            dict([('button', self)]))
                pygame.event.post(event)
    # end setStateFromClickCount(self)
    
    def isDown(self):
        if self.state == BUTTON_STATE_DOWN:
            return True
        else:
            return False
    # end isDown(self)
# end class Button


class Gamepad:
    def __init__(self):
        self.joystickCount = pygame.joystick.get_count()
        self.buttons = []

    # end __init__(self)

    def addButton(self, image, overlay, x, y):
        newButton = Button(image, overlay, x, y)
        self.buttons.append(newButton)
        return newButton
    # end addButton
    
    def update(self):
        buttonCount = len(self.buttons)
        if buttonCount <= 0:
            return

        for button in self.buttons:
            button.resetClickCount()
        
        for i in range(1, self.joystickCount):
            if pygame.joystick.Joystick(i).get_button(0):
                x = pygame.joystick.Joystick(i).get_axis(0) * 32768
                y = pygame.joystick.Joystick(i).get_axis(1) * 32768
                for button in self.buttons:
                    if button.pointInButton((x, y)):
                        button.incrementClickCount()

        for button in self.buttons:
            button.setStateFromClickCount()
    # end update(self)
    
    def render(self, screen):
        for button in self.buttons:
            button.render(screen)
    # end render(self, screen)
# end Gamepad
