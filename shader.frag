#version 450
in vec2 v_vert;

uniform vec2 u_center;
uniform float u_scale;
uniform int u_max_iterations;
uniform vec2 u_resolution;
uniform float u_time;

out vec4 fragColor;

void main() {
    vec2 p = (v_vert * 0.5 + 0.5) * u_resolution; // Normalized screen coordinates
    p = (p - u_resolution * 0.5) / u_scale + u_center; // Transform coordinates to fractal space

    int iterations = 0;
    vec2 z = p;
    while (dot(z, z) < 4.0 && iterations < u_max_iterations) {
        z = vec2(z.x * z.x - z.y * z.y + p.x, 2.0 * z.x * z.y + p.y);
        iterations++;
    }

    // Calculate color based on the number of iterations
    if (iterations == u_max_iterations) {
        // Inside the Mandelbrot set, color it black
        fragColor = vec4(0.0, 0.0, 0.0, 1.0);
    } else {
        // Outside, color it based on the iteration count
        float t = float(iterations) / float(u_max_iterations); // Normalized iteration count
        fragColor = vec4(t * 0.5 + 0.5, u_time, 1 - u_time, u_time); // Gradient from blue to violet
    }
}
