# -*- coding:UTF-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from pipeline.models import Frontpage, Pipeline
from pipeline.forms import PipelineForm
from django.db.models import Count
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


def index(request):
    latest_frontpage_list = Frontpage.objects.all()
    context = {'latest_frontpage_list': latest_frontpage_list}
    return render(request, 'pipeline/index.html', context)

@login_required
def data_input(request):
    if request.method == "POST":
        form = PipelineForm(request.POST)
        if form.is_valid():
            form.save()
        # return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PipelineForm()
    return render(request, 'pipeline/data_input.html', {'form': form})

def data_modify(request):
    if request.method == "POST":
        # project = Pipeline.objects. 링크 누른 해당 플젝의 코드를 가지고 최신날짜 플젝정보를 가져온다.



    else:
        form = PipelineForm()

    return render(request, 'pipeline/data_modify.html', {'form': form})

@login_required
def project_status(request):
    pipeline_list = Pipeline.objects.all()
    participation_list = Pipeline.objects.all().values('project_leader', 'project_team').annotate(
        total=Count('project_leader')).order_by()
    # 팀별 프로젝트 주관 횟수
    team_list = Pipeline.objects.all().filter(project_status="In-Progress").values('project_team',
                                                                                   'project_status').annotate(
        total=Count('project_team')).order_by()

    # select * from pipelines group by project_team order by project_team

    temp_list = []
    staffcount = {}
    inprogress_count = {}

    # 인원별 프로젝트 참여 횟수 계산
    for pipeline in pipeline_list:
        for staff in pipeline.project_staffing.split(','):
            if staff not in staffcount:
                staffcount[staff] = 1
            else:
                staffcount[staff] += 1

    for staff in staffcount:
        for participation in participation_list:
            exists = False
            if staff in participation['project_leader']:
                exists = True
                participation['total'] += 1

        if exists is False:
            temp_list.append({'project_leader': staff, 'total': staffcount[staff]})

    result = list(participation_list) + temp_list

    # 팀별 주관 In-Progress 프로젝트 개수 계산중

    context = {'pipeline_list': pipeline_list, 'participation_list': result, 'team_list': team_list}

    return render(request, 'pipeline/project_status.html', context)

@login_required
def detail(request, pipeline_id):
    pipeline = get_object_or_404(Pipeline, pk=pipeline_id)
    return render(request, 'pipeline/detail.html', {'pipeline': pipeline})

    # def my_view(request):
    # 	username = request.POST['username']
    # 	password = request.POST['password']
    # 	user = authenticate(username=username, password=password)
    # 	if user is not None:
    # 		if user.is_active:
    # 			login(request, user)
    # 			# Redirect to a success page.
    # 		else:
    # 			# Return a 'disabled account' error message
    # 	else:
    # 		# Return an 'invalid login' error message.
    # def post_new(request):
    #     if request.method == "POST":
    #         form = PostForm(request.POST)
    #         if form.is_valid():
    #             post = form.save(commit=False)
    #             post.author = request.user
    #             post.published_date = timezone.now()
    #             post.save()
    #             return redirect('blog.views.post_detail', pk=post.pk)
    #     else:
    #         form = PostForm()
    #     return render(request, 'blog/post_edit.html', {'form': form})
