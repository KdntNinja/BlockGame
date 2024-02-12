import os

import pygame as pg
import pygame_menu

from Voxel_Engine.voxel_engine import VoxelEngine
from Voxel_Engine import engine_settings

from config import Config
from default_config import Default
from resolution import get_screen_resolution


class Menu:
    def __init__(self):
        pg.init()

        os.environ["SDL_VIDEO_CENTERED"] = "1"
        self.menu = None
        self.app = None

        self.config = Config()
        self.temp_config = self.config.load_config()
        self.default_config = Default()

        self.width = 400
        self.height = 500

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

        self.base_menu()

    def base_menu(self):
        self.menu = pygame_menu.Menu("BlockGame", self.width, self.height, theme=self.theme)
        self.menu.add.text_input("Name: ", default=self.config.get("name", self.default_config.name), onchange=lambda value: self.change_config("name", value))
        self.menu.add.button("Play", self.start_the_game)
        self.menu.add.button("Settings", self.create_settings_menu)
        self.menu.add.button("Quit", lambda: (self.save_config(), exit()))

    def create_settings_menu(self):
        settings_menu = pygame_menu.Menu("Settings", self.width, self.height, theme=self.theme)

        settings_menu.add.selector("Fullscreen: ", [("OFF", 0), ("ON", 1)], onchange=lambda value, index: self.change_config("fullscreen", index), default=int(self.temp_config["fullscreen"]))
        settings_menu.add.selector("Mode: ", [("Spectator", 0), ("Survival", 1)], onchange=lambda value, index: self.change_config("mode", index), default=int(self.temp_config["mode"]))
        settings_menu.add.selector("World: ", [("Initial", 0), ("Constant", 1)], onchange=lambda value, index: self.change_config("world", index), default=int(self.temp_config["world"]))
        settings_menu.add.button("Back", self.exit_settings_menu)
        settings_menu.mainloop(self.surface)

    def exit_settings_menu(self):
        self.menu.clear()
        self.base_menu()
        self.menu.mainloop(self.surface)

    def save_config(self):
        self.config.config = self.temp_config
        self.config.save_config()

    def change_config(self, parameter: str, index):
        self.temp_config[parameter] = index
        self.save_config()

    def start_the_game(self):
        self.save_config()
        self.menu.disable()
        pg.display.set_caption("BlockGame")

        new_resolution = get_screen_resolution()
        engine_settings.WIN_RES = new_resolution

        self.app = VoxelEngine(new_resolution)
        self.app.run()



    def run(self):
        self.menu.mainloop(self.surface)
