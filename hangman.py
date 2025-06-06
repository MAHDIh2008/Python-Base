import random
import sys
from typing import List

class Hangman:
    HANGMAN_STAGES = [
        '''
           +---+
               |
               |
               |
              ===
        ''',
        '''
           +---+
           O   |
               |
               |
              ===
        ''',
        '''
           +---+
           O   |
           |   |
               |
              ===
        ''',
        '''
           +---+
           O   |
          /|   |
               |
              ===
        ''',
        '''
           +---+
           O   |
          /|\\  |
               |
              ===
        ''',
        '''
           +---+
           O   |
          /|\\  |
          /    |
              ===
        ''',
        '''
           +---+
           O   |
          /|\\  |
          / \\  |
              ===
        '''
    ]

    def __init__(self):
        self.words = ['python', 'programming', 'hangman', 'developer', 'computer']
        self.secret_word = random.choice(self.words).lower()
        self.guessed_letters = set()
        self.attempts_left = len(self.HANGMAN_STAGES) - 1
        self.current_stage = 0

    def display_word(self):
        display = []
        for letter in self.secret_word:
            if letter in self.guessed_letters:
                display.append(letter)
            else:
                display.append('_')
        return ' '.join(display)

    def guess_letter(self, letter):
        letter = letter.lower()
        if letter in self.guessed_letters:
            print("You already guessed that letter!")
            return False
        
        self.guessed_letters.add(letter)
        if letter not in self.secret_word:
            self.attempts_left -= 1
            self.current_stage += 1
            print("Wrong guess!")
            return False
        return True

    def is_word_guessed(self):
        return all(letter in self.guessed_letters for letter in self.secret_word)

    def is_game_over(self):
        return self.attempts_left <= 0 or self.is_word_guessed()

    def display_game(self):
        print("\n" + self.HANGMAN_STAGES[self.current_stage])
        print(f"Word: {self.display_word()}")
        print(f"Guessed letters: {' '.join(sorted(self.guessed_letters))}")
        print(f"Attempts left: {self.attempts_left}")

def play_game():
    game = Hangman()
    
    print("Welcome to Hangman!")
    print("Guess the word before the man is hanged!")
    
    while not game.is_game_over():
        game.display_game()
        
        try:
            guess = input("Enter a letter: ").lower()
            if len(guess) != 1 or not guess.isalpha():
                print("Please enter a single letter!")
                continue
                
            game.guess_letter(guess)
        except KeyboardInterrupt:
            print("\nGame aborted!")
            return

    game.display_game()
    if game.is_word_guessed():
        print("\nCongratulations! You won!")
        print(f"The word was: {game.secret_word}")
    else:
        print("\nGame over! You lost!")
        print(f"The word was: {game.secret_word}")

def main():
    while True:
        play_game()
        play_again = input("\nPlay again? (y/n): ").lower()
        if play_again != 'y':
            print("Thanks for playing!")
            break

if __name__ == '__main__':
    main()