# Generated by Django 5.1.2 on 2024-11-05 16:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("runner", "0002_historicalpattern_source_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalpattern",
            name="author",
            field=models.CharField(blank=True, max_length=50, verbose_name="author"),
        ),
        migrations.AlterField(
            model_name="historicalpattern",
            name="description",
            field=models.CharField(blank=True, max_length=200, verbose_name="description"),
        ),
        migrations.AlterField(
            model_name="historicalpattern",
            name="docker",
            field=models.CharField(max_length=200, verbose_name="docker"),
        ),
        migrations.AlterField(
            model_name="historicalpattern",
            name="name",
            field=models.CharField(max_length=50, verbose_name="name"),
        ),
        migrations.AlterField(
            model_name="historicalpattern",
            name="school",
            field=models.CharField(blank=True, max_length=100, verbose_name="school"),
        ),
        migrations.AlterField(
            model_name="historicalpattern",
            name="source",
            field=models.URLField(blank=True, verbose_name="source"),
        ),
        migrations.AlterField(
            model_name="pattern",
            name="author",
            field=models.CharField(blank=True, max_length=50, verbose_name="author"),
        ),
        migrations.AlterField(
            model_name="pattern",
            name="description",
            field=models.CharField(blank=True, max_length=200, verbose_name="description"),
        ),
        migrations.AlterField(
            model_name="pattern",
            name="docker",
            field=models.CharField(max_length=200, verbose_name="docker"),
        ),
        migrations.AlterField(
            model_name="pattern",
            name="name",
            field=models.CharField(max_length=50, verbose_name="name"),
        ),
        migrations.AlterField(
            model_name="pattern",
            name="school",
            field=models.CharField(blank=True, max_length=100, verbose_name="school"),
        ),
        migrations.AlterField(
            model_name="pattern",
            name="source",
            field=models.URLField(blank=True, verbose_name="source"),
        ),
    ]
