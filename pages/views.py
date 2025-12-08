from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import User # Import User model for UserType access

@login_required
def company_home(request):
    if request.user.user_type != User.UserType.COMPANY:
        return redirect('screen1')
    return render(request, 'pages/company_home.html')

@login_required
def company_about(request):
    if request.user.user_type != User.UserType.COMPANY:
        return redirect('screen1')
    
    # Mock data for demonstration. In a real application, this data would be fetched dynamically
    # based on the logged-in user/company profile.
    context = {
        'company_display_name': 'Innovative Solutions Inc.',
        'mission_text': 'Our mission is to simplify complex data analysis for small businesses.',
        'problems_solved': 'We help companies overcome the challenge of interpreting large datasets quickly, enabling better decision-making without requiring dedicated data science teams.',
        'contact_email': 'contact@innovativesolutions.com',
    }
    return render(request, 'pages/company_about.html', context)
