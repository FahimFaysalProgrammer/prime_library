from django.shortcuts import render, redirect
from django.views import View
from . import forms

# Create your views here.
class AddCategoryView(View):
    template_name = 'add_category.html'

    def get(self, request):
        category_form = forms.CategoryForm()
        return render(request, self.template_name, {'form': category_form})

    def post(self, request):
        category_form = forms.CategoryForm(request.POST)
        if category_form.is_valid():
            category_form.save()
            return redirect('add_category')

        return render(request, self.template_name, {'form': category_form})