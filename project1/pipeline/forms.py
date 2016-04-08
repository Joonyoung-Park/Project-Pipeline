from django import forms
from pipeline.models import Pipeline


class PipelineForm(forms.ModelForm):

    project_code_text = forms.CharField(max_length=200, required=False)

    class Meta:
        model = Pipeline
        fields = ('project_code_text', 'project_name', 'start_date', 'end_date', 'project_leader', 'project_staffing', 'project_status',
                  'project_team')