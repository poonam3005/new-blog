# Generated by Django 4.0.5 on 2022-07-21 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0014_rename_created_replycomment_replied_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='private',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
