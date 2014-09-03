from django import forms
from eumkd.models import Resource
from tdata.models import Specialty, Discipline

ERROR_ONE_FIELD_IS_REQUIRED = 'Вы должны заполнить одно из полей'


class ModelChoiceFieldWithText(forms.ModelChoiceField):
    """
    Class that provides text for field by object_id in current queryset
    """

    object_id = None

    def validate(self, value):
        """
        Sets object_id if exist for next usage
        """
        super(ModelChoiceFieldWithText, self).validate(value)
        if value:
            self.object_id = value.Id

    @property
    def text(self):
        try:
            return self.queryset.get(Id=self.object_id).Name
        except:
            return ''


class EumkdSearchForm(forms.ModelForm):
    """
    Class that present search form for search page
    """
    number = forms.CharField(label='Номер', max_length=16, required=False)
    discipline = ModelChoiceFieldWithText(
        label='Дисцилина', queryset=Discipline.objects.all(), empty_label='Не выбрано',
        required=False
    )
    specialty = ModelChoiceFieldWithText(
        label='Cпециальность', queryset=Specialty.objects.all(), empty_label='Не выбрано',
        required=False
    )

    def find_resources(self):
        """
        Provides custom filter from form attributes
        """
        kwargs = {}
        if self.cleaned_data.get('number'):
            kwargs['number'] = self.cleaned_data['number']
            return Resource.objects.filter(**kwargs)

        if self.cleaned_data.get('discipline'):
            kwargs['discipline'] = self.cleaned_data['discipline']
            return Resource.objects.filter(**kwargs)

        if self.cleaned_data.get('specialty'):
            kwargs['specialty'] = self.cleaned_data['specialty']
            return Resource.objects.filter(**kwargs)

    def clean(self):
        """
        Provides extra clean validation for form fields
        """
        cleaned_data = super(EumkdSearchForm, self).clean()
        number = cleaned_data.get('number')
        discipline = cleaned_data.get('discipline')
        specialty = cleaned_data.get('specialty')

        if not number and not discipline and not specialty:
            self.add_error('number', ERROR_ONE_FIELD_IS_REQUIRED)

    class Meta:
        model = Resource
        fields = ['number']