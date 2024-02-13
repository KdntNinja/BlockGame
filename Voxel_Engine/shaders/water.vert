#version 330 core

layout (location = 0) in vec2 in_tex_coord;
layout (location = 1) in vec3 in_position;

uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_view_proj;
uniform int water_area;
uniform float water_line;
uniform float time;

out vec2 uv;
out vec3 position;
out vec3 normal;

void main() {
    vec3 pos = in_position;
    pos.xz *= water_area;
    pos.xz -= 0.33 * water_area;

    pos.y += water_line + sin(time + pos.x) * 0.1;
    uv = in_tex_coord * water_area;
    position = pos;

    normal = vec3(0.0, 1.0, 0.0);

    gl_Position = m_proj * m_view * vec4(pos, 1.0);
}