import arcade
from arcade import key as k
from player import Player
from camera import ScrollManager
from controls import Control
from enemy import Enemy, Coin
import random
import timeit

SW, SH = arcade.get_display_size(0)
Refresh_Rate = 60

p_speed = 3 / (Refresh_Rate/60)
FPS = 60
# TODO: Player can die
# TODO: Music & Sound effects
# TODO: Main Menu

class Game(arcade.Window):
    def __init__(self, SW, SH, name):
        super(Game, self).__init__(SW, SH, title=name, antialiasing=True)
        self.set_update_rate(1/Refresh_Rate)
        arcade.set_background_color(arcade.color.SKY_BLUE)
        screens = arcade.get_screens()
        screenout = screens[0]
        #get rid of for actual game

        self.set_vsync(True)
        self.set_fullscreen(True,screen=screenout)
        # create players
        self.player = Player(250, SH / 2, .15, hitbox="Detailed")
        self.player.angle = -90
        self.enemies = arcade.SpriteList()
        self.circle_interact = None
        self.count_on_screen = 10
        self.coins = arcade.SpriteList()
        self.points = 0

        self.menuart = arcade.Sprite("Resources/Menu/Menu.png", 1, center_x=SW/2, center_y=SH/2)

        self.menu = True

        self.music = arcade.Sound("Resources/music/music.mp3")
        self.music.play(.4, loop=True)

        self.hit = arcade.Sound("Resources/sound_effects/hit.wav")
        self.collect = arcade.Sound("Resources/sound_effects/collect.wav")

        self.coins.append(Coin(SW * 2, random.randint(0, SH), .06))

        # Variables used to calculate frames per second
        self.frame_count = 0
        self.fps_start_timer = None
        self.fps = None

        self.minsize = .06
        self.maxsize = .12
        # for i in range(50):
        #     yval = random.randint(100, SH - 100)
        #     xval = random.randint(SW, SW * 2)
        #     scale = random.uniform(.05, .12)
        #     enemy = Enemy(xval, yval, scale)
        #     enemy.set_dx(-5)
        #     self.enemies.append(enemy)
        self.generate_enemies(spreadx=SW)

        self.game_over = False
        # enemy = Enemy("Resources/Sprites/Entities/BlueCircle.png", SW/2, SH/2, .08)
        # enemy.set_dx(-5)
        # self.enemies.append(enemy)

        # initialize key manager
        self.key_controller = Control()
        self.show_fps = False
        self.draw_time = 0
        # calculate view change margins

