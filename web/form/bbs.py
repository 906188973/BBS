from django import forms
from web.models import Forum, Topic, Floor
from django.core.exceptions import ValidationError
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class ForumForm(forms.ModelForm):
    forum_name = forms.CharField(label='版块名')

    class Meta:
        model = Forum
        fields = ['forum_name', 'picture', 'background']

    def clean_forum_name(self):
        forum_name = self.cleaned_data['forum_name']
        exists = Forum.objects.filter(forum_name=forum_name).exists()
        if exists:
            raise ValidationError('版块名已经存在')
        return forum_name

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['topic_text']
        labels = {'topic_text': ''}
        widgets = {'topic_text': forms.TextInput(attrs={'style': "width: 756.68px;"})}

class FloorForm(forms.Form):
    floor_text = forms.CharField(widget=CKEditorUploadingWidget(config_name='comment_ckeditor'))

    # class Meta:
    #     model = Floor
    #     fields = ['floor_text']
    #     labels = {'floor_text': ''}
    #     widgets = {'floor_text': forms.Textarea(attrs={'cols': 115, 'style': "resize:none"})}
    def clean_floor_text(self):
        floor_text = self.cleaned_data['floor_text']
        return floor_text