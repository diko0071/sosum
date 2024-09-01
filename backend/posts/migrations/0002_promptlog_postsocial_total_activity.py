# Generated by Django 5.0.2 on 2024-09-01 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromptLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('system_message', models.TextField()),
                ('user_message', models.TextField()),
                ('response', models.TextField()),
                ('cost', models.DecimalField(decimal_places=10, max_digits=10)),
                ('input_tokens', models.PositiveIntegerField(blank=True, null=True)),
                ('output_tokens', models.PositiveIntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='postsocial',
            name='total_activity',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
