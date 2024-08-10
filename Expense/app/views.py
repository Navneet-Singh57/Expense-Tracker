from django.shortcuts import render,redirect
from .forms import ExpenseForm
from .models import Expense
import datetime
from django.db.models import Sum

# Create your views here.
def index(request):
    if request.method == "POST":
        expense = ExpenseForm(request.POST)
        if expense.is_valid():
            expense.save()
            return redirect('index')
            
    expenses = Expense.objects.all()
    total_expenses = expenses.aggregate(Sum('cost'))
    
    #For Year expenses
    last_year = datetime.date.today() - datetime.timedelta(days=365)
    data = Expense.objects.filter(date__gt=last_year)
    yearly_sum = data.aggregate(Sum('cost'))
    
    #For Month expenses
    last_month = datetime.date.today() - datetime.timedelta(days=30)
    data = Expense.objects.filter(date__gt=last_month)
    monthly_sum = data.aggregate(Sum('cost'))
    
    #For Week expenses
    last_week = datetime.date.today() - datetime.timedelta(days=7)
    data = Expense.objects.filter(date__gt=last_week)
    weekly_sum = data.aggregate(Sum('cost'))
    
    daily_sums = Expense.objects.filter().values('date').order_by('date').annotate(sum=Sum('cost'))
    
    category_sums = Expense.objects.filter().values('category').order_by('category').annotate(sum=Sum('cost'))
    
    form = ExpenseForm()
    
    context = {
        'form':form,
        'expenses':expenses,
        'total_expenses':total_expenses,
        'yearly_sum':yearly_sum,
        'monthly_sum':monthly_sum,
        'weekly_sum':weekly_sum,
        'daily_sums':daily_sums,
        'category_sums':category_sums,
        }
    return render(request,'app/index.html',context)

def edit(request,id):
    if request.method == "POST":
        expense = Expense.objects.get(id=id)
        form = ExpenseForm(request.POST,instance=expense)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        expense = Expense.objects.get(id=id)
        form = ExpenseForm(instance=expense)      
    return render(request,'app/edit.html',{'form':form})


def delete(request,id):
    if request.method == "POST" and "delete" in request.POST:
        expense = Expense.objects.get(id=id)
        expense.delete()
    return redirect('index')
        
    
    