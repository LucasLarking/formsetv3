from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from rest_framework import (authentication, generics, mixins, permissions, viewsets)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .forms import (OptionCreateForm, QuestionCreateForm, SurveyCreateForm,
                    VoteFormset, createOptionFormset)
from .models import Answer, Option, Question, Survey
from .serializers import QuestionSerializer, SurveySerializer
from .permissions import isStaffEditorPermission

class home(View):

    def get(self, request):
        # surveyForm = SurveyCreateForm(request.GET or None, prefix='surveyForm')
        surveyForm = SurveyCreateForm(request.GET or None)

        context = {
            'surveyForm': surveyForm,
            'surveys': Survey.objects.all()
        }
        return render(request, 'base/home.html', context)

    def post(self, request):
        surveyForm = SurveyCreateForm(request.POST, prefix='surveyForm')

        if surveyForm.is_valid():
            surveyObj = Survey.objects.create(
                survey=surveyForm.cleaned_data.get('survey')
            )

            return redirect(f"surveydetail/{surveyObj.id}")
        context = {
            'surveyForm': SurveyCreateForm(request.GET or None, prefix='surveyForm'),
            'surveys': Survey.objects.all()
        }
        return render(request, 'base/home.html', context)


class surveyDetail(View):

    def get(self, request, pk):
        surveyObj = Survey.objects.get(id=pk)
        addQForm = QuestionCreateForm(request.GET or None, prefix='addQForm')
        addOFormset = createOptionFormset(
            request.GET or None, prefix='addOFormset')

        context = {
            'survey': surveyObj,
            'addQForm': addQForm,
            'addOFormset': addOFormset,
        }
        return render(request, 'base/surveydetail.html', context)

    def post(self, request, pk):
        surveyObj = Survey.objects.get(id=pk)

        addQForm = QuestionCreateForm(request.POST, prefix='addQForm')
        addOFormset = createOptionFormset(request.POST, prefix='addOFormset')
        if addQForm.is_valid():
            #  and addOFormset.is_valid()
            type = addQForm.cleaned_data.get('type')
            if type == 'm' or type == 's':
                if addOFormset.is_valid():

                    print('form', addQForm.cleaned_data)
                    print('formset', addOFormset.cleaned_data)
                    questionObj = Question.objects.create(
                        survey=surveyObj,
                        question=addQForm.cleaned_data.get('question'),
                        type=addQForm.cleaned_data.get('type'),
                    )
                    for option in addOFormset:
                        Option.objects.create(
                            survey=surveyObj,
                            question=questionObj,
                            option=option.cleaned_data.get('option'),
                        )
            elif type == 'i' or type == 'm':
                questionObj = Question.objects.create(
                    survey=surveyObj,
                    question=addQForm.cleaned_data.get('question'),
                    type=addQForm.cleaned_data.get('type'),
                )
        else:
            print(addQForm.errors.as_data)
            print(addOFormset.errors)
        context = {
            'survey': surveyObj,
            'addQForm': addQForm,
            'addOFormset': addOFormset,
        }

        return render(request, 'base/surveydetail.html', context)


class SurveyOption(View):

    def get(self, request, pk):
        questionObj = Question.objects.get(id=pk)

        if questionObj.type == 'm' or questionObj.type == 's':
            optionFormset = createOptionFormset(
                request.GET or None, prefix='optionFormset')

            context = {
                'question': questionObj,
                'optionFormset': optionFormset
            }
        else:
            context = {
                'question': questionObj,
            }

        return render(request, 'base/surveyoption.html', context)

    def post(self, request, pk):
        questionObj = Question.objects.get(id=pk)
        optionCreateForm = OptionCreateForm(request.POST)

        if optionCreateForm.is_valid():

            Option.objects.create(
                option=optionCreateForm.cleaned_data.get('option'),
                survey=questionObj.survey,
                question=questionObj,
            )
        return redirect('home')


class SurveyTake(View):

    def get(self, request, pk):
        surveyObj = Survey.objects.get(id=pk)

        questions = list(surveyObj.question_set.all())

        voteFormset = VoteFormset(form_kwargs={'questions': questions})

        voteFormset.min_num = surveyObj.question_set.all().count()

        context = {
            'survey': surveyObj,
            'voteFormset': voteFormset
        }

        return render(request, 'base/surveytake.html', context)

    def post(self, request, pk):
        # print(request.POST)
        surveyObj = Survey.objects.get(id=pk)
        questions = list(surveyObj.question_set.all())

        voteFormset = VoteFormset(request.POST, form_kwargs={
                                  'questions': questions})
        voteFormset.min_num = surveyObj.question_set.all().count()
        voteFormset.validate_min = True

        if voteFormset.is_valid():
            print('################################')

            count = 0
            for form in voteFormset:
                print(form.cleaned_data)
                if form.cleaned_data.get('mail'):
                    Answer.objects.create(
                        survey=surveyObj,
                        question=questions[count],
                        answer=form.cleaned_data.get('mail')
                    )
                    print('mail question')
                elif form.cleaned_data.get('multiple_choice'):
                    print(form.cleaned_data.get('multiple_choice'))
                    for choice in form.cleaned_data.get('multiple_choice'):

                        optionObj = Option.objects.get(id=choice.id)
                        optionObj.votes = optionObj.votes + 1
                        optionObj.save()
                        print('mail question')

                elif form.cleaned_data.get('integer'):

                    Answer.objects.create(
                        survey=surveyObj,
                        question=questions[count],
                        answer=form.cleaned_data.get('integer')
                    )

                count += 1
        else:
            print('aaaaa not valid')
            print(voteFormset.errors)

            print((voteFormset.non_form_errors()))
        print((voteFormset.non_form_errors()))
        print(voteFormset.errors)

        context = {
            'survey': surveyObj,
            'voteFormset': voteFormset
        }

        return render(request, 'base/surveytake.html', context)


