# Sports Event Calendar

A Flask-based web application for managing sports events, teams, venues, and scheduling. This project provides a clean interface for creating and managing sports events with their related entities.

## Features

- **Event Management**: Create, view, and delete sports events
- **Team Management**: Manage home and away teams
- **Venue Administration**: Track event locations and cities
- **Sport Categories**: Organize events by sport type
- **Data Validation**: Ensures data integrity and proper relationships
- **Responsive UI**: Bootstrap-based interface for all screen sizes

## Technology Stack

- **Backend**: Python 3.x with Flask
- **Database**: SQLite with SQLAlchemy
- **Frontend**: HTML5, Bootstrap 4.5
- **Documentation**: ERAlchemy for database schema visualization

## Project Structure

```
sportradar_calendar/
├── __init__.py           # Flask app initialization
├── config.py            # Configuration settings
├── db.py               # Database connection and initialization
├── schema.sql          # Database schema
├── calendar/           # Calendar view functionality
├── sports/            # Sports management
├── teams/             # Team management
├── venues/            # Venue management
├── general/           # Shared functionality
├── static/            # Static assets (CSS, JS)
└── templates/         # Jinja2 templates
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- SQLite3

## Installation

1. Clone the repository:
```bash
git clone https://github.com/tohaHack/sports-events-calendar
cd sportradar_task
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
flask --app sportradar_calendar init-db
```

## Running the Application

1. Start the Flask development server:
```bash
flask --app sportradar_calendar run
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

## Development Guidelines

- Use the provided database schema in `schema.sql`
- Follow the Flask application factory pattern
- Implement proper error handling and validation
- Write tests for new functionality
- Keep the code modular and maintainable

## Testing

Run the test suite using Python's built-in unittest. The simplest command (and the one that works in this project) is:

```powershell
# Run all tests (unittest discovery)
python -m unittest
```

Important: activate your project's virtual environment first (so dependencies like Flask are available). On Windows PowerShell:

```powershell
# Activate virtualenv (from project root)
venv\Scripts\Activate
```

If you want more control, you can still run targeted discovery commands, for example:

```powershell
# Run all tests in the package (explicit discovery)
python -m unittest discover -s sportradar_calendar -p "test_*.py" -t . -v

# Focused run for the 'general' tests
python -m unittest discover -s sportradar_calendar/general/test -p "test_*.py" -v
```

Notes:
- Ensure the virtualenv is activated so Python can import dependencies like Flask.
- Make sure test folders contain `__init__.py` so discovery treats them as packages; you mentioned you added those files which allows the project-wide discovery command to work.

## Database Schema

The application uses a relational database with the following main tables:
- `event`: Stores sports events with relationships to teams, venues, and sports
- `sport`: Manages different types of sports
- `team`: Tracks participating teams
- `venue`: Records event locations

## API Endpoints

The application provides several REST endpoints for managing entities:

The application routes are mounted as follows (matching the app factory in `sportradar_calendar/__init__.py`):

- Event endpoints
  - `GET /` — list and view events (mapped to `event.get_all_view`)
  - `GET /add`, `POST /add` — show add-event form / submit new event (`event.add`)
  - `DELETE /delete/<id>` — delete event by id (`event.delete`)

- Sport endpoints
  - `GET /sport` — list sports (`sport.get_all_view`)
  - `GET /sport/add`, `POST /sport/add` — add sport (`sport.add`)
  - `DELETE /sport/delete/<id>` — delete sport by id (`sport.delete`)

- Team endpoints
  - `GET /team` — list teams (`team.get_all_view`)
  - `GET /team/add`, `POST /team/add` — add team (`team.add`)
  - `DELETE /team/delete/<id>` — delete team by id (`team.delete`)

- Venue endpoints
  - `GET /venue` — list venues (`venue.get_all_view`)
  - `GET /venue/add`, `POST /venue/add` — add venue (`venue.add`)
  - `DELETE /venue/delete/<id>` — delete venue by id (`venue.delete`)

## Future Improvements

- Add user authentication and authorization
- Implement event search and filtering
- Add support for recurring events
- Enable bulk operations for events
- Add API documentation with Swagger/OpenAPI

## Contributing

1. Create a feature branch
2. Write tests for new functionality
3. Ensure all tests pass
4. Submit a pull request

---

## AI Usage Reflection

### Code Authorship (what I wrote)

I implemented the entire backend and core of the application by hand. This includes:
- All route handlers and view logic (per-blueprint routes)
- Services and business logic that operate on the database
- The project architecture and folder structure
- Database schema, migrations/initialization, and custom SQL queries
- Application configuration, error handling and validation logic

### AI-Assisted Work (what I used AI for)

I used AI tools (e.g., GitHub Copilot, ChatGPT) as assistance for frontend and test scaffolding. These AI-assisted parts were reviewed, adapted and integrated by me. Specifically:
- HTML templates, forms and CSS (Bootstrap integration and layout)
- Reusable Jinja2 template macros and base templates
- Unit test scaffolding and templates (unittest)
  - Note: I chose the `unittest` framework intentionally to organize tests into folders and keep event-specific tests separated from general/shared tests. This makes the test suite more modular and easier to navigate when logic differs between components (for example, `event` routes vs general helpers).
- Test case structure, mock patterns and example assertions
- Documentation snippets and README drafting

All AI-generated suggestions were inspected, edited and incorporated only after I verified they matched the project's requirements and style.

### AI as a Learning and Explanation Tool

I also relied on AI frequently as a learning aid: I used it to explain concepts, clarify why certain patterns work, and help structure my thoughts while designing features. I treat AI as an assistant for gaining understanding and organizing ideas — I review and validate any suggestions before applying them. This project benefited from that workflow: AI helped speed up learning and iterate faster, while the implementation and final decisions remained mine.

### Technical Decisions

1. **Flask Framework**: Chosen for its simplicity and excellent documentation
2. **SQLite Database**: Selected for easy setup and development
3. **Bootstrap Frontend**: Ensures responsive design without custom CSS
4. **Modular Structure**: Separates concerns for maintainability

### Planned Improvements

With more time, I would:
- Implement a more robust event filtering system
- Add caching for frequently accessed data
- Improve test coverage
- Add real-time updates for event changes

### Honor Statement

I confirm that:
- The submitted work reflects my own understanding
- The solution was implemented by me
- AI usage has been documented transparently
- I can explain and modify any part of the code
 
## Developer Reflection

I enjoyed automating code for most of the tables in the project — building general routes and services that work across entities felt productive and scalable. I intentionally excluded the `event` table from the full automation because its add/display logic and filtering behavior are more complex and required bespoke handling.

Implementing the `DatabaseManager` and general service layer was particularly satisfying: it allowed me to automate common CRUD patterns and focus on the unique business logic for events. Working directly with the database and seeing changes immediately on the web pages was motivating — I could quickly verify the data I created and iterate.

This project was a pleasure to build. Even if it doesn't lead to a job, I'm proud that I completed it and learned a lot in the process.