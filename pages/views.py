from django.shortcuts import render

def company_home(request):
    return render(request, 'pages/company_home.html')

def company_about(request):
    # Mock data for demonstration. In a real application, this data would be fetched dynamically
    # based on the logged-in user/company profile.
    context = {
        'company_display_name': 'Innovative Solutions Inc.',
        'mission_text': 'Our mission is to simplify complex data analysis for small businesses.',
        'problems_solved': 'We help companies overcome the challenge of interpreting large datasets quickly, enabling better decision-making without requiring dedicated data science teams.',
        'contact_email': 'contact@innovativesolutions.com',
    }
    return render(request, 'pages/company_about.html', context)
