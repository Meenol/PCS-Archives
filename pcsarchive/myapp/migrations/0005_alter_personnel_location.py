# Generated by Django 4.2.20 on 2025-04-18 04:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0004_entity_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="personnel",
            name="location",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.SET_NULL, to="myapp.site"
            ),
        ),
    ]
