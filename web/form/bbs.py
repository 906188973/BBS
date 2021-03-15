from django import forms
from web.models import Forum, Topic, Floor
from django.core.exceptions import ValidationError

class ForumForm(forms.ModelForm):
    forum_name = forms.CharField(label='版块名')

    class Meta:
        model = Forum
        fields = ['forum_name', 'picture']

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

class FloorForm(forms.ModelForm):
    class Meta:
        model = Floor
        fields = ['floor_text']
        labels = {'floor_text': ''}
        widgets = {'floor_text': forms.Textarea(attrs={'cols': 80})}