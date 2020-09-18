from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question, Comments


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    # return HttpResponse("You're voting on question %s." % question_id)


class CommentsView(generic.CreateView):
    model = Comments
    template_name = 'polls/comments.html'
    fields = '__all__'
# def comments(request):
#     comment = get_object_or_404(Comments)
#     try:
#         name = comment.get(pk=request.POST['name'])
#         body = comment.get(pk=request.POST['body'])
#         if not name or body:
#             raise ValueError('empty string')
#     except ValueError as e:
#         return render(request, 'polls/comments.html', {
#             'comment': comment,
#             'error_message': "You didn't enter a comment.",
#         })
#     else:
#         c = Comments(comment_name=name, comment_body=body)
#         c.save()
#         return HttpResponseRedirect(reverse('polls:comments_list'))


def comments_list(request):
    comment_list = Comments.objects.all()
    context = {'comment_list': comment_list}
    if request.POST.get('name') is not None:
        name = request.POST.get('name')
        body = request.POST.get('body')
        c = Comments(comment_name=name, comment_body=body)
        c.save()
    return render(request, "polls/comments_list.html", context)


# class CommentsListView(generic.ListView):
#     # model = Comments
#     template_name = 'polls/comments_list.html'
#     # context_object_name = 'comments_list'
#
#     def get_queryset(self):
#         return Comments.objects.exclude(comment_name__isnull=True)


# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     # template = loader.get_template('polls/index.html')
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     return render(request, 'polls/index.html', context)
#     # return HttpResponse(template.render(context, request))
#
#
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     # return render(request, 'polls/detail.html', {'question': question})
#     # return HttpResponse("You're looking at question %s." % question_id)
#
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})
#     # response = "You're looking at the results of question %s."
#     # return HttpResponse(response % question_id)
