from django import forms
from django.forms import BaseFormSet
from django.forms import formset_factory
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError
from .models import (
    Survey,
    Question,
    Option,
)


class SurveyCreateForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ('survey', )
        blank = True
        null = True
        required = False

    survey = forms.CharField(
        required=False,
        label="Ny Undersökning",
    )

    def clean(self):
        cleaned_data = super(SurveyCreateForm, self).clean()
        if self.cleaned_data.get('survey'):
            if len(self.cleaned_data.get('survey')) < 5:
                self.add_error('survey', 'For kort undersöking')
        else:
            self.add_error('survey', 'Ange undersökning')
        return cleaned_data


class QuestionCreateForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question', 'type')
        blank = True
        null = True
        required = False

    question = forms.CharField(
        required=False,
        label="Ny fraga",
    )

    def clean(self):

        cleaned_data = super(QuestionCreateForm, self).clean()
        if self.cleaned_data.get('question'):

            if len(self.cleaned_data.get('question')) < 5:
                self.add_error('question', 'For kort fraga')

        else:
            self.add_error('question', 'Ange Fraga')
        return cleaned_data


class OptionCreateForm(forms.Form):
    email = forms.EmailField(

        required=False,
        max_length=100,
        label='Email Field',
    )

    option = forms.CharField(
        required=False,
        label="Nytt Allternativ",
    )

    integer = forms.IntegerField(
        required=False,
        label="Nytt Allternativ nummer",
    )

    def __init__(self, *args, **kwargs):
        self.type = kwargs.pop('type', None)
        super().__init__(*args, **kwargs)
        print('aaa', self.type)

        if self.type == 'm':
            self.fields.pop('email')
            self.fields.pop('integer')
        elif self.type == 'e':
            self.fields.pop('option')
            self.fields.pop('integer')
        elif self.type == 'i':
            self.fields.pop('option')
            self.fields.pop('email')


class BaseVoteFormset(BaseFormSet):

    # def add_fields(self, form, index):
    #     super().add_fields(form, index)
    #     form.fields["my_field"] = forms.CharField()

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        q = kwargs['questions'][index]
        # print('q', q, q.id)

        return {'question': q}


class VoteForm(forms.Form):

    def __init__(self, *args, question, **kwargs):
        # print('question', question, question.id, question.type)
        self.type = kwargs.pop('type', None)
        super().__init__(*args, **kwargs)
        self.empty_permitted = False
        # print('aaa', self.type)

        if question.type == 'm':

            self.fields["multiple_choice"] = forms.ModelMultipleChoiceField(
                widget=forms.CheckboxSelectMultiple(),
                queryset=question.option_set.all(),
                label=f"{question.question}: multiple choice ",
                required=False,

            )
        elif question.type == 'e':
            self.fields["mail"] = forms.EmailField(
                required=False,
                max_length=100,
                label=f"{question.question}: email ",
                widget=forms.TextInput(attrs={'formnovalidate': 'true'}),
            )
        elif question.type == 'i':
            self.fields["integer"] = forms.IntegerField(
                required=False,
                label=f"{question.question}: integer",
                widget=forms.TextInput(attrs={'formnovalidate': 'true'}),
            )


class MyVoteForm(VoteForm):
    def __init__(self, *args, question, **kwargs):
        # print('question', question)
        # self.survey = survey
        # print(self.survey)
        super().__init__(*args, question, **kwargs)


VoteFormset = formset_factory(
    VoteForm,
    formset=BaseVoteFormset,
    extra=0,
    min_num=0,
    validate_min=True,
)


class CreateOptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ('option', )
        blank = True
        null = True
        required = False

    option = forms.CharField(
        required=False,
        label="Nytt Alternativ",

    )

    def clean(self):

        cleaned_data = super(CreateOptionForm, self).clean()
        if self.cleaned_data.get('option'):

            if len(self.cleaned_data.get('option')) < 5:
                self.add_error('option', 'For kort allternativ')

            elif len(self.cleaned_data.get('option')) > 200:
                self.add_error('option', 'For langt allternativ')

        else:
            self.add_error('option', 'Ange minst ett allternativ')

        return cleaned_data


createOptionFormset = forms.formset_factory(
    CreateOptionForm,
    extra=0,
    min_num=1,
    validate_min=True,
)
