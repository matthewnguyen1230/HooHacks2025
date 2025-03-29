import cv2
import time
import random
from HandGestureRecognizer import HandGestureRecognizer

class HandGestureGame:
    def __init__(self):
        self.recognizer = HandGestureRecognizer()
        self.score = 0
        self.lives = 3

    def play_game(self):
        while True:
            result = self.recognizer.recognize_gesture()
            if result:
                print(f"Recognized Letter: {result}")
                self.process_gesture(result)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.recognizer.cap.release()
        cv2.destroyAllWindows()

    def process_gesture(self, gesture):
        # Example game logic based on recognized gestures
        if gesture == "A":
            self.score += 10
            print(f"Score increased by 10! Current score: {self.score}")
        elif gesture == "B":
            self.lives += 1
            print(f"Lives increased by 1! Current lives: {self.lives}")
        elif gesture == "C":
            self.score -= 5
            print(f"Score decreased by 5! Current score: {self.score}")
        elif gesture == "D":
            self.lives -= 1
            print(f"Lives decreased by 1! Current lives: {self.lives}")
            if self.lives == 0:
                print("Game Over!")
                self.game_over()

    def game_over(self):
        print("Game Over! Final Score:", self.score)
        play_again = input("Do you want to play again? (yes/no): ")
        if play_again.lower() == "yes":
            self.score = 0
            self.lives = 3
        else:
            exit()

if __name__ == "__main__":
    game = HandGestureGame()
    game.play_game()
