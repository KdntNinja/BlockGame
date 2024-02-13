from Voxel_Engine.meshes.quad_mesh import QuadMesh


class Water:
    def __init__(self, app):
        self.app = app
        self.mesh = QuadMesh(app)
        self.time = 0.0

    def update(self):
        self.time += 0.005
        self.mesh.program["time"].value = self.time

    def render(self):
        self.update()
        self.mesh.render()
