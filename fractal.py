import moderngl
import numpy as np

class FractalRenderer:
    def __init__(self, ctx):
        self.ctx = ctx

        # Load shaders
        self.program = self.ctx.program(
            vertex_shader=open('shader.vert').read(),
            fragment_shader=open('shader.frag').read()
        )

        # Define the full-screen quad vertices
        self.vertices = np.array([
            # First triangle
            -1.0, -1.0,
             1.0, -1.0,
            -1.0,  1.0,
            # Second triangle
             1.0, -1.0,
             1.0,  1.0,
            -1.0,  1.0
        ], dtype='f4')

        # Create a vertex buffer
        self.vbo = self.ctx.buffer(self.vertices)
        self.vao = self.ctx.simple_vertex_array(self.program, self.vbo, 'in_vert')

        # Set initial uniform values
        self.program['u_center'].value = (0.0, 0.0)  # Initial center
        self.program['u_scale'].value = 200.0           # Initial zoom (scale)
        self.program['u_max_iterations'].value = 500   # Max iterations
        self.program['u_resolution'].value = (2560.0, 1440.0)  # Window size (as floats)
        self.program['u_time'].value = 0.0

    def move_center(self, mx, my, width, height):
        # Normalize mouse position to OpenGL coordinates (-1 to 1 range)
        center = self.program['u_center'].value
        scale = self.program['u_scale'].value

        mouse_x = (mx - width / 2) / (width / 2) / scale + center[0]
        mouse_y = (height / 2 - my) / (height / 2) / scale + center[1]

        # Move center toward mouse slightly, relative to zoom level
        direction_to_mouse = np.array([mouse_x, mouse_y]) - center
        self.program['u_center'].value += direction_to_mouse * 10000 * (scale * 0.008) / scale

    def increment_scale(self, scale):
        # Update the scale uniform value
        zoomchange = self.program['u_scale'].value * scale / 1000
        self.program['u_scale'].value += zoomchange

    def render(self):
        # Render the fractal (draw the full-screen quad)
        self.ctx.clear(0.0, 0.0, 0.0)  # Clear the screen (black background)
        self.vao.render()  # Draw the quad to the screen
    def increment_time(self, time):
        self.program['u_time'].value += time
        if self.program['u_time'].value > 1:
            self.program['u_time'].value = 0