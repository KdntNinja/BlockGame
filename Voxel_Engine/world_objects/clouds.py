from Voxel_Engine.meshes.cloud_mesh import CloudMesh
from math import sin


class Clouds:
    def __init__(self, app, system="default"):
        self.app = app
        self.mesh = CloudMesh(app)
        self.speed = 0.005
        self.system = system
        self.colour_change_speed = 0.1

    def update(self):
        self.mesh.program["u_time"] = self.app.time
        current_center = self.mesh.program["center"].value
        new_center = current_center + self.speed
        self.mesh.program["center"].value = int(new_center)

        if self.system == "default":
            self.mesh.program["color_change"] = 0.5 * sin(self.colour_change_speed * self.app.time)

    def render(self):
        self.mesh.render()