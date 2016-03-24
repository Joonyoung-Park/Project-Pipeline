from django import forms
from pipeline.models import Pipeline


class PipelineForm(forms.ModelForm):
    class Meta:
        model = Pipeline
        fields = ('project_name', 'start_date', 'end_date', 'project_leader', 'project_staffing', 'project_status',
                  'project_team')
