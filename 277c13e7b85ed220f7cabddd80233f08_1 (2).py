import random


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other_dot):
        return self.x == other_dot.x and self.y == other_dot.y


class Ship:
    def __init__(self, length, bow, direction):
        self.length = length
        self.bow = bow
        self.direction = direction
        self.lives = length

    def dots(self):
        ship_dots = []
        x, y = self.bow.x, self.bow.y

        for _ in range(self.length):
            ship_dots.append(Dot(x, y))
            if self.direction == 'horizontal':
                x += 1
            else:
                y += 1

        return ship_dots


class Board:
    def __init__(self, hid=False):
        self.field = [['o'] * 7 for _ in range(7)]
        self.ships = []
        self.hid = hid
        self.live_ships = 7  # Общее количество кораблей

    def add_ship(self, ship):
        for dot in ship.dots():
            if self.out(dot) or self.field[dot.x][dot.y] == '■':
                raise Exception("Невозможно разместить корабль здесь")
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if self.out(Dot(dot.x + i, dot.y + j)):
                        continue
                    if self.field[dot.x + i][dot.y + j] == 'o':
                        self.field[dot.x + i][dot.y + j] = '.'
        for dot in ship.dots():
            self.field[dot.x][dot.y] = '■'
        self.ships.append(ship)
        #self.live_ships += 1
        #self.contour(ship)

    def contour(self,  ship):

        for dot in ship.dots():
            for i in range(-1, 2):
                for j in range(-1, 2):
                    near = Dot(dot.x + i, dot.y + j)
                    if not self.out(near) and self.field[near.x][near.y] == 'o':
                        self.field[x][y] = '.'

    @classmethod
    def out(cls, dot):
        return not (0 <= dot.x < 6 and 0 <= dot.y < 6)

    def shot(self, dot):
        if self.out(dot):
            raise Exception("Выстрел за пределы доски")
        if self.field[dot.x][dot.y] in ['X', 'T']:
            raise Exception("Вы уже стреляли в эту клетку")

        if self.field[dot.x][dot.y] == '■':
            for ship in self.ships:
                if dot in ship.dots():
                    ship.lives -= 1
                    if ship.lives == 0:
                        self.live_ships -= 1
                        self.field[dot.x][dot.y] = 'X'
                        self.contour(ship)
                        print("Корабль потоплен!")
                    else:
                        self.field[dot.x][dot.y] = 'X'
                        print("Попадание!")
                    break
        else:
            self.field[dot.x][dot.y] = 'T'
            print("Промах!")

    def display(self):
        for i in range(6):
            for j in range(6):
                if j == 0:
                    print("|", end=" ")
                if self.hid and self.field[i][j] == '■':
                    print(' ', end=" ")
                else:
                    print(self.field[i][j], end=" ")
                if j == 5:
                    print("|")
        print("-" * 23)


class Player:
    def __init__(self, board, enemy_board):
        self.board = board
        self.enemy_board = enemy_board

    def ask(self):
        while True:
            try:
                x, y = map(int, input("Введите координаты выстрела (y, x)(от 0 до 5): ").split())
                shot_dot = Dot(x, y)
                if self.board.out(shot_dot):
                    print("Координаты выстрела за пределами доски. Попробуйте еще раз.")
                    continue
                return shot_dot
            except ValueError:
                print("Некорректный ввод. Введите два целых числа через пробел.")

    def move(self):
        while True:
            try:
                shot_dot = self.ask()
                self.enemy_board.shot(shot_dot)
                break
            except Exception as e:
                print(e)
                continue


class AI(Player):
    def ask(self):
        while True:
            x, y = random.randint(0, 6), random.randint(0, 6)
            shot_dot = Dot(x, y)
            if self.board.out(shot_dot):
                continue
            return shot_dot


class User(Player):
    def ask(self):
        return super().ask()


class Game:
    def __init__(self):
        self.user_board = Board()
        self.ai_board = Board(hid=True)
        self.user = User(self.user_board, self.ai_board)
        self.ai = AI(self.ai_board, self.user_board)

    def random_board(self):  # Генерация случайной доски с кораблями
        ship_lengths = [3, 2, 2, 1, 1, 1, 1]
        for length in ship_lengths:
            while True:
                x, y = random.randint(0, 6), random.randint(0, 6)
                direction = random.choice(['horizontal', 'vertical'])
                bow = Dot(x, y)
                try:
                    ship = Ship(length, bow, direction)
                    self.ai_board.add_ship(ship)
                    break
                except Exception:
                    continue

    def greet(self):
        print("Добро пожаловать в игру 'Морской бой'!")
        print("Вы играете против компьютера.")
        print("Ваша доска:")
        self.user_board.display()
        print("Для начала игры компьютер случайным образом разместит корабли на своей доске.")

    def loop(self):
        while True:
            print("Ваш ход:")
            self.user.move()
            self.user_board.display()
            if self.ai_board.live_ships == 0:
                print("Вы победили! Поздравляем!")
                break

            print("Ход компьютера:")
            self.ai.move()
            self.ai_board.display()
            if self.user_board.live_ships == 0:
                print("Компьютер победил. Попробуйте еще раз.")
                break

    def start(self):
        self.greet()
        self.random_board()
        self.loop()


if __name__ == '__main__':
    # game = Game()
    # game.start
    game = Game()
    game.start()
