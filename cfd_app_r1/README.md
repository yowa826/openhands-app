# CFD App

## Local Execution

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
2. Activate the virtual environment:
   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   flask run
   ```

## Docker Execution

1. Build the Docker image:
   ```bash
   docker build -t cfd_app .
   ```
2. Run the Docker container:
   ```bash
   docker run -p 3000:3000 cfd_app
   ```

## Test Execution

To run the tests, use the following command:
```bash
NUMBA_DISABLE_JIT=1 pytest -q
```
This will execute the tests without JIT compilation for faster results.

## Frontend Features

- **Input Validation**: Real-time validation for grid size inputs with immediate feedback.
- **Progress Bar**: Displays computation progress and redirects to the result page upon completion.
- **Visualization**: Uses Plotly to display velocity vectors and pressure contours.
- **Download**: Provides a CSV download of the results.

## Typical Input Example

- Inflow velocity: 1.0 m/s
- Outflow pressure: 0 Pa
- Kinematic viscosity: 1e-3 m²/s
- Grid size: 50x50
- Steps: 5000

## API Specification

| Method | Path              | Description                      |
|--------|-------------------|----------------------------------|
| GET    | /                 | Display input form               |
| POST   | /run              | Register job and redirect        |
| GET    | /progress/<job_id>| Return progress percentage       |
| GET    | /result/<job_id>  | Display result page              |
| GET    | /download/<job_id>| Provide CSV download             |

## Known Issues / Future Roadmap

- Improve solver efficiency for larger grids.
- Enhance user interface for better usability.
- Implement additional boundary conditions.

## License

This project is licensed under the MIT License.