#doesn't have to be a varible
#default speed is 3
#the movement "curves" aka acceleration is player class (player.py)

        self.control_keys = {k.W: {"func": self.player.set_dy, "param": 3.5, "release": self.player.stop_y, "repeat": True},
                             k.A: {"func": self.player.set_dx, "param": -6, "release": self.player.stop_x, "repeat": True},
                             k.S: {"func": self.player.set_dy, "param": -3.5, "release": self.player.stop_y, "repeat": True},
                             k.D: {"func": self.player.set_dx, "param": 2, "release": self.player.stop_x, "repeat": True},
                             k.UP: {"func": self.player.set_dy, "param": 3.5, "release": self.player.stop_y, "repeat": True},
                             k.LEFT: {"func": self.player.set_dx, "param": -6, "release": self.player.stop_x, "repeat": True},
                             k.DOWN: {"func": self.player.set_dy, "param": -3.5, "release": self.player.stop_y, "repeat": True},
                             k.RIGHT: {"func": self.player.set_dx, "param": 2, "release": self.player.stop_x, "repeat": True},
                             k.R: {"func": self.reset, "param": None, "release": None, "repeat": False},
                             k.P: {"func": self.toggle_fps, "param": None, "release": None, "repeat": False}
                             }
        # bind each key to an action in the key controller
        for key in self.control_keys:
            func, param, release, repeat = tuple(self.control_keys[key].values())  # get the key action and key parameter from dict
            self.key_controller.bind_key(key, func, param, release, repeat)  # bind key action and set parameter


        # self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.enemies, 0)

    # draw scene
    def on_draw(self):
        start_time = timeit.default_timer()

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
        arcade.start_render()

        if self.menu:
            self.menuart.draw()
            arcade.draw_text("Press any key to play", SW/2, SH/2, arcade.color.CREAM, 30, anchor_x="center")
            arcade.draw_text("Use [WASD] or arrow keys to move", SW/2, SH/2 - 50, arcade.color.CREAM, 30, anchor_x="center")

        elif not self.game_over:
            self.player.draw()
            self.coins.draw()
            # self.player.draw_hit_box(arcade.color.BLUE, 2)
            self.enemies.draw()
        else:
            self.reset()
            self.game_over = False
        if self.show_fps:
            output = f"Processing time: {self.processing_time:.3f}"
            arcade.draw_text(output, 20, SH - 40, arcade.color.BLACK, 18)

            output = f"Drawing time: {self.draw_time:.3f}"
            arcade.draw_text(output, 20, SH - 60, arcade.color.BLACK, 18)

            if self.fps is not None:
                output = f"FPS: {self.fps:.0f}"
                arcade.draw_text(output, 20, SH - 80, arcade.color.BLACK, 18)
        # self.cursor.draw()
        # Stop the draw timer, and calculate total on_draw time.
        self.draw_time = timeit.default_timer() - start_time
    # update sprites and logic
    def on_update(self, delta_time: float):
        start_time = timeit.default_timer()
        self.key_controller.update()
        if not self.menu:
            self.enemies.update()
            self.player.update()
            self.coins.update()
        if self.circle_interact:
            if arcade.check_for_collision(self.circle_interact, self.player):
                pass
            else:
                self.circle_interact = None
        did_collide = arcade.check_for_collision_with_list(self.player, self.enemies)
        # where the collisions physics happen
        if did_collide:
            self.hit.play(.8)
            circle = did_collide[0]
            self.circle_interact = circle
            if circle.center_x > self.player.center_x:
                self.player.change_x += circle.impact * 1.5
                circle.change_x *= -.6
                # circle.center_x += 5
                # rate at which player is pushed backwards
            elif circle.center_x < self.player.center_x:
                # self.player.change_x -= circle.impact
                self.player.change_x = 0
                self.player.left = circle.right
                circle.change_x -= 3
            if circle.center_y > self.player.center_y + (self.player.width / 2):
                # self.player.change_y = circle.change_x * .2
                circle.change_y = self.player.change_y
            elif circle.center_y < self.player.center_y - (self.player.width / 2):
                # self.player.change_y = - circle.change_x * .2
                circle.change_y = -self.player.change_y
            # self.player.change_y += circle.change_x
            # self.player.set_dx(0)  # set

            circle.change_y = self.player.change_y
            # self.player.center_x -= circle.change_x
        else:
            self.player.set_dx(0)
            pass

        did_get_coin = arcade.check_for_collision_with_list(self.player, self.coins)
        if did_get_coin:
            did_get_coin[0].kill()
            self.points += 10
            self.collect.play(.8)
            self.count_on_screen += 15
            self.generate_enemies(SW)

        # for circle in self.enemies:
        #     did_collide = arcade.check_for_collision_with_list(circle, self.enemies)
            # if did_collide:


        if self.player.center_y < 0:
            self.player.center_y = SH
        elif self.player.center_y > SH:
            self.player.center_y = 0

        if self.player.center_x < -50:
            self.game_over = True


        self.generate_enemies(50)

        # remove circles when they go off screen
        # for circle in self.enemies:
        #     circle_collide = arcade.check_for_collision_with_list(circle, self.enemies)
        #     if circle.center_x < -50:
        #         # circle.center_x = random.randint(SW, SW * 2)
        #         self.enemies.remove(circle)
        #         self.generate_enemies()
            # if circle_collide:
            #     if circle_collide[0].center_x < circle.center_x:
            #         circle_collide[0].center_x -= 4
            #         circle_collide[0].change_x = -7
            #
            #     elif circle_collide[0].center_x > circle.center_x:
            #         circle.center_x -= 4
            #         circle.change_x = -7

        self.processing_time = timeit.default_timer() - start_time

    # register key presses
    def on_key_press(self, symbol: int, modifiers: int):
        if self.menu:
            self.menu = False
        if symbol in list(self.control_keys.keys()):
            self.key_controller.on_press(symbol)
        elif symbol == k.C:
            self.camera_controller.output_values()

    # register key releases
    def on_key_release(self, symbol: int, modifiers: int):
        if symbol in list(self.control_keys.keys()):
            self.key_controller.on_release(symbol)

    def generate_enemies(self, spreadx=300, spready=None):


        count = self.count_on_screen - len(self.enemies)
        for i in range(count):

            c = random.randint(1, 100)
            if c == 15:
                x = random.randint(SW + 50, SW + 100)
                y = random.randint(0, SH)
                coin = Coin(x, y, .06)
                coin.set_dx(-random.randint(3, 5))
                self.coins.append(coin)


            else:
                # randomly assigned position
                x = random.randint(SW + 50, SW + spreadx)
                y = random.randint(0, SH)
                # randomly generate the size of the shape between two values
                minsize = self.minsize
                maxsize = self.maxsize
                scale = random.uniform(minsize, maxsize)
                enemy = Enemy(x, y, scale)
                enemy.set_dx(-5.5 / ((scale/minsize) * .8))
                enemy.impact = enemy.target_dx * (scale / minsize)
                if arcade.check_for_collision_with_list(enemy, self.enemies):
                    enemy.center_x = random.randint(SW + 50, SW + spreadx)
                    enemy.center_y = random.randint(0, SH)
                self.enemies.append(enemy)

    def reset(self):
        self.enemies = arcade.SpriteList()
        self.generate_enemies(spreadx=SW)
        self.player.center_y, self.player.center_x = SH / 2, 250

    def toggle_fps(self):
        if self.show_fps:
            self.show_fps = False
        else:
            self.show_fps = True

# open game window
def main():
    window = Game(SW, SH, "Tri Flow")
    arcade.run()


if __name__ == "__main__":
    main()
