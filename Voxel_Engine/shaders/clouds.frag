#version 330 core

layout (location = 0) out vec4 fragColor;

uniform vec3 bg_color;
uniform float u_time;

void main() {
    float fog_dist = gl_FragCoord.z / gl_FragCoord.w;

    vec3 cloud_color = vec3(0.5 * sin(0.1 * u_time) + 0.5);

    vec3 col = mix(cloud_color, bg_color, 1.0 - exp(-0.000001 * fog_dist * fog_dist));

    fragColor = vec4(col, 0.8);
}