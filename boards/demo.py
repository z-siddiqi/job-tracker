from .models import Board, Job

from notes.models import Note

def create_demo_board(user):
    board = Board.objects.create(title="Demo Board", user=user)
    job = Job.objects.create(
        board=board,
        company='Company',
        title='Title',
        description='This is a demo job application.'
    )
    note = Note.objects.create(job=job)
