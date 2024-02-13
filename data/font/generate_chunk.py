@staticmethod
@njit
def generate_terrain(voxels, cx, cy, cz):
    for x in range(GENERATION_INTENSITY):
        wx = x + cx
        for z in range(GENERATION_INTENSITY):
            wz = z + cz
            world_height = get_height(wx, wz)
            local_height = min(world_height - cy, GENERATION_INTENSITY)

            for y in range(local_height):
                wy = y + cy
                set_voxel_id(voxels, x, y, z, wx, wy, wz, world_height)