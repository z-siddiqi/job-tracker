from .models import Board, Job

def create_demo_board(user):
    board = Board.objects.create(title="Demo Board", user=user)
    job = Job.objects.create(
        board=board,
        company='Company',
        title='Title',
        description=''
    )
