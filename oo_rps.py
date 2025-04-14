import random
import os

class Player:

    def __init__(self):
        self.move = None


class Human(Player):
    def __init__(self):
        super().__init__()


    def choose(self):
        prompt = 'Please choose rock, paper, scissors, lizard, or spock: '

        while True:
            choice = input(prompt).lower()
            print('')
            if choice in Move.CHOICES:
                break

            print(f'Sorry,  {choice} is not valid')

        self.move = choice

class Computer(Player):
    def __init__(self):
        super().__init__()

    def choose(self):
        self.move = random.choice(Move.CHOICES)

    @property
    def info(self):
        return 'You chose this computer.  This computer chooses randomly...'

class R2D2(Computer):

    def choose(self):
        self.move = 'rock'

    @property
    def info(self):
        return 'You chose R2D2.  R2D2 always chooses rock...'

class HAL(Computer):
    HAL_CHOICES = ('scissors', 'scissors', 'scissors', 'scissors', 'scissors')

    def choose(self):
        self.move = random.choice((Move.CHOICES + HAL.HAL_CHOICES))

    @property
    def info(self):
        return 'You chose HAL. HAL is more likely to choose scissors...'


class Daneel(Computer):

    def choose(self):
        if len(RPSGame.move_history[0]) < 1:
            self.move = random.choice(Move.CHOICES)
        else:
            self.move = RPSGame.move_history[0][-1]

    @property
    def info(self):
        return 'You chose Daneel. \n' \
        'After the first move, Daneel will always choose your last move...'

class Move:
    CHOICES = ('rock', 'paper', 'scissors', 'lizard', 'spock')

    def __init__(self, defeats):
        self.defeats = defeats

    def __eq__(self, other):
        return other == self.__class__.__name__.lower()

class Rock(Move):
    def __init__(self):
        super().__init__(['lizard', 'scissors'])

class Paper(Move):
    def __init__(self):
        super().__init__(['rock', 'spock'])

class Scissors(Move):
    def __init__(self):
        super().__init__(['lizard', 'paper'])

class Lizard(Move):
    def __init__(self):
        super().__init__(['paper', 'spock'])

class Spock(Move):
    def __init__(self):
        super().__init__(['rock', 'scissors'])


class RPSGame:
    human_score = 0
    computer_score = 0
    WINNING_SCORE = 3
    move_history = [[],[]]

    def __init__(self):
        self._human = Human()
        self._computer = None
        self._moves = (Rock(), Paper(), Scissors(), Lizard(), Spock())

    def _display_welcome_message(self):
        print('Welcome to Rock Paper Scissors!')

    def _display_rules(self):
        print('')
        print('Rock crushes Lizard and Scissors')
        print('')
        print('Paper covers Rock and disproves Spock')
        print('')
        print('Scissors cut Paper and decapitate Lizard')
        print('')
        print('Lizard eats Paper and poisons Spock')
        print('')
        print('Spock vaporizes Rock and smashes Scissors')
        print('')
        print('Game is best of 5.  First player to 3 wins the match!')

    def _select_robot(self):
        prompt = 'Select your opponent. \n'\
        '1) R2D2 2) HAL 3) Daneel 4) This Computer (select 1, 2, 3, or 4) '

        while True:
            choice = input(prompt)
            if choice in ['1', '2', '3', '4']:
                break

            print(f'Sorry, {choice} is not valid. Please select 1, 2, 3, or 4')

        match choice:
            case '1':
                self._computer = R2D2()
            case '2':
                self._computer = HAL()
            case '3':
                self._computer = Daneel()
            case '4':
                self._computer = Computer()

        print(f'{self._computer.info}')

    def _display_goodbye_message(self):
        print('Thanks for playing Rock Paper Scissors Lizard Spock.  Goodbye!')

    def _human_wins(self):
        human_move = self._human.move
        computer_move  = self._computer.move

        for choice in self._moves:
            if human_move == choice and computer_move in choice.defeats:
                return True


    def _computer_wins(self):
        human_move = self._human.move
        computer_move = self._computer.move

        for choice in self._moves:
            if computer_move == choice and human_move in choice.defeats:
                return True



    def _display_winner(self):
        human_move = self._human.move
        computer_move = self._computer.move

        print(f'You chose: {human_move}')
        print(f'The computer chose: {computer_move}')

        if self._human_wins():
            print('')
            print('You win!')
        elif self._computer_wins():
            print('')
            print('Computer wins!')
        else:
            print('')
            print("It's a tie!")

    def _display_score(self):
        if self._human_wins():
            RPSGame.human_score += 1
        elif self._computer_wins():
            RPSGame.computer_score += 1
        print('')
        print(f"The score is Player: {RPSGame.human_score} " \
              f"Computer: {RPSGame.computer_score}")
        print('')

    def _display_move_history(self):
        human_move = self._human.move
        computer_move = self._computer.move

        RPSGame.move_history[0].append(human_move)
        RPSGame.move_history[1].append(computer_move)
        print(f'User move history: {self.move_history[0]}')
        print(f'Computer move history: {self.move_history[1]}')
        print('')

    def _winning_score(self):
        if RPSGame.human_score == RPSGame.WINNING_SCORE:
            print('YOU WIN THE MATCH!')
        elif RPSGame.computer_score == RPSGame.WINNING_SCORE:
            print('COMPUTER WINS THE MATCH!')
        return RPSGame.WINNING_SCORE in [RPSGame.human_score, RPSGame.computer_score]

    def _play_again(self):
        while True:
            answer = input('Would you like to play again? (y/n) ')
            if answer.lower() not in ['y', 'yes', 'n', 'no']:
                print(f'{answer} is not a valid choice')
            else:
                break
        return answer.lower() in ['y', 'yes']

    def _clear_terminal(self):
        os.system('clear')

    def play(self):
        self._clear_terminal()
        self._display_welcome_message()
        self._display_rules()
        while True:
            self._select_robot()
            while True:
                self._human.choose()
                self._computer.choose()
                self._display_winner()
                self._display_score()
                self._display_move_history()
                if self._winning_score():
                    break
            if self._play_again():
                RPSGame.computer_score = 0
                RPSGame.human_score = 0
                self._clear_terminal()
            else:
                break

        self._display_goodbye_message()

RPSGame().play()
