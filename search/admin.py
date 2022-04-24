from django.contrib import admin
from search.models import para, searchinpara

class paraAdmin(admin.ModelAdmin):
    # original list display
    # list_display=('id','sentence',)

    #showing only first 50 leters of the paragrah
    list_display=('id', 'less_content',)
    list_display_links=('id', 'less_content',)

    # to show only first 50 letters of the paragraph
    def less_content(self, obj):
        return obj.sentence[:50]

class searchinparaAdmin(admin.ModelAdmin):
    list_display=('id','word','index',)
    list_display_links=('id','word','index',)


admin.site.register(para, paraAdmin)
admin.site.register(searchinpara, searchinparaAdmin)
