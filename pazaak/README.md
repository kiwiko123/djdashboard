# Pazaak
[Pazaak](https://starwars.fandom.com/wiki/Pazaak/Legends) is a card game from [Star Wars: Knights of the Old Republic](https://en.wikipedia.org/wiki/Star_Wars:_Knights_of_the_Old_Republic), similar to [Blackjack](https://en.wikipedia.org/wiki/Blackjack).

## Rules
The objective of the game is to get the highest score you can, while remaining at or below 20. 
You start with a blank table, and 4 cards in your "hand".

### Actions 
At each turn, you have a few options:

* end the turn
* draw from your hand
* stand

#### End Turn
This means you pick a random card and put it on the table. Now it's the opponent's turn.

Ending your turn with a score over 20 is an automatic loss.

#### Choose From Your Hand
Recall that you started with 4 known cards. At any turn, you can play one of these cards instead of picking a random one.
This is particularly useful if playing one of your hand cards will total your score to 20.
For example, if your score is 16, and your hand consists of \[+2, -3, +4, -1\], then playing +4 gives you a score of 20.

Additionally, it's possible to have your score be _over_ 20. 
And if you have a negative card in your hand that will bump your score back below 20, you've got a chance at redeeming yourself!

#### Stand
Standing means that you're all in. You're satisifed with your score, and you don't think that your opponent will top you.
Once you stand, you can't make any more moves for the rest of the game. It's generally wise to stand when you have a score close to 20.

Getting a score of 20 (e.g., by luckily drawing a random card, or choosing from your hand) will automatically make you stand.

### 20
That's the magic number! And yep, it's possible to be over 20.
For example, your score is 18. You decide to tempt fate, and end your turn. You happen to draw a +4, giving you a score of 22.
Your opponent then makes their move, and the turn comes back to you. Since your score is over 20, ending the turn or standing will both result in a loss.
But, if you have a -2 or _lower_ in your hand, you can bump your score back below 20 and remain in the game.

### Any Catches?
The rules are outlined in the fandom article linked above, but to summarize, here are the ways you can win:
* if both players are standing, the one with the highest score _at or below_ 20 wins.
* if one player ends their turn or stands with a score over 20, they lose, and the other player wins.
* if a player manages to get 9 cards on the table, and their score is still under 20, they automatically win.
* and of course, if both players end with a score of 20 (or stand at the same score), it's a tie!

## Technical Implementation
Alright, alright, you know how to play the game. Now you want to know the nerdy stuff!

### Backend
Implemented entirely in Python. All of the core game logic lives under the top-level `game` package.

The server is implemented using Django.
A bit unconventional, especially for an API! This is explained in more detail in [the comments here](views.py).

Since this is purely an API, we're only utilizing the **view** portion of the Django model, and not the **template** or **model**.

(_For those unfamiliar with Django, there's some different terminology than the traditional MVC pattern. In Django, the model is still the model, but the view is called the **template**, and the controller is called the **view**_).

### Frontend
React JSX. Check out the [setup script](docs/setup.sh) to install the necessary dependencies.