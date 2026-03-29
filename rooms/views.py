from django.shortcuts import render
from .models import Room, Building

# Create your views here.

def home(request):
    featured_rooms = Room.objects.select_related('building').all()[:6]
    buildings = Building.objects.all()

    context = {
        'featured_rooms': featured_rooms,
        'buildings': buildings,
    }
    return render(request, "rooms/home.html", context)

def room_list(request):
    rooms = Room.objects.all()
    buildings = Building.objects.all()

    building_id = request.GET.get('building') # consider using id instead of name
    date = request.GET.get('date')
    time = request.GET.get('time')
    min_capacity = request.GET.get('min_capacity')

    if building_id:
        rooms = rooms.filter(building_id=building_id)
    
    if min_capacity and min_capacity != '':
        try:
            min_capacity = int(min_capacity)
            rooms = rooms.filter(capacity__gte=min_capacity)
        except ValueError:
            pass

    selected_building = building_id if building_id else ''
    selected_date = date if date else ''
    selected_time = time if time else ''
    
    context = {
        'rooms': rooms,
        'buildings': buildings,
        'selected_building': selected_building,
        'selected_date': selected_date,
        'selected_time': selected_time,
        'min_capacity': min_capacity,
    }

    return render(request, "rooms/room_list.html", context)


# Reservation view (no login required)
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.shortcuts import redirect

@csrf_exempt
def reservation(request):
    from .models import Room
    rooms = Room.objects.select_related('building').all()
    success = False
    error = None
    if request.method == 'POST':
        room_id = request.POST.get('room')
        date = request.POST.get('date')
        time_ = request.POST.get('time')
        duration = request.POST.get('duration')
        name = request.POST.get('name')
        if not (room_id and date and time_ and duration):
            error = 'Please fill in all required fields.'
        else:
            # Here you would normally save the reservation to the database
            # For now, just show success (no model yet)
            success = True
    context = {
        'rooms': rooms,
        'success': success,
        'error': error,
    }
    return render(request, "rooms/reservation.html", context)
