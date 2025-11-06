from flask import Flask

def create_app():

    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    # Database
    from . import db
    db.init_app(app=app)

    # Event
    from . import event
    app.add_url_rule('/add', 'event.add',  event.routes.add_view, methods=['GET', 'POST'])
    app.add_url_rule('/', 'event', event.routes.get_all_view, methods=['GET'])
    app.add_url_rule('/delete/<id>', 'event.delete', event.routes.delete, methods=['DELETE'])

    # Sport
    from . import sport
    app.add_url_rule('/sport/add', 'sport.add',  sport.routes.add_view, methods=['GET', 'POST'])
    app.add_url_rule('/sport', 'sport', sport.routes.get_all_view, methods=['GET'])
    app.add_url_rule('/sport/delete/<id>', 'sport.delete', sport.routes.delete, methods=['DELETE'])

    # Team
    from . import team
    app.add_url_rule('/team/add', 'team.add',  team.routes.add_view, methods=['GET', 'POST'])
    app.add_url_rule('/team', 'team', team.routes.get_all_view, methods=['GET'])
    app.add_url_rule('/team/delete/<id>', 'team.delete', team.routes.delete, methods=['DELETE'])

    # Venue
    from . import venue
    app.add_url_rule('/venue/add', 'venue.add',  venue.routes.add_view, methods=['GET', 'POST'])
    app.add_url_rule('/venue', 'venue', venue.routes.get_all_view, methods=['GET'])
    app.add_url_rule('/venue/delete/<id>', 'venue.delete', venue.routes.delete, methods=['DELETE'])


    return app