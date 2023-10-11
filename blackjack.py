import tkinter as tk
from tkinter import messagebox
import random

# Function to calculate the total value of a hand
def calculate_hand_value(hand):
    value = sum(hand)
    if 11 in hand and value > 21:
        value -= 10
    return value

# Function to deal a card from the deck
def deal_card():
    return random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11])

class BlackjackGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Blackjack")
        self.geometry("800x600")
        self.configure(bg="#222222")

        self.wins = 0
        self.losses = 0
        self.draws = 0

        custom_image_path = "logo.png" 
        self.bg_image = tk.PhotoImage(file=custom_image_path)

        self.home_frame = tk.Frame(self, bg="#222222")
        self.home_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Resize the image to fit the screen better
        resized_image = self.bg_image.subsample(3, 3)
        self.bg_label = tk.Label(self.home_frame, image=resized_image, bg="#222222")
        self.bg_label.image = resized_image
        self.bg_label.pack(fill=tk.BOTH, expand=True)

        self.title_label = tk.Label(self.home_frame, text="Welcome to Blackjack!", font=("Arial", 36, "bold"), bg="#222222", fg="white")
        self.title_label.pack(pady=20)

        # Adjust button placement
        self.play_button = tk.Button(self.home_frame, text="Play", command=self.start_game, font=("Arial", 24), bg="#007BFF", fg="black", activebackground="#0056b3")
        self.play_button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

    def start_game(self):
        self.home_frame.destroy()
        self.blackjack_frame = tk.Frame(self, bg="#1C0920")
        self.blackjack_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        self.deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4
        self.player_hand = [deal_card(), deal_card()]
        self.dealer_hand = [deal_card(), deal_card()]

        self.header_label = tk.Label(self.blackjack_frame, text="Blackjack", font=("Arial", 36, "bold"), bg="#1C0920", fg="white")
        self.header_label.pack(pady=20)

        self.dealer_label = tk.Label(self.blackjack_frame, text="Dealer's cards: ??", font=("Arial", 24), bg="#1C0920", fg="white")
        self.dealer_label.pack(pady=10)

        self.player_label = tk.Label(self.blackjack_frame, text="Your cards:", font=("Arial", 24), bg="#1C0920", fg="white")
        self.player_label.pack(pady=10)

        self.player_cards_label = tk.Label(self.blackjack_frame, text=", ".join(map(str, self.player_hand)), font=("Arial", 24), bg="#1C0920", fg="white")
        self.player_cards_label.pack(pady=10)

        self.score_label = tk.Label(self.blackjack_frame, text="Wins: 0 | Losses: 0 | Draws: 0", font=("Arial", 20), bg="#1C0920", fg="white")
        self.score_label.pack(pady=10)

        self.button_frame = tk.Frame(self.blackjack_frame, bg="#1C0920")
        self.button_frame.pack(pady=20)

        self.hit_button = tk.Button(self.button_frame, text="Hit", command=self.hit, font=("Arial", 20), bg="#007BFF", fg="black", activebackground="#0056b3")
        self.hit_button.pack(side=tk.LEFT, padx=20)

        self.stand_button = tk.Button(self.button_frame, text="Stand", command=self.stand, font=("Arial", 20), bg="#007BFF", fg="black", activebackground="#0056b3")
        self.stand_button.pack(side=tk.RIGHT, padx=20)

    def deal_card_to_player(self):
        card_value = deal_card()
        self.player_hand.append(card_value)
        self.update_player_cards()

        if calculate_hand_value(self.player_hand) > 21:
            self.end_game("Bust! You lost.")
            self.losses += 1
            self.update_score()

    def deal_card_to_dealer(self, face_up=False):
        card_value = deal_card()
        self.dealer_hand.append(card_value)
        self.dealer_label.config(text="Dealer's cards: " + ', '.join(map(str, self.dealer_hand[1:])) if face_up else "Dealer's cards: ??")

    def update_player_cards(self):
        cards_text = ", ".join(map(str, self.player_hand))
        self.player_cards_label.config(text=cards_text)

    def hit(self):
        self.deal_card_to_player()

    def stand(self):
        for card in self.dealer_hand[1:]:
            self.deal_card_to_dealer(face_up=True)

        while calculate_hand_value(self.dealer_hand) < 17:
            self.deal_card_to_dealer(face_up=True)

        self.dealer_label.config(text=f"Dealer's cards: {self.dealer_hand} (total: {calculate_hand_value(self.dealer_hand)})")

        if calculate_hand_value(self.dealer_hand) > 21:
            self.end_game("Dealer busts! You win.")
            self.wins += 1
            self.update_score()
        elif calculate_hand_value(self.dealer_hand) >= calculate_hand_value(self.player_hand):
            self.end_game("Dealer wins.")
            self.losses += 1
            self.update_score()
        else:
            self.end_game("You win!")
            self.wins += 1
            self.update_score()

    def end_game(self, message):
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        self.result_label = tk.Label(self.blackjack_frame, text=message, font=("Arial", 20), bg="#1C0920", fg="white")
        self.result_label.pack(pady=20)

        self.play_again_button = tk.Button(self.blackjack_frame, text="Play Again", command=self.restart_game, font=("Arial", 20), bg="#007BFF", fg="white", activebackground="#0056b3")
        self.play_again_button.pack(pady=10)

    def restart_game(self):
        self.blackjack_frame.destroy()
        self.__init__()

        # Reset the score to zero
        self.wins = 0
        self.losses = 0
        self.draws = 0

        # Enable the play button again
        self.play_button.config(state=tk.NORMAL)

    def update_score(self):
        score_text = f"Wins: {self.wins} | Losses: {self.losses} | Draws: {self.draws}"
        self.score_label.config(text=score_text)

if __name__ == "__main__":
    app = BlackjackGUI()
    app.mainloop()
