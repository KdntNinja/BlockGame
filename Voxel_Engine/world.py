from Voxel_Engine.engine_settings import *
from Voxel_Engine.world_objects.chunk import Chunk
from Voxel_Engine.voxel_handler import VoxelHandler

from concurrent.futures import ThreadPoolExecutor


class World:
    def __init__(self, app):
        self.app = app
        self.chunks = [None for _ in range(WORLD_VOL)]
        self.voxels = np.empty([WORLD_VOL, CHUNK_VOL], dtype="uint8")
        self.build_chunks()
        self.build_chunk_mesh()
        self.voxel_handler = VoxelHandler(self)

    def update(self):
        self.voxel_handler.update()

    def build_chunks(self):
        player_chunk_x = self.app.player.position[0] // GENERATION_INTENSITY
        player_chunk_y = self.app.player.position[1] // GENERATION_INTENSITY
        player_chunk_z = self.app.player.position[2] // GENERATION_INTENSITY

        player_chunk = Chunk(self, position=(player_chunk_x, player_chunk_y, player_chunk_z))
        player_chunk_index = (int(player_chunk_x) + WORLD_W * int(player_chunk_z) + WORLD_AREA * int(player_chunk_y)) % WORLD_VOL
        self.chunks[player_chunk_index] = player_chunk
        self.voxels[player_chunk_index] = player_chunk.build_voxels()
        player_chunk.voxels = self.voxels[player_chunk_index]

        with ThreadPoolExecutor() as executor:
            for x in range(WORLD_W):
                for y in range(WORLD_H):
                    for z in range(WORLD_D):
                        if x == player_chunk_x and y == player_chunk_y and z == player_chunk_z:
                            continue

                        executor.submit(self.build_single_chunk, x, y, z)

    def build_single_chunk(self, x, y, z):
        chunk = Chunk(self, position=(x, y, z))
        chunk_index = (x + WORLD_W * z + WORLD_AREA * y) % WORLD_VOL
        self.chunks[chunk_index] = chunk
        self.voxels[chunk_index] = chunk.build_voxels()
        chunk.voxels = self.voxels[chunk_index]

    def build_chunk_mesh(self):
        for chunk in self.chunks:
            chunk.build_mesh()

    def render(self):
        for chunk in self.chunks:
            chunk.render()
