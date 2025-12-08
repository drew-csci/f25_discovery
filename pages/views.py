from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import User

def welcome(request):
    return render(request, 'welcome.html')

@login_required
def screen1(request):
    if request.user.user_type == User.UserType.UNIVERSITY:
        return redirect('university_home')
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

    # Placeholder data for the university dashboard
    funding_updates = [
        {'title': 'New Grant for AI Research', 'description': 'The National Science Foundation has awarded a $5M grant for advancements in AI.', 'date_posted': '2 days ago'},
        {'title': 'Biotechnology Funding Initiative', 'description': 'A new initiative by PharmaCorp to fund biotech startups and university research.', 'date_posted': '1 week ago'},
    ]
    research_projects = [
        {'title': 'Quantum Computing Advancements', 'field': 'Physics', 'status': 'Ongoing'},
        {'title': 'CRISPR Gene Editing Applications', 'field': 'Biology', 'status': 'Ongoing'},
        {'title': 'Sustainable Urban Development', 'field': 'Architecture', 'status': 'Completed'},
    ]
    all_companies = [
        {'name': 'Tech Innovators Inc.', 'focus': ['AI', 'Machine Learning']},
        {'name': 'BioHealth Corp.', 'focus': ['Biotechnology', 'Patents']},
        {'name': 'GreenEnergy Solutions', 'focus': ['Renewable Energy', 'Research']},
        {'name': 'QuantumLeap Computing', 'focus': ['Quantum Computing', 'Patents']},
    ]

    # Search logic for companies
    query = request.GET.get('q', '')
    companies = all_companies
    if query:
        companies = [c for c in all_companies if query.lower() in c['name'].lower() or any(query.lower() in f.lower() for f in c['focus'])]

    context = {
        'university_name': request.user.username.title(),
        'funding_updates': funding_updates,
        'research_projects': research_projects,
        'companies': companies,
        'current_query': query,
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
    field_filter = request.GET.get('field', '')

    if query:
        projects = [p for p in projects if query.lower() in p['title'].lower() or query.lower() in p['description'].lower()]
    if field_filter:
        projects = [p for p in projects if p['field'] == field_filter]

    # Get all unique fields for the filter dropdown
    available_fields = sorted(list(set([p['field'] for p in all_projects])))

    context = {
        'projects': projects,
        'current_query': query if query else '',
        'current_field': field_filter,
        'available_fields': available_fields,
    }
    return render(request, 'pages/company_home.html', context)


@login_required
def company_profile(request):
    # Restrict access to only company users
    if request.user.user_type != User.UserType.COMPANY:
        return redirect('screen1') # Redirect if not a company user

    # This is dummy data for now, inspired by LinkedIn company profiles.
    company_data = {
        'name': request.user.username.title(),
        'tagline': 'Innovating for a better future, one line of code at a time.',
        'about': 'We are a forward-thinking technology company specializing in custom software solutions that drive business growth. Our mission is to empower our clients through innovative technology and expert consulting. We believe in creating partnerships, not just products.',
        'website': 'https://example.com',
        'industry': 'Information Technology & Services',
        'size': '51-200 employees',
        'headquarters': 'Tech City, Innovation State',
        'founded': 2010,
        'specialties': ['Web Development', 'Cloud Computing', 'AI & Machine Learning', 'Enterprise Solutions'],
        'projects': [
            {
                'title': 'AI-Powered Analytics Platform',
                'duration': '2022 - Present',
                'description': 'Developed a platform that provides deep insights into customer behavior using machine learning algorithms.'
            },
            {
                'title': 'Global E-commerce Marketplace',
                'duration': '2020 - 2022',
                'description': 'Built a scalable and secure marketplace serving millions of users worldwide.'
            },
        ],
        'jobs': [
            {
                'title': 'Senior Python Developer',
                'location': 'Remote',
                'type': 'Full-time'
            },
            {
                'title': 'Frontend Engineer (React)',
                'location': 'Tech City Office',
                'type': 'Full-time'
            },
        ]
    }
    
    context = {
        'company': company_data,
    }
    return render(request, 'pages/company_profile.html', context)


@login_required
def investor_profile(request):
    # Restrict access to only investor users
    if request.user.user_type != User.UserType.INVESTOR:
        return redirect('screen1') # Redirect if not an investor user

    # This is dummy data for now, inspired by LinkedIn/AngelList profiles.
    investor_data = {
        'name': request.user.display_name,
        'title': 'Managing Partner',
        'firm': 'Venture Capital Partners',
        'location': 'Silicon Valley, CA',
        'about': 'Seasoned investor with over 15 years of experience in early-stage technology startups. Passionate about helping entrepreneurs build disruptive companies. My focus is on SaaS, FinTech, and AI. Looking to connect with innovative founders who are changing the world.',
        'focus': {
            'industries': ['SaaS', 'FinTech', 'Artificial Intelligence', 'HealthTech'],
            'stage': 'Seed, Series A',
            'check_size': '$250k - $2M',
            'geography': 'North America',
        },
        'portfolio': [
            {
                'company': 'Innovate AI',
                'industry': 'Artificial Intelligence',
                'year': '2021',
                'description': 'A leading platform for developing and deploying machine learning models at scale.'
            },
            {
                'company': 'FinSecure',
                'industry': 'FinTech',
                'year': '2019',
                'description': 'Cybersecurity solutions for financial institutions, acquired by a major bank in 2023.'
            },
        ],
    }
    
    context = {
        'investor': investor_data,
    }
    return render(request, 'pages/investor_profile.html', context)


@login_required
def university_profile(request):
    # Restrict access to only university users
    if request.user.user_type != User.UserType.UNIVERSITY:
        return redirect('screen1') # Redirect if not a university user

    # This is dummy data for now.
    university_data = {
        'name': request.user.username.title(),
        'location': 'Innovation City, Knowledge State',
        'about': 'A leading institution for higher education and research, committed to academic excellence and fostering innovation. We have a rich history of producing leaders and pioneers in various fields.',
        'website': 'https://university.example.edu',
        'type': 'Public Research University',
        'enrollment': '35,000',
        'founded': 1850,
        'departments': [
            'Computer Science', 'Electrical Engineering', 'Biomedical Engineering',
            'Physics', 'Chemistry', 'Business Administration'
        ],
        'research': [
            {
                'title': 'Quantum Computing Advancements',
                'publication': 'Journal of Quantum Information',
                'summary': 'Breakthroughs in qubit stability and error correction, paving the way for more powerful quantum computers.'
            },
            {
                'title': 'CRISPR-based Gene Therapy for Genetic Disorders',
                'publication': 'Nature Biotechnology',
                'summary': 'Developing novel gene-editing techniques to treat inherited diseases with high precision.'
            },
        ],
    }
    
    context = {
        'university': university_data,
    }
    return render(request, 'pages/university_profile.html', context)
