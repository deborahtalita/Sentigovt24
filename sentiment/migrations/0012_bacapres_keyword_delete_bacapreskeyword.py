# Generated by Django 4.2 on 2023-05-03 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sentiment', '0011_rename_keyword_bacapreskeyword'),
    ]

    operations = [
        migrations.AddField(
            model_name='bacapres',
            name='keyword',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.DeleteModel(
            name='BacapresKeyword',
        ),
    ]