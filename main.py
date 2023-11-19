import pygame
from pygame.locals import *
from board import *
from config import *

class GameOfLife:

    def __init__(self):
        """The main class constructor that starts the application.
        """
        self._running = False
        self.size = self.width, self.height = 1000, 1000
    

    def on_init(self):
        """Runs the pygame initialization after the application is created.
        """
        pygame.init()
        pygame.display.set_caption("Game of Life")
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.board = Board(self.size)
        self._running = True
        self.clock = pygame.time.Clock()
        self.paused = True
        self.fps = STARTING_FPS
    

    def on_event(self, event):
        """Runs when an event happens in the application.

        Args:
            event (Event): The event that has happened.
        """
        if event.type == pygame.QUIT:
            self._running = False
        
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                self.paused = not self.paused
        
        elif event.type == MOUSEBUTTONDOWN:
            left, middle, right = pygame.mouse.get_pressed()
            if left:
                self.board.change_state_on_click(pygame.mouse.get_pos())

    
    def on_loop(self):
        """Runs as the main application loop.
        """
        if not self.paused:
            self.clock.tick(self.fps)
            self.board.on_loop()


    def on_render(self):
        """Renders things to the screen.
        """
        self._display_surf.fill("black")
        self.board.on_draw(self._display_surf)
        
        # Draws the pause icon.
        if self.paused:
            pygame.draw.rect(self._display_surf, color="gray", rect=[10, 10, 15, 50])
            pygame.draw.rect(self._display_surf, color="gray", rect=[40, 10, 15, 50])

        pygame.display.flip()


    def on_cleanup(self):
        """Runs when the application is closed.
        """
        pygame.quit()


    def on_execute(self):
        """Executes the start of the application.
        """
        if self.on_init() == False:
            self._running = False
        
        while(self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    """Main.
    """
    game = GameOfLife()
    game.on_execute()

