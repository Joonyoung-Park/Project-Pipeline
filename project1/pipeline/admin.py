from django.contrib import admin
from pipeline.models import Frontpage, Pipeline


# class RatingAdmin(admin.ModelAdmin):
#     readonly_fields = ('date',)
#
#
# admin.site.register(Rating, RatingAdmin)

class PipelineAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)
    #
    # def add_view(self, request, form_url='', extra_context=None):
    #     if request.user.get_profile().is_employee:
    #         self.model.branch.field.editable = False
    #     else:
    #         self.model.branch.field.editable = True
    #     return super(PipelineAdmin, self).add_view(request, form_url)


admin.site.register(Frontpage)
admin.site.register(Pipeline, PipelineAdmin)
