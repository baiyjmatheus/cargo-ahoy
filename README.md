# Cargo Ahoy

### Requirements

- Postgres 13.1
- Python 3.8.6
- Flask 1.1.1

### Setting up

- Install dependencies
`pip install -r requirements.txt`

- In Postgres, run the following to create the databases:

```sql
create database cargoahoy;
create database cargoahoytest;
```

- Create a user on postgres with admin permissions
- On [./cargo-ahoy.sh](./cargo-ahoy.sh), replace `POSTGRES_USER` and `POSTGRES_PASSWORD` for the recently created user information from the previous step
- Add execution permission to `run-migrations.sh` and `cargo-ahoy.sh`
```shell script
chmod +x cargo-ahoy.sh run-migrations.sh
```
- Run scripts
`./cargo-ahoy.sh` and 
`./run-migrations.sh`

### Running application locally
To run the application locally execute one of the following: `flask run`
or `python main.py`

### Tests

To run the tests, simply execute: `pytest`

##### How tests were structured
- Api: Unit tests to verify if whether the api returns the correct response. Services are mocked and the json schemas are also tested.
- Core: Services methods are validated based on the database created records. Repostory layer behaviour is covered by the service's test as well.

### Endpoints

- Create a new vessel: `POST /api/vessels/`
```json
{
    "code": "MV102" [required]
}
```

- Get vessel by code: `GET /api/vessels/<vessel_code>`

- Create a new vessel equipment: `POST /api/vessels/<vessel_code>/equipments/`
```json
{
    "code": "MV103", [required]
    "name": "turbine", [required]
    "location": "BRAZIL", (enumerated EquipmentLocation)
    "status": "ACTIVE", (enumerated EquipmentStatus)
}
```

- Create a new vessel equipment: `POST /api/vessels/<vessel_code>/equipments/`
```json
{
    "code": "MV103", [required]
    "name": "turbine", [required]
    "location": "BRAZIL", (enumerated EquipmentLocation)
    "status": "ACTIVE", (enumerated EquipmentStatus)
}
```

- Get all active vessel equipments: `GET /api/vessels/<vessel_code>/equipments/`

- Inactivate vessel equipments: `PATCH /api/vessels/<vessel_code>/equipments/inactivate`
```json
{
    "codes": ["MV103", "MV102"], [required]
}
```
 