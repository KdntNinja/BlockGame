from Voxel_Engine.meshes.chunk_mesh import ChunkMesh
from Voxel_Engine.terrain_gen import *
from numba import njit, prange
import numpy as np
import glm


class Chunk:
    def __init__(self, world, position):
        self.app = world.app
        self.world = world
        self.position = position
        self.m_model = self.get_model_matrix()
        self.voxels: np.array = None
        self.mesh: ChunkMesh = None
        self.is_empty = True

        self.center = (glm.vec3(self.position) + 0.5) * GENERATION_INTENSITY
        self.is_on_frustum = self.app.player.frustum.is_on_frustum

    def get_model_matrix(self):
        m_model = glm.translate(
            glm.mat4(), glm.vec3(self.position) * GENERATION_INTENSITY
        )
        return m_model

    def set_uniform(self):
        self.mesh.program["m_model"].write(self.m_model)

    def build_mesh(self):
        self.mesh = ChunkMesh(self)

    def render(self):
        if not self.is_empty and self.is_on_frustum(self):
            self.set_uniform()
            self.mesh.render()

    def build_voxels(self):
        voxels = np.zeros(CHUNK_VOL, dtype="uint8")

        cx, cy, cz = glm.ivec3(self.position) * GENERATION_INTENSITY
        self.generate_terrain(voxels, cx, cy, cz)

        if np.any(voxels):
            self.is_empty = False
        return voxels

    @staticmethod
    @njit(parallel=True)
    def generate_terrain(voxels, cx, cy, cz):
        for x in prange(GENERATION_INTENSITY):
            wx = x + cx
            for z in prange(GENERATION_INTENSITY):
                wz = z + cz
                world_height = get_height(wx, wz)
                local_height = min(world_height - cy, GENERATION_INTENSITY)

                for y in prange(local_height):
                    wy = y + cy
                    set_voxel_id(voxels, x, y, z, wx, wy, wz, world_height)

    @staticmethod
    @njit
    def set_voxel_id(voxels, x, y, z, wx, wy, wz, world_height):
        set_voxel_id(voxels, x, y, z, wx, wy, wz, world_height)
