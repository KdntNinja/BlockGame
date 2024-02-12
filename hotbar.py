import pygame as pg

class Hotbar:
    def __init__(self, surface, item_images):
        self.surface = surface
        self.item_images = item_images
        self.slot_size = 50
        self.slots_count = 10
        self.margin = 5
        self.hotbar = [None] * self.slots_count

    def draw(self):
        for i in range(self.slots_count):
            rect = pg.Rect(i * (self.slot_size + self.margin), self.surface.get_height() - self.slot_size - self.margin, self.slot_size, self.slot_size)
            pg.draw.rect(self.surface, (100, 100, 100), rect)
            if self.hotbar[i] is not None:
                self.surface.blit(pg.transform.scale(self.item_images[self.hotbar[i]], (self.slot_size, self.slot_size)), rect.topleft)

    def update(self, hotbar):
        self.hotbar = hotbar
