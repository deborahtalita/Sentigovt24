# Generated by Django 4.2 on 2023-05-21 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bacapres', '0001_initial'),
        ('sentiment', '0022_alter_tweet_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(default=None)),
                ('end_date', models.DateTimeField(default=None)),
                ('bacapres', models.ManyToManyField(to='bacapres.bacapres')),
                ('tweet', models.ManyToManyField(to='sentiment.tweet')),
            ],
        ),
        migrations.DeleteModel(
            name='Bacapres',
        ),
    ]