import arcade
from arcade import key as k
from player import Player
from camera import ScrollManager
from controls import Control
from enemy import Enemy, Coin
import random
import timeit
from score_manager import score_tracker
from perf_counter import PerfCounter

SW, SH = arcade.get_display_size(0)
Refresh_Rate = 60

p_speed = 3 / (Refresh_Rate/60)
FPS = 60

# it does work between resets

class Game(arcade.Window):
    def __init__(self, SW, SH, name):
        super(Game, self).__init__(SW, SH, title=name, antialiasing=True)
        self.set_update_rate(1/Refresh_Rate)
        arcade.set_background_color(arcade.color.SKY_BLUE)
        # set the active monitor
        screens = arcade.get_screens()
        screenout = screens[0]
        # initialize the performance counter
        self.perf_counter = PerfCounter(self)
        # initialiaze window settings
        self.set_vsync(True)
        self.set_fullscreen(True,screen=screenout)
        self.set_mouse_visible(False)
        # create player
        self.player = Player(250, SH / 2, .15, hitbox="Detailed")
        self.player.angle = -90

        # initialize score tracker
        self.score_tracker = score_tracker

        # create spritelists
        self.enemies = arcade.SpriteList()
        self.coins = arcade.SpriteList()
        self.players = arcade.SpriteList()
        # add player to spritelist (only one sprite, so not necessary, but useful for performance reasons)
        self.players.append(self.player)
        # create initial coin
        self.coins.append(Coin(SW * 2, random.randint(0, SH), .06))
        # set initial circle count
        self.count_on_screen = 10

        # initialize menu art
        self.menuart = arcade.Sprite("Resources/Menu/Menu.png", 1, center_x=SW/2, center_y=SH/2)
        # start on main menu
        self.menu = True

        # create background music
        self.music = arcade.Sound("Resources/music/music.mp3")
        self.music.play(.25, loop=True)
        # initialize sound effects
        self.hit = arcade.Sound("Resources/sound_effects/hit.wav")
        self.collect = arcade.Sound("Resources/sound_effects/collect.wav")

        self.circle_interact = None

        # min and max enemy scale
        self.minsize = .06
        self.maxsize = .12
        # generate initial set of enemies
        self.generate_enemies(spreadx=SW)
        # game is not over
        self.game_over = False

        # initialize key manager
        self.key_controller = Control()
        # variable to decide whether to display performance stats
        self.show_fps = False



        '''
        To create a new control, add a key to the dictionary and set the value of it to another dictionary
        This dictionary should contain 4 key values (not keyboard keys, dict keys), with a value assigned to each
        These four keys and values are as follows
            "func" - the function to be called on keypress, make sure not to include '()' as that will call the 
                    function instead of passing it through. (Ex: "func": move_forward NOT "func": move_forward())
            "param" - the parameter(s) to be passed through upon calling the function. Currently only supports one value
                        set param to None if there is no value to be passed through. (Ex: "param": None)
            "release" - the function to be called on key release. For example, when W is released the player should stop
                        moving forward. (Ex: "release": stop_moving) remember not to include '()'. This does not support
                        parameters, however
                        
            "repeat" - Should the function continue to be called as long as key is pressed, or should it only be called
                        once regardless of how long the key is held. Set equal to True or False. (Ex: "repeat": True)
                
        '''
        # param doesn't have to be a varible
        # default speed is 3
        # the movement "curves" aka acceleration is player class (player.py)
        # setup the controls dictionary
        self.control_keys = {k.W: {"func": self.player.set_dy, "param": 3.5, "release": self.player.stop_y, "repeat": True},
                             k.A: {"func": self.player.set_dx, "param": -6, "release": self.player.stop_x, "repeat": True},
                             k.S: {"func": self.player.set_dy, "param": -3.5, "release": self.player.stop_y, "repeat": True},
                             k.D: {"func": self.player.set_dx, "param": 2, "release": self.player.stop_x, "repeat": True},
                             k.UP: {"func": self.player.set_dy, "param": 3.5, "release": self.player.stop_y, "repeat": True},
                             k.LEFT: {"func": self.player.set_dx, "param": -6, "release": self.player.stop_x, "repeat": True},
                             k.DOWN: {"func": self.player.set_dy, "param": -3.5, "release": self.player.stop_y, "repeat": True},
                             k.RIGHT: {"func": self.player.set_dx, "param": 2, "release": self.player.stop_x, "repeat": True},
                             k.R: {"func": self.reset, "param": None, "release": None, "repeat": False},
                             k.P: {"func": self.toggle_fps, "param": None, "release": None, "repeat": False},
                             k.L: {"func": self.score_tracker.reset_highscore, "param": None, "release": None, "repeat": False}
                             }
        # bind each key to an action in the key controller
        for key in self.control_keys:
            func, param, release, repeat = tuple(self.control_keys[key].values())  # get the key actions and parameters
            self.key_controller.bind_key(key, func, param, release, repeat)  # bind key action and set parameter

    # draw scene
    def on_draw(self):
        self.perf_counter.start_draw()
        arcade.start_render()
        if self.menu:
            # draw background art for main menu
            self.menuart.draw()
            # draw menu text
            arcade.draw_text("Press any key to play", SW/2, SH/2, arcade.color.CREAM, 30, anchor_x="center")
            arcade.draw_text("Use [WASD] or arrow keys to move", SW/2, SH/2 - 50, arcade.color.CREAM, 30, anchor_x="center")
        # only draw sprites if game is not over
        elif not self.game_over:
            # draw all sprites
            self.player.draw()
            self.coins.draw()
            self.enemies.draw()
            # draw score text
            score = self.score_tracker.get_score()
            arcade.draw_text(str(score), SW/2, SH - 40, arcade.color.BLACK, 30, anchor_x="center")
            highscore = "Highscore: " + str(self.score_tracker.get_highscore())
            arcade.draw_text(highscore, SW / 2, SH - 65, arcade.color.BLACK, 15, anchor_x="center")
        else:
            # reset the game if it is over
            self.reset()
            self.game_over = False  # set game over back to false

        if self.show_fps:
            self.perf_counter.end_draw()

    # update sprites and logic
    def on_update(self, delta_time: float):
        self.perf_counter.start_update()
        self.key_controller.update()
        # if game is running (not in menu)
        if not self.menu:
            # update positions of all sprites
            self.player.update()
            self.enemies.update()
            self.coins.update()
            # points are calculated in multiple places, add them together for overall score

        '''
            player should be unable to interact with the same circle between two adjacent frames.
            this isn't technically possible anyways but sometimes game registers incorrectly, resulting in doubled up 
            physics calculations. This if/else statement detects an incorrect registration and prevents calculations from 
            happening
        '''
        if self.circle_interact:
            if arcade.check_for_collision(self.circle_interact, self.player):  # if game thinks player hits same circle
                return  # exit function and prevent further calculations
            else:
                self.circle_interact = None

        # check for collision between player and circles
        did_collide = arcade.check_for_collision_with_list(self.player, self.enemies)
        # where the collisions physics happen
        if did_collide:
            circle: Enemy = did_collide[0]  # set the active object for calculation to the first item in the collision list
            self.hit.play(.8)  # play a sound upon interaction between player and circle
            self.score_tracker.add_score(1)  # add a point for player interaction with a circle
            # current circle being interacted with
            self.circle_interact = circle
            # if circle is in front of player
            if circle.center_x > self.player.center_x:
                # make player bounce away from the circle on impact
                self.player.change_x += circle.impact * 1.5
                circle.change_x *= -.6  # make the circle bounce away from the player impact
            # if circle is behind player (player hits circle when moving backwards)
            elif circle.center_x < self.player.center_x:
                # self.player.change_x -= circle.impact
                self.player.change_x = 0  # halt player movement when running into circle
                self.player.left = circle.right  # prevent player from passing through circle (will stop sprite at edge)
                circle.change_x -= 3  # make circle bounce away from player
            # if circle is above player
            if circle.center_y > self.player.center_y + (self.player.width / 2):
                # make player bounce in opposite y direction of collision
                self.player.change_y -= circle.impact * .4
                # make the circle bounce in the y direction of the player collision
                circle.change_y = self.player.change_y
            # if circle is below player
            elif circle.center_y < self.player.center_y - (self.player.width / 2):
                # make player bounce in opposite y direction of collision
                self.player.change_y += circle.impact * .4
                # make the circle bounce in the y direction of the player collision
                circle.change_y = self.player.change_y




        # set the players rate of change back to 0 when it's not colliding with objects
        else:
            self.player.set_dx(0)
            pass

        # when player collects a coin
        did_get_coin = arcade.check_for_collision_with_list(self.player, self.coins)
        if did_get_coin:
            did_get_coin[0].kill()  # delete the coin since it has been collected
            self.score_tracker.add_score(100)  # add 100 points to score
            self.collect.play(.8)  # play the coin collect sound
            self.count_on_screen += 10  # increase generation count of circles
            self.generate_enemies(SW)  # generate the additional enemies

        # loop player position to opposite side when going off top or bottom of the screen
        if self.player.center_y < 0:
            self.player.center_y = SH
        elif self.player.center_y > SH:
            self.player.center_y = 0

        # player dies if they fall of left edge of screen
        if self.player.center_x < -50:
            self.game_over = True
        # player is unable to go past right edge of screen
        elif self.player.center_x > SW - (self.player.width / 2):
            self.player.right = SW
        # generate new enemies 50 pixels of the right of the screen
        self.generate_enemies(spreadx=50)

        self.perf_counter.end_update()

    # register key presses
    def on_key_press(self, symbol: int, modifiers: int):
        # press any key to get past the menu
        if self.menu:
            self.menu = False
        # only register keypress if it is a bound control
        if symbol in list(self.control_keys.keys()):
            self.key_controller.on_press(symbol)  # activate function bound to keypress

    # register key releases
    def on_key_release(self, symbol: int, modifiers: int):
        # only register keypress if it is a bound control
        if symbol in list(self.control_keys.keys()):
            self.key_controller.on_release(symbol)  # activate the function bound to key release

    def generate_enemies(self, spreadx=300, spready=None):
        # calculate amount of enemies to generate by subtracting the current amount from how many there should be
        count = self.count_on_screen - len(self.enemies)
        # generate enemies for count
        for i in range(count):
            # generate a number to pick whether to generate coin or enemy. Odds are weighted 40 to 1 in favor of enemies
            c = random.choices([1,2], [1, 40 + (self.count_on_screen/10)])[0]  # odds scale with number of enemies
            # if c is 1, generate a coin instead of an enemy
            if c == 1:
                # generate random x and y position
                x = random.randint(SW + 50, SW + 100)
                y = random.randint(0, SH)
                coin = Coin(x, y, .06)  # create instance of coin
                coin.set_dx(-random.randint(3, 5))  # set a random x speed between -3 and -5
                self.coins.append(coin)  # add coin to main spritelist of coins

            else:
                # randomly assigned position
                x = random.randint(SW + 50, SW + spreadx)
                y = random.randint(0, SH)
                # min and max enemy sizes
                minsize = self.minsize
                maxsize = self.maxsize
                scale = random.uniform(minsize, maxsize)  # randomly generate the scale of the enemy
                enemy = Enemy(x, y, scale)  # create the instance of the enemy
                # regenerate circle at different position if it overlaps with existing circle
                if arcade.check_for_collision_with_list(enemy, self.enemies):
                    enemy.center_x = random.randint(SW + 50, SW + spreadx)
                    enemy.center_y = random.randint(0, SH)
                self.enemies.append(enemy)  # add the circle to the main enemy spritelist

    def reset(self):
        # delete all the sprites onscreen
        self.enemies = arcade.SpriteList()
        self.coins = arcade.SpriteList()
        # add an initial coin
        self.coins.append(Coin(SW * 1.5, random.randint(50, SH - 50), .06))
        self.count_on_screen = 10  # same as initial value (reset difficulty)
        # reset the score
        self.score_tracker.game_over()
        self.points = 0
        # generate the enemies with whole screen spread
        self.generate_enemies(spreadx=SW)
        # reset player position
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
