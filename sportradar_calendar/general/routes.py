from .services import DatabaseManager, ItemServiceError
from flask import render_template, request, flash


# Route to add a new sport
def general_add_view(manager: DatabaseManager, endpoint: str) -> str:
    if request.method == "POST":
        try:
            manager.add(**request.form)
            flash(f"Item is successfully added!", "success")

        except ItemServiceError as e:
            flash(str(e), "danger")
    columns = manager.get_columns()
    return render_template(endpoint, columns=columns)


# Route to display delete sport page
def general_get_all_view(
    manager: DatabaseManager,
    endpoint: str,
    lookups=None,
    header_labels=None,
    items=None,
    **kwargs,
):
    if not items:
        items = manager.get_all()
    columns = manager.get_columns()
    return render_template(
        endpoint,
        manager=manager,
        items=items,
        columns=columns,
        id_field=columns[0]["name"],
        lookups=lookups,
        header_labels=header_labels,
        **kwargs,
    )


# Route to delete a sport by ID
def general_delete(manager: DatabaseManager, id: int, endpoint: str):
    try:
        manager.delete(id=id)
        flash(f'Item "{id}" deleted', "success")
    except ItemServiceError as e:
        flash(str(e), "danger")

    return general_get_all_view(manager=manager, endpoint=endpoint)
