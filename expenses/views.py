from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages

# Create your views here.
@login_required(login_url='/authentication/login')
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)

    context = {
        'categories': categories,
        'expenses': expenses
    }

    return render(request, 'expenses/index.html', context)


def add_expense(request):
    categories = Category.objects.all()

    context = {
        'categories': categories,
        'values': request.POST
    }

    if request.method == 'GET':
        return render(request, 'expenses/add-expense.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        date = request.POST['expense_date']
        category = request.POST['category']
        description = request.POST['description']

        if not amount or not date or not category:
            messages.error(request, 'Action Failed, Amount, Date and Category Is Required')
            return render(request, 'expenses/add-expense.html', context)
        
        Expense.objects.create(owner=request.user, amount=amount, date=date,category=category, description=description)
        messages.success(request, 'Expense Created')
        return redirect('expenses')
    

def edit_expense(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
            'expense': expense,
            'values': expense,
            'categories': categories
        }

    if request.method == 'GET':
        return render(request, 'expenses/edit-expense.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        category = request.POST['category']
        description = request.POST['description']

        if not amount or not category:
            messages.error(request, 'Action Failed, Amount, Date and Category Is Required')
            return render(request, 'expenses/edit-expense.html', context)
        
        expense.owner = request.user
        expense.amount=amount
        expense.category=category
        expense.description=description
        expense.save()

        messages.success(request, 'Expense Updated Succesfully')
        return redirect('expenses')
    

def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()

    messages.error(request, 'Expense Deleted Succesfully')
    return redirect('expenses')