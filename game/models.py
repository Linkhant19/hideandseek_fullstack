from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# my models
class Profile(models.Model):
    '''
    Profile model - connected to logged in user:
        username
        email
        games_played
        games_won
    '''
    username = models.CharField(max_length=120)
    email = models.EmailField()
    games_played = models.IntegerField(default=0)
    games_won = models.IntegerField(default=0)

    # associate each Profile with a User
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        ''' string representation of profile '''
        return f'{self.username} - {self.email}'

class Card(models.Model):
    '''
    Card model:
        card_name - name of card
        image - image of card
        description - description of card abilities
        card_type - main or ability card
        keywords - keywords associated with card
    '''
    card_name = models.CharField(max_length=100)
    image = models.ImageField()
    description = models.TextField()
    card_type = models.CharField(max_length=13)
    keywords = models.TextField()

    def __str__(self):
        ''' string representation of card '''
        return f'{self.card_name} - {self.card_type}'

class Hider(models.Model):
    '''
    Hider model:
        class_name - name of class
        description - description of class
        image - image of class
    '''
    class_name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField()

    def __str__(self):
        ''' string representation of Hider class '''
        return f'{self.class_name}'

class Seeker(models.Model):
    '''
    Seeker model:
        class_name - name of class
        description - description of class
        image - image of class
    '''
    class_name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField()

    def __str__(self):
        ''' string representation of Seeker class '''
        return f'{self.class_name}'

class AddToDeck(models.Model):
    '''
    AddToDeck model:
        card - card object
        hider_class - player class object
        seeker_class - player class object
    '''
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    # hider_class and seeker_class can be null
    hider_class = models.ForeignKey(Hider, on_delete=models.CASCADE, null=True, blank=True)
    seeker_class = models.ForeignKey(Seeker, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        ''' string representation of add to deck '''
        if self.hider_class and self.seeker_class:
            return f'({self.card}) added to {self.hider_class} and {self.seeker_class}'
        elif self.hider_class:
            return f'({self.card}) added to {self.hider_class}'
        elif self.seeker_class:
            return f'({self.card}) added to {self.seeker_class}'
        else:
            return f'({self.card})'

class Game(models.Model):
    '''
    Game model:
        id - id of game
        player - foriegn key to player profile
        hider_class - foriegn key to Hider class
        seeker_class - foriegn key to Seeker class
        current_turn - integer for turn count
    '''
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    player = models.ForeignKey(Profile, on_delete=models.CASCADE)
    hider_class = models.ForeignKey(Hider, on_delete=models.CASCADE)
    seeker_class = models.ForeignKey(Seeker, on_delete=models.CASCADE)
    current_turn = models.IntegerField(default=0)

    def __str__(self):
        ''' string representation of game '''
        return f'{self.player} as {self.hider_class} against {self.seeker_class}. Turn: {self.current_turn}'



