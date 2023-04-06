from django.db import models
from django.urls import reverse

# Create your models here.

class Question(models.Model):
    question_text = models.TextField()

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this book."""
        return reverse('question/show', args=[str(self.id)])

class Answer(models.Model):
    question_id = models.ForeignKey('Question', on_delete=models.CASCADE, null=False)
    anwser_text = models.TextField()
    answer_edited = models.TextField()

class Report(models.Model):
    question_id = models.ForeignKey('Question', on_delete=models.CASCADE, null=False)
    creation_date = models.DateTimeField()
    data_count = models.PositiveIntegerField()

class TagsGroup(models.Model):
    report_id = models.ForeignKey('Report', on_delete=models.CASCADE, null=False)

class Tag(models.Model):
    tagsGroup_id = models.ForeignKey('TagsGroup', on_delete=models.CASCADE, null=False)
    tag_text = models.TextField()
    popularity = models.FloatField()

class Sentence(models.Model):
    tagsGroup_id = models.ForeignKey('TagsGroup', on_delete=models.CASCADE, null=False)
    sentence_text = models.TextField()
