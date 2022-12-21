from django.db import models


class Survey(models.Model):
    survey = models.CharField(max_length=200)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.survey


    def get_questions(self):
        return self.question_set.all()


class Question(models.Model):
    question = models.CharField(max_length=200)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, null=True)
    question_types = (
        ('m', 'multiple_choice'),
        ('s', 'single_choice'),
        ('i', 'integer'),
        ('e', 'email'),
    )
    type = models.CharField(max_length=1, choices=question_types, default='s')

    def __str__(self):
        return self.question

    def get_options(self):
        return self.option_set.all()

    def get_answers(self):
        return self.answer_set.all()


class Option(models.Model):
    option = models.CharField(max_length=200, blank=True, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return str(self.option)


class Answer(models.Model):
    answer = models.CharField(max_length=200, blank=True, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.answer)
