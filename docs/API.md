# API Documentation

## Base URL
```
http://localhost:8000
```

## Endpoints

### Root
- **GET** `/`
  - Returns API information

### Phases

#### List All Phases
- **GET** `/api/phases?skip=0&limit=100`
  - Query Parameters:
    - `skip` (optional): Number of records to skip
    - `limit` (optional): Maximum number of records to return
  - Returns: Array of Phase objects

#### Get Phase
- **GET** `/api/phases/{phase_id}`
  - Path Parameters:
    - `phase_id`: Phase ID
  - Returns: Phase object with topics

#### Create Phase
- **POST** `/api/phases`
  - Body: PhaseCreate object
  ```json
  {
    "title": "Phase Title",
    "goal": "Phase goal description",
    "progress": 0.0,
    "notes": "Optional notes",
    "order": 1,
    "xp": 0,
    "topics": []
  }
  ```
  - Returns: Created Phase object

#### Update Phase
- **PATCH** `/api/phases/{phase_id}`
  - Path Parameters:
    - `phase_id`: Phase ID
  - Body: PhaseUpdate object (all fields optional)
  ```json
  {
    "progress": 50.0,
    "xp": 100,
    "notes": "Updated notes"
  }
  ```
  - Returns: Updated Phase object

#### Delete Phase
- **DELETE** `/api/phases/{phase_id}`
  - Path Parameters:
    - `phase_id`: Phase ID
  - Returns: 204 No Content

### Statistics

#### Get Progress Stats
- **GET** `/api/stats`
  - Returns: ProgressStats object
  ```json
  {
    "total_phases": 10,
    "completed_phases": 2,
    "total_progress": 35.5,
    "total_xp": 1500,
    "phases_progress": []
  }
  ```

## Interactive API Documentation

FastAPI provides interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
