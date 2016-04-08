# -*- coding:UTF-8 -*-
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from pipeline.models import Frontpage, Pipeline
from pipeline.forms import PipelineForm
from django.db.models import Count, Max
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from pipeline.models import Frontpage, Pipeline
from django.core.urlresolvers import reverse


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
    else:
        form = PipelineForm()
    return render(request, 'pipeline/data_input.html', {'form': form})


@login_required
def project_status(request):
    # pipeline_list = Pipeline.objects.all()

    pipeline_list = Pipeline.objects.all().filter(active=True).order_by('-created_at')
    # pipeline_temp_list = Pipeline.objects.raw(
    # 'select project_code_text, project_name, project_leader, start_date, end_date, project_staffing, project_status, created_at from pipeline A (select project_code_text, max(created_at) as created_at from pipeline group by project_code_text) B on A.project_code_text = B.project_code_text and A.created_at = B.created_at;')

    progress_list, progress_team_list = make_pipeline_list(pipeline_list, "In-Progress")
    cooking_list, cooking_team_list = make_pipeline_list(pipeline_list, "Cooking")

    # 팀별 주관 In-Progress 프로젝트 개수 계산중
    context = {'pipeline_list': pipeline_list, 'progress_list': progress_list, 'progress_team_list': progress_team_list,
               'cooking_list': progress_list, 'cooking_team_list': progress_team_list}

    return render(request, 'pipeline/project_status.html', context)


def make_pipeline_list(pipeline_list, status):
    # 신규 프로젝트 정보가 입력되었을 경우에도 최신 업데이트 사항만을 반영하여 개인별 프로젝트 참여 현황 계산
    personal_list = Pipeline.objects.all().filter(project_status=status, active=True).values('project_leader',
                                                                                             'project_team',
                                                                                             'project_code_text').annotate(
        max_created=Max('created_at')).values('project_leader', 'project_team').annotate(total=Count('project_leader'))
    # progress_list = Pipeline.objects.all().filter(project_status="In-Progress").values('project_leader', 'project_team').annotate(
    #     max_created=Max('created_at'), total=Count('project_leader')).order_by()
    # 팀별 프로젝트 주관 횟수
    # return redirect('blog.views.post_detail', pk=post.pk)
    team_list = Pipeline.objects.all().filter(project_status=status, active=True).values('project_team',
                                                                                         'project_status').annotate(
        total=Count('project_team')).order_by()
    temp_list = []
    staffcount = {}
    inprogress_count = {}

    # 인원별 프로젝트 참여 횟수 계산
    for pipeline in pipeline_list:
        for staff in pipeline.project_staffing.split(','):
            staff = staff.strip()
            if staff not in staffcount:
                staffcount[staff] = 1
            else:
                staffcount[staff] += 1

    exist = False
    for staff in staffcount:
        for participation in personal_list:
            exist = False
            if staff in participation['project_leader']:
                exist = True
                participation['total'] += staffcount[staff]

        if exist is False:
            temp_list.append({'project_leader': staff, 'total': staffcount[staff]})

    result = list(personal_list) + temp_list
    return result, team_list


@login_required
def detail(request, pipeline_id):
    pipeline = get_object_or_404(Pipeline, pk=pipeline_id)
    return render(request, 'pipeline/detail.html', {'pipeline': pipeline})


# def index(request):
#     latest_frontpage_list = Frontpage.objects.all()
#     context = {'latest_frontpage_list': latest_frontpage_list}
#     return render(request, 'pipeline/index.html', context)
#
#
# @login_required
# def data_input(request):
#     if request.method == "POST":
#         form = PipelineForm(request.POST)
#         if form.is_valid():
#             form.save()
#     else:
#         form = PipelineForm()
#     return render(request, 'pipeline/data_input.html', {'form': form})
#
#
@login_required
def data_modify(request, pipeline_id):
    #
    pipeline = get_object_or_404(Pipeline, pk=pipeline_id)

    # 수정하지 않고
    form = PipelineForm(instance=pipeline)
    # return render_to_response('pipeline/data_modify.html', {'pipeline': pipeline})
    # return HttpResponseRedirect(reverse('pipeline:pipeline', args=(pipeline.id)))

    return render(request, 'pipeline/data_modify.html', {'pipeline': form, 'pipeline_id': pipeline_id})

    # project = Pipeline.objects. 링크 누른 해당 플젝의 코드를 가지고 최신날짜 플젝정보를 가져온다.


@login_required
def data_modify_save(request, project_code_text):
    # 수정 후 Save 를 하게 되면 내부 로직을 타게 됨. DB에 새로 저장해야 하기 때문임
    # 수정해도 엎어씌우는 것이 아니라 새로 ID를 따서 신규 데이터가 생성되게 됨
    # 동일한 프로젝트 코드에 대해 여러개의 데이터가 형성되는 것이기에 추후 이 부분을 고려하여 데이터 처리 로직 필요
    if request.method == "POST":

        # 기존 Active=True인 프로젝트 이력은 Active=False로 업데이트
        Pipeline.objects.all().filter(project_code_text=project_code_text).update(active=False)

        form = PipelineForm(request.POST)
        # Debug Code
        # print form.errors

        if form.is_valid():
            pipeline = form.save(commit=False)

            pipeline.project_code_text = request.POST['project_code_text']
            pipeline.project_name = request.POST['project_name']
            pipeline.start_date = request.POST['start_date']
            pipeline.end_date = request.POST['end_date']
            pipeline.project_leader = request.POST['project_leader']
            pipeline.project_staffing = request.POST['project_staffing']
            pipeline.status = request.POST['project_status']
            pipeline.team = request.POST['project_team']
            # pipeline.created_at = request.POST['created_at']
            # pipeline.active = request.POST['active']

            pipeline.save()

    # return render(request, 'pipeline/data_modify.html', {'pipeline': form})
    return project_status(request)

