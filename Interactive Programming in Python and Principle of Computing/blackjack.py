# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []
        
    def add_card(self, card):
        self.cards.append(card)
        
    def get_value(self):
        value = 0
        flag = False
        for card in self.cards:
            value += VALUES[card.get_rank()]
            if card.get_rank() == 'A':
                flag = True
        if flag and value <= 11:
            value +=10
        return value
    
    def draw(self, canvas, pos):
        for i, card in enumerate(self.cards):
            card.draw(canvas, [pos[0]+ 50*i, pos[1]])

# define deck class 
class Deck:
    def __init__(self):
        self.cards = [Card(x,y) for x in SUITS for y in RANKS]
        
    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop(0)



#define event handlers for buttons
def deal():
    global outcome, in_play, score
    if in_play:
        score -=1
    dealer.__init__()
    player.__init__()
    deck.__init__()
    deck.shuffle()
    player.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    in_play = True
    outcome = 'hit or stand?'

def hit():
    global outcome, score, in_play
    if in_play:
        player.add_card(deck.deal_card())
        if player.get_value()>21:
            score -= 1
            in_play = False
            outcome = 'dealer win!'
def stand():
    global outcome, score, in_play
    if in_play:
        while dealer.get_value()<17:
            dealer.add_card(deck.deal_card())
        if dealer.get_value()>21 or dealer.get_value()<player.get_value():
            score +=1
            outcome = 'player win!'
        else:
            score -=1
            outcome = 'dealer win!'
    in_play = False
    
def start():
    global score, dealer, player, deck
    dealer = Hand()
    player = Hand()
    deck = Deck()
    deal()
    score = 0
    
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    for i, card in enumerate(player.cards):
        card.draw(canvas, [120+80*i, 400])
    for i, card in enumerate(dealer.cards):
        if in_play and i == 0:
            canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE,
                              [120+CARD_BACK_CENTER[0], 100+CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
        else:
            card.draw(canvas, [120+80*i, 100])
    canvas.draw_text(outcome, (200,300), 48, 'black')
    if not in_play:
        canvas.draw_text('New deal?', (208,360), 48, 'black')
    canvas.draw_text('player score: '+str(score), (354,580), 36, 'black')
    canvas.draw_text('Black Jack', (325,60), 60, 'black')
    canvas.draw_text('Player', (120,540), 36, 'black')
    canvas.draw_text('Dealer', (120,84), 36, 'black')
    
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Reset Score", start, 200)
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
start()
frame.start()


# remember to review the gradic rubric