from .models import Board

def boards_processor(request):
    try:
        boards = Board.objects.filter(user=request.user)         
        context = {'boards': boards}
    except TypeError as e:
        context = {}
    
    return context
