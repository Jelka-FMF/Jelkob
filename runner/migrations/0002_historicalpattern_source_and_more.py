# Generated by Django 5.1.2 on 2024-10-31 20:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("runner", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalpattern",
            name="source",
            field=models.URLField(blank=True, max_length=255, verbose_name="source"),
        ),
        migrations.AlterField(
            model_name="historicalpattern",
            name="duration",
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name="duration"),
        ),
        migrations.AlterField(
            model_name="pattern",
            name="source",
            field=models.URLField(blank=True, max_length=255, verbose_name="source"),
        ),
    ]
