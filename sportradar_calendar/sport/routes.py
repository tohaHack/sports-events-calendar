from .services import manager
from ..general.routes import general_add_view, general_get_all_view, general_delete

def add_view():
    return general_add_view(manager=manager, endpoint='sport/form_add_sport.html')

def get_all_view():
    return general_get_all_view(manager=manager, endpoint='sport/index.html')

def delete(id: int):
    return general_delete(manager=manager, id=id, endpoint='sport/index.html')