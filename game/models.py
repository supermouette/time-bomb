from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):

    UNINITIALIZED = "u"
    IN_PROGRESS = "i"
    STOPPED = "s"
    RED_WIN = "r"
    BLUE_WIN = "b"

    STATUS_CHOICES = ((UNINITIALIZED, "Uninitialized"),
                      (IN_PROGRESS, "In progress"),
                      (STOPPED, "Stopped"),
                      (RED_WIN, "Red win"),
                      (BLUE_WIN, "Blue win"))

    turn = models.IntegerField(default=0)
    count_discovered = models.IntegerField(default=0)
    next_player = models.ForeignKey('Player', on_delete=models.SET_NULL, default=None, blank=True, null=True,
                                    related_name='+')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=UNINITIALIZED)
    name = models.CharField(max_length=30)

    def get_players(self):
        return Player.objects.filter(game=self)

    def _create_deck(self):
        if Card.objects.filter(game=self).count() != 0:
            raise AssertionError("Game already have cards")
        nb_players = len(self.get_players())
        # bomb
        Card(value=Card.BOMB, game=self, player=None).save()
        # wires
        for i in range(nb_players):
            Card(value=Card.WIRE, game=self, player=None).save()
        # nothing
        for i in range(nb_players*4-1):
            Card(value=Card.NOTHING, game=self, player=None).save()

    def next_turn(self):
        from random import shuffle
        if self.count_discovered != len(self.get_players()) and self.turn != 0:
            raise AssertionError("Next turn is forbidden right now")
        if self.turn > 4:
            raise AssertionError("Number of turn can not exceed 4")
        count_discovered = 0
        self.save(update_fields='count_discovered')
        cards = list(Card.objects.filter(game=self).filter(discovered=False))
        shuffle(cards)
        players = self.get_players()
        for i in range(len(cards)):
            cards[i].player = players[i % len(players)]
            cards[i].save(update_fields='player')
        self.turn += 1

    def init_game(self):
        from random import shuffle

        if self.turn != 0 or self.status != self.UNINITIALIZEDs:
            raise AssertionError("Game already initialized")

        # init player team, set first player
        players = list(self.get_players())
        nb_players = len(players)

        if nb_players in [4, 5]:
            nb_blue = 3
            nb_red = 2
        elif nb_players == 6:
            nb_blue = 4
            nb_red = 2
        elif nb_players in [7, 8]:
            nb_blue = 5
            nb_red = 3
        else:
            raise AssertionError("Number of player should be between 4 and 8")
        colors = [Player.BLUE]*nb_blue + [Player.RED]*nb_red
        shuffle(colors)
        for i in range(nb_players):
            players[i].team = colors[i]
            players[i].save(update_fields='team')
        self._create_deck()
        shuffle(players)
        self.next_player = players[0]
        self.status = self.IN_PROGRESS
        self.next_turn()
        self.save()

    def check_victory(self):
        discovered = Card.objects.filter(game=self).filter(discovered=True)
        bomb = discovered.filter(value=Card.BOMB)
        wires = discovered.filter(value=Card.WIRE)
        if wires.count() == self.get_players().count():
            self.status = self.BLUE_WIN
        elif bomb.count() != 0 or discovered.count() == self.get_players().count()*5:
            self.status = self.RED_WIN
        else:
            return self.status
        self.save(update_fields="status")
        return self.status

    def __str__(self):
        return self.name


class Player(models.Model):

    BLUE = "b"
    RED = "r"
    TEAM_CHOICES = ((BLUE, "Blue"), (RED, "Red"))

    team = models.CharField(max_length=1, choices=TEAM_CHOICES, null=True, blank=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def discover_card(self, card):
        if self.game.next_player != self:
            raise AssertionError("This is not " + str(self) + " turn.")
        if card.player == self:
            raise AssertionError("Impossible to discover own card")
        if card.discovered:
            raise AssertionError("Card already discovered")

        card.discovered = True
        card.save(update_fields='discovered')
        self.game.count_discovered += 1
        self.game.next_player = card.player
        self.game.save()
        return card.value


class Card(models.Model):

    NOTHING = "n"
    WIRE = "w"
    BOMB = "b"
    VALUE_CHOICES = ((NOTHING, "Nothing"), (WIRE, "Wire"), (BOMB, "Bomb"))

    value = models.CharField(max_length=1, choices=VALUE_CHOICES, default=NOTHING)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, blank=True)
    discovered = models.BooleanField(default=False)


class Sky(models.Model):

    color = models.IntegerField()
    day = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()

    def __str__(self):
        return str(self.day) + '/' + str(self.month) + " ("+str(self.color) + ")"
