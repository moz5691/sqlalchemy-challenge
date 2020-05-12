## HW-10 SQLAlchemy

### Climate Analysis and Exploration

#### Precipitation Analysis

#### Station Analysis

### Flask APIs

#### Routes

- `/`

  - Home page.
  - List all routes that are available.

- `/api/v1.0/precipitation`

  - Return the JSON representation of your dictionary.

- `/api/v1.0/stations`

  - Return a JSON list of stations from the dataset.

- `/api/v1.0/tobs`

  - Return a JSON list of Temperature Observations (tobs) for the previous year.

- `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`
  - Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
