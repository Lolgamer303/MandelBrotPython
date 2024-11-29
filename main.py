import moderngl
import glfw
import fractal as fra

def main():
    if not glfw.init():
        raise Exception("glfw init failed")

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.SAMPLES, 16)  # Enable 4x multisampling

    window = glfw.create_window(2560, 1440, "Fractal Viewer", None, None)
    if not window:
        glfw.terminate()
        raise Exception("glfw window creation failed")
    
    glfw.make_context_current(window)

    ctx = moderngl.create_context()

    fractal = fra.FractalRenderer(ctx)

    def scroll(window, xoffset, yoffset):
        fractal.increment_scale(yoffset * 40)
        # Get current mouse position in window coordinates
        mx, my = glfw.get_cursor_pos(window)
        width, height = glfw.get_window_size(window)
        fractal.move_center(mx, my, width, height)

    glfw.set_scroll_callback(window, scroll)

    while not glfw.window_should_close(window):
        fractal.increment_time(0.001)
        ctx.clear(1.0, 1.0, 1.0)
        fractal.render()
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()