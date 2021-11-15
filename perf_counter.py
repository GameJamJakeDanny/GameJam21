import arcade
import timeit
FPS = 60
class PerfCounter:
    def __init__(self, window):
        self.window = window
        self.fps = 0
        self.frame_count = 0
        self.fps_start_timer = 0
        self.start_time = 0
        self.update_start_time = 0
        self.draw_start_time = 0
        self.SW = self.window.width
        self.SH = self.window.height
        self.processing_time = 0
        self.draw_time = 0

    def start_update(self):
        self.update_start_time = timeit.default_timer()

    def end_update(self):
        self.processing_time = timeit.default_timer() - self.update_start_time

    def start_draw(self):
        self.draw_start_time = timeit.default_timer()

        # --- Calculate FPS
        fps_calculation_freq = FPS
        # Once every 60 frames, calculate our FPS

        if self.frame_count % fps_calculation_freq == 0:
            # Do we have a start time?
            if self.fps_start_timer is not None:
                # Calculate FPS
                total_time = timeit.default_timer() - self.fps_start_timer
                self.fps = fps_calculation_freq / total_time
            # Reset the timer
            self.fps_start_timer = timeit.default_timer()
        # Add one to our frame count
        self.frame_count += 1

    def end_draw(self):
        output = f"Processing time: {self.processing_time:.4f}"
        arcade.draw_text(output, 20, self.SH - 40, arcade.color.BLACK, 18)

        output = f"Drawing time: {self.draw_time:.4f}"
        arcade.draw_text(output, 20, self.SH - 60, arcade.color.BLACK, 18)

        if self.fps is not None:
            output = f"FPS: {self.fps:.0f}"
            arcade.draw_text(output, 20, self.SH - 80, arcade.color.BLACK, 18)
        # self.cursor.draw()
        # Stop the draw timer, and calculate total on_draw time.

        self.draw_time = timeit.default_timer() - self.draw_start_time