class SurveyData(View):

    def get(self, request, pk):
        surveyObj = Survey.objects.get(id=pk)
        context = {
            'survey': surveyObj,
        }

        return render(request, 'base/surveydata.html', context)


class questionAPI(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None, pk=None):
        # print(pk)
        instance = Survey.objects.get(id=pk)

        data = SurveySerializer(instance, many=False).data
        return Response(data)

    def post(self, request, format=None, pk=None):
        print(request.data)
        surveyObj = Survey.objects.get(id=pk)
        addQForm = QuestionCreateForm(request.POST, prefix='addQForm')
        addOFormset = createOptionFormset(request.POST, prefix='addOFormset')

        if addQForm.is_valid():

            type = addQForm.cleaned_data.get('type')
            if type == 'm' or type == 's':
                optionList = []
                if addOFormset.is_valid():

                    print('form', addQForm.cleaned_data)
                    print('formset', addOFormset.cleaned_data)
                    questionObj = Question.objects.create(
                        survey=surveyObj,
                        question=addQForm.cleaned_data.get('question'),
                        type=addQForm.cleaned_data.get('type'),
                    )
                    for option in addOFormset:
                        Option.objects.create(
                            survey=surveyObj,
                            question=questionObj,
                            option=option.cleaned_data.get('option'),
                        )
                    data = {
                        'question': questionObj.question,
                        'id': questionObj.id,
                        'type': questionObj.type,

                    }
                elif type == 'i' or type == 'm':
                    questionObj = Question.objects.create(
                        survey=surveyObj,
                        question=addQForm.cleaned_data.get('question'),
                        type=addQForm.cleaned_data.get('type'),
                    )
                    data = {
                        'question': questionObj.question,
                        'id': questionObj.id,
                        'type': questionObj.type,
                    }

                questions = Question.objects.get(id=questionObj.id)
                serializer = QuestionSerializer(questions, many=False)

                return Response(serializer.data)
        else:
            print(addQForm.errors.as_data)
            print(addOFormset.errors)

        # return Response(data)


class surveyAPI(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None, pk=None):
        # print(pk)
        instance = Survey.objects.get(id=pk)

        data = SurveySerializer(instance, many=False).data
        return Response(data)

    def post(self, request, format=None, pk=None):
        print(request.data)

        serializer = SurveySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # instance = serializer.save()
            # print(instance)

            print(serializer.data)
            # print('DATA', data)

            return Response(serializer.data)
        else:
            print(serializer.errors)
            print('not valid')
            return Response({'invalid': 'Not good data'}, status=400)


class QuestionViewSet(viewsets.ModelViewSet):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = []


class SurveyDetailAPIView(generics.RetrieveAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    # lookup_field = 'pk'
    # product.objects.get(pk=11)


class SurveyListCreateAPIView(generics.ListCreateAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    authentication_classes = [
        authentication.SessionAuthentication,
        authentication.TokenAuthentication,
        ]
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    permission_classes = [permissions.IsAdminUser, isStaffEditorPermission]

    def perform_create(self, serializer):
        print(serializer.validated_data)
        survey = serializer.validated_data.get('survey')
        serializer.save(survey=survey)

# class SurveyCreateAPIView(generics.CreateAPIView):
#     queryset = Survey.objects.all()
#     serializer_class = SurveySerializer

#     def perform_create(self, serializer):
#         print(serializer.validated_data)
#         survey = serializer.validated_data.get('survey')
#         serializer.save(survey=survey)


class SurveyListAPIView(generics.ListAPIView):
    # Dont use
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer


class SurveyUpdateAPIView(generics.UpdateAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    lookup_field = 'pk'
    # product.objects.get(pk=11)

    def perform_update(self, serializer):
        instance = serializer.save()


class SurveyDeleteAPIView(generics.DestroyAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    lookup_field = 'pk'
    # product.objects.get(pk=11)

    def perform_destroy(self, instance):
        #  instance
        super().perform_destroy(instance)


@api_view(['GET', 'POST'])
def survey_alt_view(request, pk=None, *args, **kwargs):
    method = request.method

    if method == 'GET':
        if pk is not None:
            # Detail view
            obj = get_object_or_404(Survey, id=pk)
            data = SurveySerializer(obj, many=False).data
            return Response(data)
        else:
            # list view
            queryset = Survey.objects.all()
            data = SurveySerializer(queryset, many=True).data
            return Response(data)

    if method == 'POST':
        serializer = SurveySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            print(serializer.validated_data)
            survey = serializer.validated_data.get('survey')
            serializer.save(survey=survey)
            return Response(serializer.data)
        return Response({'invalid': 'error'})


class SurveyMixinView(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        mixins.CreateModelMixin,
        generics.GenericAPIView
         ):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        print(args, kwargs)
        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


#  MOSH
@api_view()
def mosh_survey_detail(request, pk):
    survey = get_object_or_404(Survey, pk=pk)
    serializer = SurveySerializer(survey)
    return Response(serializer.data)

@api_view()
def mosh_question_detail(request, id):
    question = get_object_or_404(Question, pk=id)
    serializer = QuestionSerializer(question)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def mosh_questions(request):
    if request.method == 'GET':
        questions = Question.objects.select_related('survey').all()
        serializer = QuestionSerializer(questions, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = QuestionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response('ok')

