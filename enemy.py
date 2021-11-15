import arcade
import random
from score_manager import score_tracker

defmin = .06
defmax = .12
class Enemy(arcade.Sprite):
    def __init__(self, x, y, scale, minsize=defmin, maxsize=defmax):
        super(Enemy, self).__init__("Resources/Sprites/Entities/BlueCircle.png", scale, center_x=x, center_y=y)
        self.accel = .25
        self.decel = .1
        self.target_dx = 0
        self.target_dy = 0
        self.impact = 0
        self.set_dx(-5.5 / ((scale / minsize) * .8))
        self.impact = self.target_dx * (scale / minsize)

    def update(self, delta_time: float = 1/60):
        # accelerate
        if self.change_x < self.target_dx:
            self.change_x += self.accel
        elif self.change_x > self.target_dx:
            self.change_x -= self.decel

        # decelerate
        if self.change_y < self.target_dy:
            self.change_y += self.accel
        elif self.change_y > self.target_dy:
            self.change_y -= self.decel

        # update position
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.center_x < -50:
            # remove from any active spritelists
            self.kill()
            # add score based on size of circle. max score to add is 10
            score_tracker.add_score(int(10 * (self.scale/.12)))

    def set_dx(self, dx):
        self.target_dx = dx

    def set_dy(self, dy):
        self.target_dy = dy

    def stop_x(self):
        self.target_dx = 0

    def stop_y(self):
        self.target_dy = 0

    def move_up(self):
        pass

    def move_down(self):
        pass

    def is_off(self):
        if self.center_x < -50:
            self.kill()
            return True
        else:
            return False
# def generate_enemies(count, sizerange, spritelist):
class Coin(arcade.Sprite):
    def __init__(self, x, y, scale):
        super(Coin, self).__init__("Resources/Sprites/Entities/coin.png", scale, center_x=x, center_y=y)
        self.accel = .25
        self.decel = .1
        self.target_dx = -random.randint(3, 5)
        self.target_dy = 0
        self.impact = 0

    def update(self, delta_time: float = 1/60):
        # accelerate
        if self.change_x < self.target_dx:
            self.change_x += self.accel
        elif self.change_x > self.target_dx:
            self.change_x -= self.decel

        # decelerate
        if self.change_y < self.target_dy:
            self.change_y += self.accel
        elif self.change_y > self.target_dy:
            self.change_y -= self.decel

        # update position
        self.center_x += self.change_x
        self.center_y += self.change_y

    def set_dx(self, dx):
        self.target_dx = dx

    def set_dy(self, dy):
        self.target_dy = dy

    def stop_x(self):
        self.target_dx = 0

    def stop_y(self):
        self.target_dy = 0

    def move_up(self):
        pass

    def move_down(self):
        pass
