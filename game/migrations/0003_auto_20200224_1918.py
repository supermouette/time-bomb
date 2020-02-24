# Generated by Django 3.0.2 on 2020-02-24 18:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_sky_year'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team', models.CharField(blank=True, choices=[('b', 'Blue'), ('r', 'Red')], max_length=1, null=True)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='card',
            name='gamer',
        ),
        migrations.AddField(
            model_name='card',
            name='discovered',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='game',
            name='count_discovered',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='game',
            name='status',
            field=models.CharField(choices=[('u', 'Uninitialized'), ('i', 'In progress'), ('s', 'Stopped'), ('r', 'Red win'), ('b', 'Blue win')], default='u', max_length=1),
        ),
        migrations.AlterField(
            model_name='card',
            name='value',
            field=models.CharField(choices=[('n', 'Nothing'), ('w', 'Wire'), ('b', 'Bomb')], default='n', max_length=1),
        ),
        migrations.DeleteModel(
            name='Gamer',
        ),
        migrations.AddField(
            model_name='player',
            name='game',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='game.Game'),
        ),
        migrations.AddField(
            model_name='card',
            name='player',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='game.Player'),
        ),
        migrations.AddField(
            model_name='game',
            name='next_player',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='game.Player'),
        ),
    ]
