from django.shortcuts import render, redirect, get_object_or_404
from CustomerInformation.models import Company,LicenseInformation
from .forms import NewLicenseInformationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(request):
    companies = Company.objects.all()
    return render(request, 'home.html', {'companies': companies})

@login_required
def company_licenseinfo(request, pk):
    company = get_object_or_404(Company, pk=pk)
    return render(request, 'licenseinfo.html', {'company': company})

@login_required
def new_company_licenseinfo(request, pk):
    company = get_object_or_404(Company, pk=pk)
    user = User.objects.first()  # TODO: get the currently logged in user
    if request.method == "POST":
        form = NewLicenseInformationForm(request.POST)
        if form.is_valid():
            licenseinfo = form.save(commit=False)
            licenseinfo.company = company
            licenseinfo.created_by = request.user
            licenseinfo.updated_by = request.user
            licenseinfo.license = "ABCD-EFGH-1234"
            licenseinfo.save()
            return redirect('company_licenseinfo', pk=company.pk)
    else:
        form = NewLicenseInformationForm()
    return render(request, 'new_licenseinfo.html', {'company': company, 'form': form})
      