\# Facility Work Order Management API

A Python REST API for managing facility assets and maintenance work orders, applying priority-based SLA deadlines, enforcing controlled work-order status transitions, and reporting operational metrics.

\## Business Problem

Facilities and infrastructure teams need a consistent way to register assets, track maintenance work, prioritize interventions, monitor response deadlines, and identify overdue work.

This project demonstrates how a lightweight API and relational database can support those operational controls while providing a foundation for integration with dashboards, maintenance systems, or other applications.

\## Features

\- Register facility and infrastructure assets

\- Assign asset criticality levels

\- Create maintenance work orders linked to assets

\- Assign HIGH, MEDIUM, or LOW work-order priorities

\- Automatically calculate priority-based SLA deadlines

\- Track OPEN, IN\_PROGRESS, and COMPLETED work orders

\- Enforce controlled status transitions

\- Prevent completed work orders from being reopened

\- Identify overdue incomplete work orders

\- Produce operational work-order metrics

\- Persist application data in SQLite

\- Provide interactive OpenAPI/Swagger documentation

\- Run automated integration tests through GitHub Actions

\## Technology Stack

\- Python 3.13

\- FastAPI

\- SQLModel

\- SQLAlchemy

\- SQLite

\- pytest

\- HTTPX

\- Uvicorn

\- GitHub Actions

\## Architecture

The application separates responsibilities into distinct layers:

```text

Client / Swagger UI

&#x20;       |

&#x20;       v

FastAPI Routes

&#x20;       |

&#x20;       v

Service / Business Rules

&#x20;       |

&#x20;       v

SQLModel / SQLAlchemy

&#x20;       |

&#x20;       v

SQLite Database

```

Repository structure:

```text

facility-work-order-api/

├── app/

│   ├── \_\_init\_\_.py

│   ├── database.py

│   ├── main.py

│   ├── models.py

│   ├── routes.py

│   ├── schemas.py

│   └── services.py

├── data/

│   └── sample\_assets.json

├── tests/

│   ├── conftest.py

│   ├── test\_assets.py

│   ├── test\_metrics.py

│   └── test\_work\_orders.py

├── .github/

│   └── workflows/

│       └── tests.yml

├── .gitignore

├── requirements.txt

└── README.md

```

\## Data Model

\### Asset

Each asset contains:

\- `id`

\- `name`

\- `location`

\- `criticality`

Criticality values:

\- `HIGH`

\- `MEDIUM`

\- `LOW`

\### Work Order

Each work order contains:

\- `id`

\- `asset\_id`

\- `title`

\- `priority`

\- `status`

\- `created\_at`

\- `due\_at`

\- `completed\_at`

Each work order references an asset through `asset\_id`.

\## Illustrative SLA Rules

For this portfolio project, work-order deadlines are calculated using the following assumptions:

| Priority | SLA Deadline |

| --- | ---: |

| HIGH | 4 hours |

| MEDIUM | 24 hours |

| LOW | 72 hours |

These values are illustrative application rules only. They are not presented as industry-standard, regulatory, contractual, or client-specific SLA requirements.

\## Work-Order Lifecycle

Version 0.1 permits the following workflow:

```text

OPEN -> IN\_PROGRESS -> COMPLETED

```

Skipping stages or reopening a completed work order is rejected with HTTP `409 Conflict`.

\## API Endpoints

| Method | Endpoint | Purpose |

| --- | --- | --- |

| GET | `/` | API status |

| POST | `/assets` | Register an asset |

| GET | `/assets` | List assets |

| POST | `/work-orders` | Create a work order |

| GET | `/work-orders` | List work orders |

| PATCH | `/work-orders/{work\_order\_id}/status` | Change work-order status |

| GET | `/metrics` | Return operational metrics |

\## Installation

Clone the repository and enter the project directory:

```bash

git clone https://github.com/RCJantjies/facility-work-order-api.git

cd facility-work-order-api

```

Create and activate a Python environment, then install the dependencies:

```bash

python -m pip install -r requirements.txt

```

\## Running the API

Start the development server:

```bash

python -m uvicorn app.main:app --reload

```

Open the interactive API documentation at:

```text

http://127.0.0.1:8000/docs

```

\## Example Workflow

Create an asset:

```json

{

&#x20; "name": "Main Distribution Board",

&#x20; "location": "Building A - Electrical Room",

&#x20; "criticality": "HIGH"

}

```

Create a HIGH-priority work order for that asset:

```json

{

&#x20; "asset\_id": 1,

&#x20; "title": "Investigate abnormal heat at main distribution board",

&#x20; "priority": "HIGH"

}

```

The API automatically assigns `OPEN` status and calculates a deadline four hours after creation.

Progress the work order using:

```json

{

&#x20; "status": "IN\_PROGRESS"

}

```

and then:

```json

{

&#x20; "status": "COMPLETED"

}

```

Completion automatically records the completion timestamp.

\## Operational Metrics

`GET /metrics` returns:

```json

{

&#x20; "total": 1,

&#x20; "open": 0,

&#x20; "in\_progress": 0,

&#x20; "completed": 1,

&#x20; "overdue": 0

}

```

An overdue work order is an incomplete work order whose SLA deadline has passed.

\## Testing

The project includes automated integration tests covering:

\- Asset creation and retrieval

\- Input validation

\- HIGH, MEDIUM, and LOW SLA calculations

\- Missing asset handling

\- Work-order status progression

\- Invalid status transitions

\- Missing work-order handling

\- Operational metrics

\- Overdue work-order detection

\- Completed-work-order overdue exclusion

Run the complete suite with:

```bash

python -m pytest -v

```

Version 0.1 contains \*\*15 automated tests\*\*.

GitHub Actions runs the test suite automatically on pushes and pull requests to `main`.

\## Data and Privacy

All demonstration assets, locations, work orders, and operational scenarios in this repository are synthetic.

The project contains no employer, client, confidential facility, production-system, or restricted academic assessment data.

\## Current Limitations

Version 0.1 intentionally remains lightweight. It does not currently include:

\- Authentication or role-based access control

\- User assignment or technician scheduling

\- File or image attachments

\- Notifications or email escalation

\- Asset maintenance history

\- Pagination or advanced filtering

\- Production database configuration

\- Graphical management dashboard

SQLite is appropriate for this portfolio demonstration but would normally be replaced by a production-grade database for a larger multi-user deployment.

\## Future Development

Potential future milestones include:

\- Work-order filtering and search

\- Asset maintenance history

\- Technician assignment

\- SLA performance reporting

\- Mean time to repair metrics

\- Dashboard visualization

\- Authentication and authorization

\- PostgreSQL support

\- Containerization

\- Deployment configuration

\## Development Approach

This project was developed as a portfolio application combining facilities and infrastructure operations concepts with backend software engineering practices. AI-assisted development was used as part of the implementation workflow, with functionality validated through manual API testing and automated tests.

\## License

MIT License.
