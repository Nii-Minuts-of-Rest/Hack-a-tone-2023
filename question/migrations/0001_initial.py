# Generated by Django 4.2 on 2023-04-06 12:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('question_text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('creation_date', models.DateTimeField()),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.question')),
            ],
        ),
        migrations.CreateModel(
            name='TagsGroup',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('report_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.report')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('tag_text', models.TextField()),
                ('popularity', models.PositiveIntegerField()),
                ('tagsGroup_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.tagsgroup')),
            ],
        ),
        migrations.CreateModel(
            name='Sentence',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('sentence_text', models.TextField()),
                ('tagsGroup_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.tagsgroup')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('anwser_text', models.TextField()),
                ('answer_edited', models.TextField()),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.question')),
            ],
        ),
    ]
