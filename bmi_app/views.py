from django.shortcuts import render, redirect
from .models import BMIRecord
from .forms import RegisterForm 
from django.contrib.auth.decorators import login_required

def register(request):
  
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request,'register.html',{'form':form})


@login_required
def dashboard(request):
    return render(request,'dashboard.html')


@login_required
def bmi_calculator(request):

    if request.method == "POST":

        weight = request.POST.get('weight')
        height = request.POST.get('height')

        if weight and height:
         weight = float(weight)
         height = float(height) / 100

        bmi = weight / (height ** 2)

        if bmi < 18.5:
            category = "Underweight"
            advice = "You may need to gain weight. Eat nutritious meals."
        elif bmi < 25:
            category = "Normal"
            advice = "Great! Maintain your healthy lifestyle."
        elif bmi < 30:
            category = "Overweight"
            advice = "Consider regular exercise and balanced diet."
        else:
            category = "Obese"
            advice = "Consult a doctor and start a healthier routine."

        BMIRecord.objects.create(
            user=request.user,
            weight=weight,
            height=height,
            bmi=bmi,
            category=category
        )

        return render(request,'bmi.html',{
            'bmi': round(bmi,2),
            'category': category,
            'advice': advice
        })

    return render(request,'bmi.html')
@login_required
def history(request):

    records = BMIRecord.objects.filter(user=request.user)

    bmi_values = []
    dates = []

    for record in records:
        bmi_values.append(record.bmi)
        dates.append(record.id)

    context = {
        'records': records,
        'bmi_values': bmi_values,
        'dates': dates
    }

    return render(request, 'history.html', context)