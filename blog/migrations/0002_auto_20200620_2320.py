# Generated by Django 2.2.13 on 2020-06-20 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='currentStory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='current_story', to='blog.Story'),
        ),
        migrations.AlterField(
            model_name='story',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent_story', to='blog.Story'),
        ),
    ]
