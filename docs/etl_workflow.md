## ETL Workflow

### Extract
- Fetch real-time data using OpenWeatherMap API
- Handle API errors and timeouts

### Transform
- Convert units to metric
- Handle missing rainfall data
- Normalize weather conditions

### Load
- Insert data into SQLite tables
- Maintain referential integrity
- Prevent duplicates
