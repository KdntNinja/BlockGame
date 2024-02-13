from Voxel_Engine.meshes.cloud_mesh import CloudMesh


class Clouds:
    def __init__(self, app):
        self.app = app
        self.mesh = CloudMesh(app)
        self.speed = 0.01

    def update(self):
        self.mesh.program["u_time"] = self.app.time
        current_center = self.mesh.program["center"].value
        new_center = current_center + self.speed
        self.mesh.program["center"].value = int(new_center)

    def render(self):
        self.mesh.render()