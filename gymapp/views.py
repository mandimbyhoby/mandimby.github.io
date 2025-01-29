from django.shortcuts import render
from .models import Program
# Create your views here.

def index(request):
    programmes = [
        {'title': 'Basic Fitness', 'description': 'Basic fitness program description here.'},
        {'title': 'Advanced Muscle Course', 'description': 'Advanced muscle program description here.'},
        {'title': 'New Gym Training', 'description': 'New gym training program description here.'},
        {'title': 'Yoga Training', 'description': 'Yoga Training program description here.'},
        {'title': 'Basic Muscle Course', 'description': 'Basic Muscle Course program description here.'},
        {'title': 'Body Building Course', 'description': 'Body Building program description here.'},

    ]
    return render(request, 'index.html', {'programs': programmes})

