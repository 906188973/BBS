from django import forms
from web.models import Forum, Topic, Floor, ApplyforForum
from django.core.exceptions import ValidationError
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class ForumForm(forms.ModelForm):
    forum_name = forms.CharField(label='版块名')
    picture = forms.ImageField(label='头像')
    background = forms.ImageField(label='头像')

    class Meta:
        model = ApplyforForum
        fields = ['forum_name', 'picture', 'background', 'text']
        # widgets = {'text': forms.TextInput(attrs={'style': "width: 500px;"})}

    def clean_forum_name(self):
        forum_name = self.cleaned_data['forum_name']
        exists = Forum.objects.filter(forum_name=forum_name).exists()
        if exists:
            raise ValidationError('版块名已经存在')
        print(forum_name)
        return forum_name

    def clean_picture(self):
        picture = self.cleaned_data['picture']
        print(self.cleaned_data['picture'])
        return picture

    def clean_background(self):
        background = self.cleaned_data['background']
        print(self.cleaned_data['background'])
        return background

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

class TopicchangeForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['topic_text', 'forum', 'owner', 'top', 'refined']
        widgets = {'topic_text': forms.TextInput(attrs={'style': ""})}