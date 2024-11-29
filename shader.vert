#version 450

in vec2 in_vert;

out vec2 v_vert;

void main() {
    v_vert = in_vert;
    gl_Position = vec4(in_vert, 0, 1.0);
}
