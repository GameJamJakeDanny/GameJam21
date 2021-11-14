import arcade

#player can be changed as much as you want and nothing will break as long as long as it works within player.pu

class Player(arcade.Sprite):
    def __init__(self, texturepath, x, y, scale, hitbox):
        super(Player, self).__init__(texturepath, scale, center_x=x, center_y=y, hit_box_algorithm=hitbox)
        #accerlation is how quickly you change speed
        #if i want to make a change to player acceleration speed I have to split this self.accel to a new
        #varible simaler to how the self.decelx and self.decly varibles are
        self.accelx = .35 #former .25
        #higher values are faster because you accelerate faster
        self.accely = .85 #former 1
        #higher decel makes you decelerate faster
        self.decelx = .1
        #lower decel makes u accelerate backwards slower
        self.decely = .8
        #no diferentation decelerating due to your actions and due to collisions
        self.target_dx = 0
        self.target_dy = 0
        self.pushed = True

    def update(self, delta_time: float = 1/60):
        # accelerate
        if self.change_x < self.target_dx:
            self.change_x += self.accelx
        elif self.change_x > self.target_dx:
            self.change_x -= self.decelx

        # decelerate
        if self.change_y < self.target_dy:
            self.change_y += self.accely
        elif self.change_y > self.target_dy:
            self.change_y -= self.decely

        # update position
        self.center_x += self.change_x
        self.center_y += self.change_y

    def set_dx(self, dx):
        self.target_dx = dx

    def set_dy(self, dy):
        self.target_dy = dy

    def target_move(self, dx):
        self.pushed = True

    def stop_x(self):
        self.target_dx = 0

    def stop_y(self):
        self.target_dy = 0

    def move_up(self):
        pass

    def move_down(self):
        pass