# @login_required
# def project_status(request):
#     temp_list_cooking = []
#     staffcount_cooking = {}
#     pipeline_list_cooking = []
#
#     pipeline_list = Pipeline.objects.all()
#     v
#
#     # 이걸 만들고 싶어요.
#     # select
#     #   project_code_text
#     #   , created_at
#     # from pipeline
#     # group by project_code_text
#
#     # 근데 latest_pipeline 아래처럼 나와요.
#     # select
#     #   project_code_text
#     #   , created_at
#     # from pipeline
#     # group by project_code_text, created_at
#
#
#     # latest_pipeline = Pipeline.objects.raw('select project_code_text, project_name, project_leader, start_date, end_date, project_staffing, project_status, created_at from pipeline A (select project_code_text, max(created_at) as created_at from pipeline group by project_code_text) B on A.project_code_text = B.project_code_text and A.created_at = B.created_at;')
#
#     # pipeline_list = Pipeline.objects.all().values('project_code_text', 'project_name', 'start_date', 'end_date', 'project_leader', 'project_staffing', 'project_status', 'project_team', 'created_at')\
#     #                     .annotate(code_cnt=Count('project_code_text'), name_cnt=Count('project_name')).order_by('created_at')[:1]
#
#     # 신규 프로젝트 정보가 입력되었을 경우에도 최신 업데이트 사항만을 반영하여 개인별 프로젝트 참여 현황 계산
#
#     # if project_status is "In-Progress":
#     participation_list = Pipeline.objects.all().filter(project_status="In-Progress")\
#         .values('project_leader', 'project_team', 'project_code_text').annotate(total=Count('project_leader'))
#
#     team_list = Pipeline.objects.all().filter(project_status="In-Progress").values('project_team',
#                                                                                'project_status').annotate(
#         total=Count('project_team')).order_by()
#
#
#     for pipeline in pipeline_list:
#         for staff in pipeline.project_staffing.split(','):
#             if staff not in staffcount:
#                 staffcount[staff] = 1
#             else:
#                 staffcount[staff] += 1
#
#     for staff in staffcount:
#         for participation in participation_list:
#             exists = False
#             if staff in participation['project_leader']:
#                 exists = True
#                 participation['total'] += 1
#
#         if exists is False:
#             temp_list.append({'project_leader': staff, 'total': staffcount[staff]})
#
#     result = list(participation_list) + temp_list
#
#
#     # else if project_status is "Cooking":
#     #     participation_list_cooking = Pipeline.objects.all().filter(project_status="Cooking")\
#     #         .values('project_leader', 'project_team', 'project_code_text').annotate(total=Count('project_leader'))
#     #
#     #     team_list_cooking = Pipeline.objects.all().filter(project_status="Cooking").values('project_team',
#     #                                                                                'project_status').annotate(
#     #         total=Count('project_team')).order_by()
#     #
#     #     for pipeline in pipeline_list_cooking:
#     #         for staff in pipeline.project_staffing.split(','):
#     #             if staff not in staffcount_cooking:
#     #                 staffcount_cooking[staff] = 1
#     #             else:
#     #                 staffcount_cooking[staff] += 1
#     #
#     #         for staff in staffcount_cooking:
#     #             for participation in participation_list_cooking:
#     #                 exists = False
#     #                 if staff in participation['project_leader']:
#     #                     exists = True
#     #                     participation['total'] += 1
#     #
#     #             if exists is False:
#     #                 temp_list.append({'project_leader': staff, 'total': staffcount_cooking[staff]})
#     #
#     # result = list(participation_list_cooking) + temp_list_cooking
#     #
#     # # participation_list = Pipeline.objects.all().filter(project_status="In-Progress").values('project_leader', 'project_team').annotate(
#     # #     max_created=Max('created_at'), total=Count('project_leader')).order_by()
#     # # 팀별 프로젝트 주관 횟수
#     # # return redirect('blog.views.post_detail', pk=post.pk)
#
#
#     temp_list = []
#     staffcount = {}
#     inprogress_count = {}
#
#     # 인원별 프로젝트 참여 횟수 계산 (In-Progress)
#
#
#     # 팀별 주관 In-Progress 프로젝트 개수 계산중
#
#     context = {'pipeline_list': pipeline_list, 'participation_list': result, 'team_list': team_list}
#
#     return render(request, 'pipeline/project_status.html', context)
#
#
# @login_required
# def detail(request, pipeline_id):
#     pipeline = get_object_or_404(Pipeline, pk=pipeline_id)
#     return render(request, 'pipeline/detail.html', {'pipeline': pipeline})
#
#     # def my_view(request):
#     # 	username = request.POST['username']
#     # 	password = request.POST['password']
#     # 	user = authenticate(username=username, password=password)
#     # 	if user is not None:
#     # 		if user.is_active:
#     # 			login(request, user)
#     # 			# Redirect to a success page.
#     # 		else:
#     # 			# Return a 'disabled account' error message
#     # 	else:
#     # 		# Return an 'invalid login' error message.
#     # def post_new(request):
#     #     if request.method == "POST":
#     #         form = PostForm(request.POST)
#     #         if form.is_valid():
#     #             post = form.save(commit=False)
#     #             post.author = request.user
#     #             post.published_date = timezone.now()
#     #             post.save()
#     #             return redirect('blog.views.post_detail', pk=post.pk)
#     #     else:
#     #         form = PostForm()
#     #     return render(request, 'blog/post_edit.html', {'form': form})
