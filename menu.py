import pygame as pg
import pygame_menu
import os

from config import Config
from voxel_engine import VoxelEngine
from default import Default



class Menu:
    def __init__(self):
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        self.menu = None
        pg.init()
        self.config = Config()
        self.temp_config = self.config.load_config()

        self.default_config = Default()

        self.width = 400
        self.height = 500

        self.surface = pg.display.set_mode((self.width, self.height))

    def base_menu(self):
        self.menu = pygame_menu.Menu("Welcome", self.width, self.height, theme=pygame_menu.themes.THEME_BLUE)
        self.menu.add.text_input("Name :", default=self.config.get("name", self.default_config.name), onchange=lambda value: self.change_config("name", value))
        self.menu.add.button("Play", self.start_the_game)
        self.menu.add.button("Settings", self.create_settings_menu)
        self.menu.add.button("Quit", pygame_menu.events.EXIT)

    def create_settings_menu(self):
        self.save_config()
        self.temp_config = self.config.load_config()

        settings_menu = pygame_menu.Menu("Settings", self.width, self.height, theme=pygame_menu.themes.THEME_BLUE)
        settings_menu.add.selector("Fullscreen :", [("OFF", 0), ("ON", 1)], onchange=lambda value, index: self.change_config("fullscreen", value), default=int(self.temp_config["fullscreen"]))
        settings_menu.add.selector("Mode :", [("Spectator", 0), ("Survival", 1)], onchange=lambda value, index: self.change_config("mode", value), default=int(self.temp_config["mode"]))
        settings_menu.add.selector("World :", [("Initial", 0), ("Constant", 1)], onchange=lambda value, index: self.change_config("world", value), default=int(self.temp_config["world"]))
        settings_menu.add.button("Back", self.exit_settings_menu)
        settings_menu.mainloop(self.surface)

    def exit_settings_menu(self):
        self.save_config()
        self.menu.clear()
        self.base_menu()
        self.menu.mainloop(self.surface)

    def save_config(self):
        self.config.config = self.temp_config
        self.config.save_config()

    def change_config(self, parameter: str, value):
        self.temp_config[parameter] = value
        self.save_config()

    def start_the_game(self):
        self.save_config()
        self.menu.disable()
        pg.display.set_caption("BlockGame")
        app = VoxelEngine()
        app.run()

    def run(self):
        self.base_menu()
        self.menu.mainloop(self.surface)
