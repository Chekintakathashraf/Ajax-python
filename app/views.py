from django.shortcuts import render
from .forms import OfficeForm, EmployeeForm
from .models import Office, Employee
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.core import serializers
import json

def home(request):
    officeForm = OfficeForm()
    employeeForm = EmployeeForm()

    # Fetch all offices to display on the home page
    offices = Office.objects.all()

    context = {
        "officeForm": officeForm,
        "employeeForm": employeeForm,
        "offices": offices,  # Pass offices to the template
    }
    return render(request, 'index.html', context=context)

def officeCrud(request):
    if request.method == "POST": 
        officeForm = OfficeForm(request.POST)
        office = officeForm.save()
        return JsonResponse(model_to_dict(office), safe=False)

def employeeCrud(request):
    if request.method == "POST": 
        employeeForm = EmployeeForm(request.POST)
        employee = employeeForm.save()
        return JsonResponse(model_to_dict(employee), safe=False)

    if request.method == "PUT":
        data = json.loads(request.body)
        data['office'] = Office(id=data.get('office'))
        employee = Employee(**data)
        employee.save()
        return JsonResponse(model_to_dict(employee), safe=False)

def getAllOffices(request):
    offices = Office.objects.all()
    data = serializers.serialize("json", offices)
    return JsonResponse(data, safe=False)

def getAllEmployees(request):
    employees = Employee.objects.all()
    data = serializers.serialize("json", employees, use_natural_foreign_keys=True)
    return JsonResponse(data, safe=False)

def showEmployeePage(request):
    employeeForm = EmployeeForm()
    return render(request, 'employee-page.html', {'employeeForm': employeeForm})

def showOfficePage(request):
    officeForm = OfficeForm()
    return render(request, 'office-page.html', {'officeForm': officeForm})
