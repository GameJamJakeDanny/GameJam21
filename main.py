import arcade
from arcade import key as k
from player import Player
from camera import ScrollManager
from controls import Control
SW, SH = arcade.get_display_size(0)
Refresh_Rate = 60

p_speed = 3 / (Refresh_Rate/60)


class Game(arcade.Window):
    def __init__(self, SW, SH, name):
        super(Game, self).__init__(SW, SH, title=name)
        self.set_update_rate(1/Refresh_Rate)
        arcade.set_background_color(arcade.color.CARDINAL)
        self.set_fullscreen(True)
        # create players
        self.player = Player("0.png", SW / 2, SH / 2, 1)
        self.staticp = Player("0.png", SW / 2 + 50, 400, 1)
        # initialize key manager
        self.key_controller = Control()
        # initialize camera controller
        self.camera_controller = ScrollManager(self)
        # calculate view change margins
        margin_lr = SW/2 + self.player.width / 2
        margin_tb = SH/2 + self.player.height / 2
        # how far player has to move in a given direction for camera to move
        self.camera_controller.set_view_change_margins(right=margin_lr, left=margin_lr, top=margin_tb, bottom=margin_tb)
        # set initial view
        self.camera_controller.set_default_view()
        # self.camera_controller.set_view("right", SW)
        # self.camera_controller.set_view("left", 0)
        # self.camera_controller.set_view("bottom", 0)
        # self.camera_controller.set_view("top", SH)
        # basic controls
        self.control_keys = {k.W: {"func": self.player.set_dy, "param": p_speed, "release": self.player.stop_y, "repeat": True},
                             k.A: {"func": self.player.set_dx, "param": -p_speed, "release": self.player.stop_x, "repeat": True},
                             k.S: {"func": self.player.set_dy, "param": -p_speed, "release": self.player.stop_y, "repeat": True},
                             k.D: {"func": self.player.set_dx, "param": p_speed, "release": self.player.stop_x, "repeat": True}
                             }
        # bind each key to an action in the key controller
        for key in self.control_keys:
            func, param, release, repeat = tuple(self.control_keys[key].values())  # get the key action and key parameter from dict
            self.key_controller.bind_key(key, func, param, release, repeat)  # bind key action and set parameter

    # draw scene
    def on_draw(self):
        arcade.start_render()
        self.player.draw()
        self.staticp.draw()

    # update sprites and logic
    def on_update(self, delta_time: float):
        self.key_controller.update()
        self.player.update()


    # register key presses
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol in list(self.control_keys.keys()):
            self.key_controller.on_press(symbol)
        elif symbol == k.C:
            self.camera_controller.output_values()

    # register key releases
    def on_key_release(self, symbol: int, modifiers: int):
        if symbol in list(self.control_keys.keys()):
            self.key_controller.on_release(symbol)


# open game window
def main():
    window = Game(SW, SH, "test")
    arcade.run()


if __name__ == "__main__":
    main()
