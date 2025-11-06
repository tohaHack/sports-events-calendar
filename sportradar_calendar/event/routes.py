from datetime import datetime
from .services import manager
from ..general.routes import general_add_view, general_get_all_view, general_delete
from flask import render_template, request, flash
from ..sport.services import manager as sport_manager
from ..team.services import manager as team_manager
from ..venue.services import manager as venue_manager


def add_view():
    if request.method == "POST":
        return general_add_view(manager=manager, endpoint="event/form_add_event.html")

    sports = [dict(r) for r in sport_manager.get_all()]
    teams = [dict(r) for r in team_manager.get_all()]
    venues = [dict(r) for r in venue_manager.get_all()]
    columns = manager.get_columns()
    return render_template(
        "event/form_add_event.html",
        columns=columns,
        sports=sports,
        teams=teams,
        venues=venues,
    )


def get_all_view():
    # Prepare lookup dictionaries for foreign key fields
    lookups = {
        "_sport_id": {s["sport_id"]: s["name"] for s in sport_manager.get_all()},
        "_home_team_id": {t["team_id"]: t["name"] for t in team_manager.get_all()},
        "_away_team_id": {t["team_id"]: t["name"] for t in team_manager.get_all()},
        "_venue_id": {
            v["venue_id"]: f"{v['name']} — {v['city']}" for v in venue_manager.get_all()
        },
    }

    # Define header labels for better readability
    header_labels = {
        "_sport_id": "sport",
        "_home_team_id": "home_team",
        "_away_team_id": "away_team",
        "_venue_id": "venue",
    }

    # Filter items on sport and date
    sport_id = request.args.get('sport_id', type=int)
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    rows = manager.get_filtered(sport_id=sport_id, date_from=date_from, date_to=date_to)

    sports = sport_manager.get_all()

    # Format DateTime field for display
    items = [dict(item) for item in rows]
    for it in items:
        raw = it.get('event_date')
        dt = datetime.strptime(raw, "%Y-%m-%dT%H:%M") if raw else None
        if raw:
            it['event_date_fmt'] = dt.strftime("%Y-%m-%d %H:%M") if dt else raw

    return general_get_all_view(
        manager=manager,
        endpoint="event/index.html",
        lookups=lookups,
        header_labels=header_labels,
        items=items,
        sports=sports,
        selected_sport=sport_id or '',
        date_from=date_from or '',
        date_to=date_to or ''
    )


def delete(id: int):
    return general_delete(manager=manager, id=id, endpoint="event/index.html")
