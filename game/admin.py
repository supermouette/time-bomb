from django.contrib import admin

from .models import Game, Player, Card, Sky, ScrapedData


admin.site.register(Game)
admin.site.register(Player)
admin.site.register(Card)
admin.site.register(Sky)
admin.site.register(ScrapedData)