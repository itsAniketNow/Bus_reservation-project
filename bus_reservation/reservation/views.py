from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Route, Ticket, Notification
from django.contrib.auth import logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import TicketForm
from .forms import SignupForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Signup view
def signup(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect to home or another page if the user is already logged in
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save() # Save the new user.
            return redirect('login')  # Redirect to login page after successful signup
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

# Login view (use Django's default login functionality)
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the home page after login
        else:
            error_message = "Invalid username or password."
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

# Home page
@login_required
def home(request):
    if request.method == "POST":
        # Handle ticket cancellation
        ticket_id = request.POST.get("ticket_id")
        try:
            ticket = Ticket.objects.get(id=ticket_id, user=request.user)
            ticket.delete()
            messages.success(request, "Ticket canceled successfully.")
        except Ticket.DoesNotExist:
            messages.error(request, "Ticket not found or you do not have permission to cancel this ticket.")
        return redirect("home")

    # Fetch remaining tickets for the user and all routes
    tickets = Ticket.objects.filter(user=request.user, date__gte=timezone.now()).select_related('route')
    routes = Route.objects.all()

    return render(request, 'home.html', {
        'routes': routes,
        'tickets': tickets,
    })


# Ticket search
@login_required
def search(request):
    routes = None
    if request.method == 'POST':
        start_city = request.POST.get('start_city', '').strip()
        destination = request.POST.get('destination', '').strip()

        # Ensure both start city and destination are provided
        if start_city and destination:
            # Perform a case-insensitive search for both start and destination cities
            routes = Route.objects.filter(
                start_city__icontains=start_city, 
                destination__icontains=destination
            )
        else:
            routes = Route.objects.none()  # No routes found if one or both fields are empty

    return render(request, 'search.html', {'routes': routes})

# Ticket booking page
@login_required
def ticket_booking(request, route_id):
    route = Route.objects.get(id=route_id)
    if request.method == 'POST':
        print("Form submitted.")
        form = TicketForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.route = route
            # Ensure the ticket date is in the future
            if ticket.date < timezone.now().date():
                form.add_error('date', 'The ticket date must be in the future.')
                print("Ticket date is in the past.")
                return render(request, 'ticket_booking.html', {'route': route, 'form': form})
            ticket.save()
            Notification.objects.create(user=request.user, message=f"Ticket booked from {route.start_city} to {route.destination}")
            print("Ticket saved.")
            return redirect('confirmation')
        else:
            print("Form is invalid")
            print(form.errors)  # Print any errors to the console
    else:
        form = TicketForm()

    return render(request, 'ticket_booking.html', {'route': route, 'form': form})


# Confirmation page (message displayed and then redirects to home)
@login_required
def confirmation(request):
    return render(request, 'confirmation.html')

# User's ticket history
@login_required
def ticket_history(request):
    tickets = Ticket.objects.filter(user=request.user)
    return render(request, 'ticket_history.html', {'tickets': tickets})


@login_required
@csrf_exempt
def cancel_ticket(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        ticket_id = data.get("ticket_id")
        try:
            ticket = Ticket.objects.get(id=ticket_id, user=request.user)
            ticket.delete()
            return JsonResponse({"success": True, "message": "Ticket canceled successfully."})
        except Ticket.DoesNotExist:
            return JsonResponse({"success": False, "message": "Ticket not found."}, status=404)
    return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)

# Account view and notifications
@login_required
def account(request):
    notifications = Notification.objects.filter(user=request.user)
    return render(request, 'account.html', {'notifications': notifications})


# Logout view
@login_required
def logout_view(request):
    logout(request)
    return redirect('signup')  # Redirect to the signup page after logout