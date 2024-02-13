#version 330 core

layout (location = 0) out vec4 fragColor;

const vec3 gamma = vec3(2.2);
const vec3 inv_gamma = 1 / gamma;

in vec2 uv;
in vec3 position;
in vec3 normal;

uniform vec3 viewPos;
uniform vec3 lightPos;
uniform sampler2D u_texture_0;
uniform sampler2D u_texture_1;
uniform float water_line;
uniform float time;

void main() {
    vec2 movingUV = uv;
    movingUV.x += time * 0.1;
    movingUV.y += time * 0.05;

    vec3 tex_col = texture(u_texture_0, movingUV).rgb;
    vec3 tex_col_1 = texture(u_texture_1, movingUV).rgb;
    tex_col = mix(tex_col, tex_col_1, 0.5);
    tex_col = pow(tex_col, gamma);

    float fog_dist = gl_FragCoord.z / gl_FragCoord.w;
    float alpha = mix(0.5, 0.0, 1.0 - exp(-0.000002 * fog_dist * fog_dist));

    float fresnel = dot(normalize(viewPos - position), vec3(0.0, 1.0, 0.0));
    fresnel = pow(1.0 - fresnel, 3.0);
    fresnel = mix(0.1, 1.0, fresnel);

    vec3 lightDir = normalize(lightPos - position);
    vec3 viewDir = normalize(viewPos - position);
    vec3 reflectDir = reflect(-lightDir, normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32.0);
    vec3 specular = vec3(1.0, 1.0, 1.0) * spec;

    tex_col = pow(tex_col, inv_gamma);
    fragColor = vec4((tex_col + specular) * fresnel, alpha);
}