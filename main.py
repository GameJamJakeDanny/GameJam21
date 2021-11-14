import arcade
from arcade import key as k
from player import Player
from camera import ScrollManager
from controls import Control
from enemy import Enemy
import random

SW, SH = arcade.get_display_size(0)
Refresh_Rate = 60

p_speed = 3 / (Refresh_Rate/60)


class Game(arcade.Window):
    def __init__(self, SW, SH, name):
        super(Game, self).__init__(SW, SH, title=name)
        self.set_update_rate(1/Refresh_Rate)
        arcade.set_background_color(arcade.color.WHITE)
        self.set_fullscreen(True)
        # create players
        self.player = Player("Resources/Sprites/Entities/MadeTriangle.png", 250, SH / 2, .15, hitbox="Detailed")
        self.player.angle = -90
        self.enemies = arcade.SpriteList()

        for i in range(50):
            yval = random.randint(100, SH - 100)
            xval = random.randint(SW, SW * 2)
            scale = random.uniform(.05, .12)
            enemy = Enemy("Resources/Sprites/Entities/BlueCircle.png", xval, yval, scale)
            enemy.set_dx(-5)
            self.enemies.append(enemy)
        # enemy = Enemy("Resources/Sprites/Entities/BlueCircle.png", SW/2, SH/2, .08)
        # enemy.set_dx(-5)
        # self.enemies.append(enemy)

        # initialize key manager
        self.key_controller = Control()

        # calculate view change margins

#doesn't have to be a varible
#default speed is 3
#the movement "curves" aka acceleration is player class (player.py)

        self.control_keys = {k.W: {"func": self.player.set_dy, "param": 6, "release": self.player.stop_y, "repeat": True},
                             k.A: {"func": self.player.set_dx, "param": -10, "release": self.player.stop_x, "repeat": True},
                             k.S: {"func": self.player.set_dy, "param": -6, "release": self.player.stop_y, "repeat": True},
                             k.D: {"func": self.player.set_dx, "param": 3, "release": self.player.stop_x, "repeat": True}
                             }
        # bind each key to an action in the key controller
        for key in self.control_keys:
            func, param, release, repeat = tuple(self.control_keys[key].values())  # get the key action and key parameter from dict
            self.key_controller.bind_key(key, func, param, release, repeat)  # bind key action and set parameter


        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.enemies, 0)

    # draw scene
    def on_draw(self):
        arcade.start_render()
        self.player.draw()
        self.player.draw_hit_box(arcade.color.BLUE, 2)
        self.enemies.draw()

    # update sprites and logic
    def on_update(self, delta_time: float):
        self.key_controller.update()
        self.enemies.update()
        self.player.update()
        did_collide = arcade.check_for_collision_with_list(self.player, self.enemies)
        # where the collisions physics happen
        if did_collide:
            circle = did_collide[0]
            self.player.change_x += circle.change_x * 1.5  # rate at which player is pushed backwards
            if circle.center_y > self.player.center_y + (self.player.width / 2):
                self.player.change_y = circle.change_x * .2
                circle.change_y = 4
            elif circle.center_y < self.player.center_y - (self.player.width / 2):
                self.player.change_y = - circle.change_x * .2
                circle.change_y = -4
            # self.player.change_y += circle.change_x
            self.player.set_dx(0)  # set
            circle.change_x *= -.6
            circle.center_x += 5
            circle.change_y = self.player.change_y
            # self.player.center_x -= circle.change_x
        else:
            # self.player.set_dx(0)\
            pass

        # for circle in self.enemies:
        #     did_collide = arcade.check_for_collision_with_list(circle, self.enemies)
            # if did_collide:


        if self.player.center_y < 0:
            self.player.center_y = SH
        elif self.player.center_y > SH:
            self.player.center_y = 0


        # remove circles when they go off screen
        for circle in self.enemies:
            if circle.center_x < -50:
                # circle.center_x = random.randint(SW, SW * 2)
                circle.center_x = SW + 100






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
