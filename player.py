import arcade


class Player(arcade.Sprite):
    def __init__(self, texturepath, x, y, scale):
        super(Player, self).__init__(texturepath, scale, center_x=x, center_y=y)
        self.accel = .25
        self.decel = .25
        self.target_dx = 0
        self.target_dy = 0

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