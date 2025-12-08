from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import User

def welcome(request):
    return render(request, 'welcome.html')

@login_required
def screen1(request):
    role = request.user.user_type.title() if hasattr(request.user, 'user_type') else 'User'
    return render(request, 'pages/screen1.html', {'role': role})

@login_required
def screen2(request):
    role = request.user.user_type.title() if hasattr(request.user, 'user_type') else 'User'
    return render(request, 'pages/screen2.html', {'role': role})

@login_required
def screen3(request):
    role = request.user.user_type.title() if hasattr(request.user, 'user_type') else 'User'
    return render(request, 'pages/screen3.html', {'role': role})

@login_required
def notifications(request): # added for notifications page
    # This is dummy data for now.
    current_notifications = [
        "Your profile was updated.",
        "You have a new message from Admin.",
    ]
    previous_notifications = [
        "Your password was changed a week ago.",
        "Welcome to the platform!",
    ]
    context = {
        'current_notifications': current_notifications,
        'previous_notifications': previous_notifications,
    }
    return render(request, 'pages/notifications.html', context)

@login_required
def university_home(request):
    # Restrict access to only university users
    if request.user.user_type != User.UserType.UNIVERSITY:
        return redirect('screen1')  # Redirect if not a university user

    # Placeholder context for university_home.html
    context = {
        'university_name': request.user.username.title() if request.user.is_authenticated else 'University',
        # Add any other data relevant to university users here
    }
    return render(request, 'pages/university_home.html', context)


@login_required
def company_home(request):
    # Restrict access to only company users
    if request.user.user_type != User.UserType.COMPANY:
        return redirect('screen1') # Redirect if not a company user

    # Placeholder for Project objects.
    # In a real application, you would import and query your Project model here.
    all_projects = [
        {'id': 1, 'title': 'AI-Powered Chatbot for Customer Service', 'field': 'Artificial Intelligence', 'description': 'Developing a chatbot using natural language processing to enhance customer support experience.'},
        {'id': 2, 'title': 'Sustainable Energy Management System', 'field': 'Renewable Energy', 'description': 'A system to monitor and optimize energy consumption for commercial buildings using IoT.'},
        {'id': 3, 'title': 'Blockchain for Supply Chain Traceability', 'field': 'Blockchain', 'description': 'Implementing a decentralized ledger to track products from origin to consumer.'},
        {'id': 4, 'title': 'Personalized Learning Platform', 'field': 'Education Technology', 'description': 'An adaptive platform that customizes learning paths based on student performance and preferences.'},
        {'id': 5, 'title': 'Predictive Maintenance for Industrial Machinery', 'field': 'Manufacturing', 'description': 'Using machine learning to predict equipment failures and optimize maintenance schedules.'},
        {'id': 6, 'title': 'Smart City Traffic Management', 'field': 'Urban Planning', 'description': 'Developing an intelligent system to alleviate traffic congestion using real-time data.'},
    ]

    projects = all_projects
    query = request.GET.get('q')
    field_filter = request.GET.get('field')

    if query:
        projects = [p for p in projects if query.lower() in p['title'].lower() or query.lower() in p['description'].lower()]
    if field_filter and field_filter != 'All':
        projects = [p for p in projects if p['field'] == field_filter]

    # Get all unique fields for the filter dropdown
    available_fields = sorted(list(set([p['field'] for p in all_projects])))
    available_fields.insert(0, 'All') # Add 'All' option at the beginning

    context = {
        'projects': projects,
        'current_query': query if query else '',
        'current_field': field_filter if field_filter else 'All',
        'available_fields': available_fields,
    }
    return render(request, 'pages/company_home.html', context)


@login_required
def company_about(request):
    # This view is for the company's "About" page, which can also serve as a profile page.
    # It's restricted to company users.
    if request.user.user_type != User.UserType.COMPANY:
        return redirect('screen1') # Or some other appropriate page

    # In a real app, this data might come from the company's profile model
    context = {
        'company_name': request.user.display_name,
        'mission': "To foster innovation by connecting with the brightest academic minds.",
        'problem_solved': "We bridge the gap between academic research and industry application, helping to bring groundbreaking ideas to market.",
        'contact_email': request.user.email,
    }
    return render(request, 'pages/company_about.html', context)
