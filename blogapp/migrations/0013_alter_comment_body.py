# Generated by Django 4.0.5 on 2022-07-21 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0012_alter_replycomment_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='body',
            field=models.TextField(blank=True, default=True, null=True),
        ),
    ]
