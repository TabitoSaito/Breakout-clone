import turtle
import random

PADDLE_WIDTH = 70
PADDLE_MOVE_DISTANCE = 20

GAME_WIDTH = 800
GAME_HEIGHT = 800


def spawn_cubs() -> list:
    cubs: list = []

    for i in range(1, int((GAME_HEIGHT/25)/3)):
        for j in range(1, int(GAME_WIDTH/25)):
            cubs.append(Block(x=j*25-(GAME_WIDTH/2), y=-(i*25)+GAME_HEIGHT/2, color="red"))

    return cubs


def setup_field() -> list:
    painter = turtle.Turtle()
    painter.speed("fastest")
    painter.hideturtle()
    painter.penup()
    painter.teleport(y=(GAME_HEIGHT / 2), x=(GAME_WIDTH / 2))
    painter.pendown()

    painter.goto(y=-(GAME_HEIGHT / 2), x=(GAME_WIDTH / 2))
    painter.goto(y=-(GAME_HEIGHT / 2), x=-(GAME_WIDTH / 2))
    painter.goto(y=(GAME_HEIGHT / 2), x=-(GAME_WIDTH / 2))
    painter.goto(y=(GAME_HEIGHT / 2), x=(GAME_WIDTH / 2))

    return spawn_cubs()


class WindowManager:

    def __init__(self):
        super().__init__()
        self.window = turtle.Screen()
        self.register_rectangle()
        self.window.setup(1.0, 1.0)
        self.window.listen()
        self.window.tracer(0)

    def register_rectangle(self) -> None:
        rect_cors = ((-10, PADDLE_WIDTH), (10, PADDLE_WIDTH), (10, -PADDLE_WIDTH), (-10, -PADDLE_WIDTH))
        self.window.register_shape("rectangle", rect_cors)


class Ball(turtle.Turtle):

    def __init__(self):
        super().__init__()
        self.spawn()

    def spawn(self)  -> None:
        self.shape("circle")
        self.speed("fastest")
        self.penup()

    def move(self) -> None:
        self.forward(5)

    def launch(self) -> None:
        self.setheading(random.randint(10, 170))

    def bounce(self, bounce_surf: str) -> None:
        match bounce_surf:

            case "top":
                new_h: float = self.calc_heading_after_bounce(0)
                self.seth(new_h)

            case "bot":
                new_h: float = self.calc_heading_after_bounce(180)
                self.seth(new_h)

            case "left":
                new_h: float = self.calc_heading_after_bounce(90)
                self.seth(new_h)

            case "right":
                new_h: float = self.calc_heading_after_bounce(270)
                self.seth(new_h)

            case _:
                raise TypeError

    def calc_heading_after_bounce(self, correction_nesw: int) -> float:
        cur_h: float = self.heading()
        cur_h -= correction_nesw

        if cur_h <= 90:
            mirrored: bool = False
        elif cur_h > 90:
            mirror: float = cur_h - 90
            cur_h = 90 - mirror
            mirrored: bool = True

        new_h: float = 360 - random.randint(int(cur_h - 2), int(cur_h + 2))

        if mirrored:
            mirror: float = 270 - new_h
            new_h: float = mirror + 270

        new_h += correction_nesw
        return new_h


class Block(turtle.Turtle):

    def __init__(self, x: int | float, y: int | float, color: str | tuple[int, int, int]):
        super().__init__()
        self.color(color)
        self.cur_x: int | float = x
        self.cur_y: int | float = y

        self.cor_top: tuple[int | float, int | float] = (self.cur_x, self.cur_y + 10)
        self.cor_right: tuple[int | float, int | float] = (self.cur_x + 10, self.cur_y)
        self.cor_bot: tuple[int | float, int | float] = (self.cur_x, self.cur_y - 10)
        self.cor_left: tuple[int | float, int | float] = (self.cur_x - 10, self.cur_y)

        self.spawn()

    def spawn(self) -> None:
        self.penup()
        self.teleport(x=self.cur_x, y=self.cur_y)
        self.shape("square")


class Paddle(turtle.Turtle):

    def __init__(self):
        super().__init__()
        self.spawn()

    def spawn(self) -> None:
        self.penup()
        self.shape("rectangle")
        self.teleport(y=-((GAME_HEIGHT / 2) - 50))

    def move_left(self) -> None:
        if self.pos()[0] >= -((GAME_WIDTH/2) - PADDLE_WIDTH - 20):
            self.back(PADDLE_MOVE_DISTANCE)

    def move_right(self) -> None:
        if self.pos()[0] <= ((GAME_WIDTH / 2) - PADDLE_WIDTH - 20):
            self.forward(PADDLE_MOVE_DISTANCE)


def main():
    window_manager = WindowManager()

    paddle = Paddle()
    ball = Ball()

    cubs: list[Block] = setup_field()

    window_manager.window.onkeypress(fun=paddle.move_left, key="Left")
    window_manager.window.onkeypress(fun=paddle.move_right, key="Right")

    ball.launch()
    won: bool = True

    while len(cubs) != 0:
        window_manager.window.update()
        ball.move()
        if ball.ycor() >= (GAME_HEIGHT/2 - 10):
            ball.bounce("top")
        elif ball.xcor() >= (GAME_HEIGHT/2 - 10):
            ball.bounce("right")
        elif ball.xcor() <= -(GAME_HEIGHT/2 - 10):
            ball.bounce("left")
        elif ball.ycor() <= -(GAME_HEIGHT/2 - 70) and ball.distance((paddle.xcor(), paddle.ycor())) <= PADDLE_WIDTH:
            ball.bounce("bot")
        elif ball.ycor() <= -(GAME_HEIGHT/2):
            ball.hideturtle()
            won: bool = False
            break

        for cub in cubs:
            if ball.distance(x=cub.cur_x, y=cub.cur_y) < 20:
                distans_to_sides = {
                    "top": ball.distance(cub.cor_top),
                    "right": ball.distance(cub.cor_right),
                    "bot": ball.distance(cub.cor_bot),
                    "left": ball.distance(cub.cor_left),
                }
                ball.bounce(min(distans_to_sides, key=distans_to_sides.get))
                cub.hideturtle()
                cubs.remove(cub)

    if won:
        print("you won")
    else:
        print("you lost")

    window_manager.window.exitonclick()


if __name__ == "__main__":
    main()
