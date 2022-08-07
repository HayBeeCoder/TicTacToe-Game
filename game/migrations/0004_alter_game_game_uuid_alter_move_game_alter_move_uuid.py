# Generated by Django 4.0.6 on 2022-08-03 19:08

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_alter_game_game_uuid_alter_move_game_alter_move_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='game_uuid',
            field=models.UUIDField(default=uuid.UUID('3cbf544a-69ff-4589-b59d-46b05efe0834'), editable=False),
        ),
        migrations.AlterField(
            model_name='move',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='moves', to='game.game'),
        ),
        migrations.AlterField(
            model_name='move',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('b3f80a31-79c9-48c4-a17d-f30acfd079be'), editable=False),
        ),
    ]