# Generated by Django 4.2.5 on 2023-10-21 13:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("word", "0002_remove_document_created_at_remove_document_title_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="document",
            name="title",
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
