import os


# manages high score
class ScoreManager:
    def __init__(self):
        self.score = 0
        # check if the save file exists
        if os.path.exists("SaveFiles/score.txt"):
            # read from existing save file for high score
            with open("SaveFiles/score.txt", "r") as score:
                self.high_score = int(score.read())  # convert string stored in file to an integer
        else:
            # create a new save file for high score
            with open("SaveFiles/score.txt", "w") as score:
                self.high_score = 0  # initialize high score as 0
                score.write("0")

    def add_score(self, n):
        self.score += n

    def remove_score(self, n):
        self.score -= n

    def reset_score(self):
        self.score = 0

    def get_score(self):
        return self.score

    def reset_highscore(self):
        self.high_score = 0
        # reset high score file
        with open("SaveFiles/score.txt", "w") as score:
            score.write("0")

    def get_highscore(self):
        return self.high_score

    def write_highscore(self, n):
        self.high_score = n
        with open("SaveFiles/score.txt", "w") as score:
            score.write(str(n))  # convert int to string to be written to file

    def game_over(self):
        # save score as highscore if it is higher than previous record
        if self.score > self.high_score:
            self.write_highscore(self.score)
        self.reset_score()


score_tracker = ScoreManager()