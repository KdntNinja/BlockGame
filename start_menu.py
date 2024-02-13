import os

import pygame as pg
import pygame_menu
import random

from Voxel_Engine.voxel_engine import VoxelEngine

from Voxel_Engine.engine_settings import *
from config import Config
from default_config import Default


class MenuConfig:
    def __init__(self):
        self.config = Config()
        self.temp_config = self.config.load_config()
        self.default_config = Default()

    def save_config(self):
        self.config.config = self.temp_config
        self.config.save_config()


    def change_config(self, parameter: str, index):
        self.temp_config[parameter] = index
        self.save_config()


class Menu:
    def __init__(self):
        pg.init()

        os.environ["SDL_VIDEO_CENTERED"] = "1"
        self.menu = None
        self.app = None

        self.config = MenuConfig()
        self.temp_config = self.config.config.load_config()
        self.default_config = Default()

        self.width = 500
        self.height = 600

        self.surface = pg.display.set_mode((self.width, self.height))

        self.theme = pygame_menu.themes.Theme(
            background_color=(26, 26, 26),
            title_font="data/font/MinecraftBold.otf",
            title_font_size=67,
            title_background_color=(26, 26, 26),
            title_font_color=(255,255,255),
            widget_font="data/font/MinecraftRegular.otf",
            widget_font_size=39,
            widget_background_color=(26, 26, 26),
            widget_font_color=(169, 169, 169),
        )

        self.create_base_menu()

    def create_base_menu(self):
        self.menu = pygame_menu.Menu("BlockGame", self.width, self.height, theme=self.theme)
        self.menu.add.text_input("Name: ", default=self.config.config.get("name", self.default_config.name), onchange=lambda value: self.config.change_config("name", value))
        self.menu.add.button("Play", self.start_the_game)
        self.menu.add.button("Settings", self.create_settings_menu)
        self.menu.add.button("Quit", lambda: (self.config.save_config(), exit()))

    def create_settings_menu(self):
        settings_menu = pygame_menu.Menu("Settings", self.width, self.height, theme=self.theme)

        settings_menu.add.selector("", [("Windowed", 0), ("Fullscreen", 1)], onchange=lambda value, index: self.config.change_config("fullscreen", index), default=int(self.temp_config["fullscreen"]))
        settings_menu.add.selector("", [("Spectator", 0), ("Survival", 1)], onchange=lambda value, index: self.config.change_config("mode", index), default=int(self.temp_config["mode"]))
        settings_menu.add.selector("", [("Initial World", 0), ("Constant World", 1)], onchange=lambda value, index: self.config.change_config("world", index), default=int(self.temp_config["world"]))
        settings_menu.add.button("Back", self.exit_settings_menu)
        settings_menu.mainloop(self.surface)

    def exit_settings_menu(self):
        self.menu.clear()
        self.create_base_menu()
        self.menu.mainloop(self.surface)

    def start_the_game(self):
        self.config.save_config()
        self.menu.disable()
        pg.display.set_caption("BlockGame")

        self.app = VoxelEngine(get_screen_resolution())
        self.app.on_init()
        self.app.run()

    def run(self):
        while True:
            self.surface.fill((26, 26, 26))
            self.menu.mainloop(self.surface)
            pg.display.flip()
