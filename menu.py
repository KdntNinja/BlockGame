import pygame as pg
import pygame_menu

from config import Config
from voxel_engine import VoxelEngine


class Menu:
    def __init__(self):
        pg.init()
        self.config = Config()
        self.temp_config = self.config.load_config()

        self.surface = pg.display.set_mode((600, 400))
        self.menu = pygame_menu.Menu("Welcome", 300, 400, theme=pygame_menu.themes.THEME_BLUE)
        self.menu.add.text_input("Name :", default=self.config.get("name", "Player 1"), onchange=self.save_name)
        self.menu.add.button("Play", self.start_the_game)
        self.menu.add.button("Settings", self.create_settings_menu)
        self.menu.add.button("Quit", pygame_menu.events.EXIT)

    def create_settings_menu(self):
        settings_menu = pygame_menu.Menu("Settings", 300, 400, theme=pygame_menu.themes.THEME_BLUE)
        fullscreen = self.config.get("fullscreen", False)
        settings_menu.add.selector('Fullscreen :', [('OFF', False), ('ON', True)],
                                   onchange=self.toggle_fullscreen, default=1 if fullscreen else 0)
        settings_menu.add.button("Back", self.exit_settings_menu)
        settings_menu.mainloop(self.surface)

    def exit_settings_menu(self):
        self.config.config = self.temp_config
        self.config.save_config()

        if self.config.get("fullscreen"):
            self.toggle_fullscreen()

        self.menu.enable()
        self.menu.reset(1)

    def save_name(self, value):
        self.temp_config["name"] = value

    def toggle_fullscreen(self, _=None, value=False):
        self.temp_config["fullscreen"] = value
        if self.temp_config["fullscreen"]:
            pg.display.set_mode((0, 0), pg.FULLSCREEN)
        else:
            pg.display.set_mode((1280, 720))

    def start_the_game(self):
        self.config.config = self.temp_config
        self.config.save_config()
        if self.config.get("fullscreen"):
            self.toggle_fullscreen()
        pg.display.set_mode((0, 0), pg.FULLSCREEN) if self.config.get("fullscreen") else pg.display.set_mode((600, 400))
        self.menu.disable()
        pg.display.set_caption("BlockGame")
        app = VoxelEngine()
        app.run()

    def run(self):
        self.menu.mainloop(self.surface)
