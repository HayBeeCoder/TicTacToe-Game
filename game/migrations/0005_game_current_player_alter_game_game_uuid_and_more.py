# Generated by Django 4.0.6 on 2022-08-03 20:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('game', '0004_alter_game_game_uuid_alter_move_game_alter_move_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='current_player',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='current_player', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='game',
            name='game_uuid',
            field=models.UUIDField(default=uuid.UUID('cb7ef775-a1bd-468d-a25d-7b04a39c1a10'), editable=False),
        ),
        migrations.AlterField(
            model_name='move',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('cf93652d-290f-4284-9b8a-598a793c5236'), editable=False),
        ),
    ]
