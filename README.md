# Scam master

Bank transfer system.
Bank transfer service written in `Python 3.10.11`. Uses the pyppeteer and selenium library to make card-to-card transfers through bank websites. The translation is initialized through the API interface, the translation status is returned through the Kafka broker.

------------

## Run the application
```bash
# Creating a virtual environment
> python -m venv venv
# Activating the virtual environment
> ./venv/Scripts/activate
# Installing dependencies
> pip install -r ./requirements.txt
# Run the application
> uvicorn main:app --host 0.0.0.0 --port 80
```
------------
## OpenAPI
The openAPI specification can be viewed by following the path `host:port/api/v1/openapi`

------------
## Supported banks
- Issuers (senders):
	- Sber Bank
	- Tinkoff
- Acquirers (gateways):
	- Tinkoff
	- Otp Bank
	- Russian Agricultural Bank

------------
## Kafka
The transfer results are returned via Kafka:
- Topic name: `transactions.status.changed`
- Statuses:
	- `in_progress` - transfer is awaiting confirmation
	- `confirmed` - confirmation was successful
	- `failed` - something went wrong
- Message json scheme:
```json
{
	"type": "object",
	"properties": {
		"id": {
			"type": "string"
		},
		"status": {
			"type": "string",
			"enum": ["in_progress", "confirmed", "failed"]
		}
	},
	"required": ["id", "status"]
}
```

------------
## Configuration
Configuration parameters are taken from an `.env` file similar to the `.env.sample` file. The `.env.sample` file must be copied and renamed to `.env`.
- `LOG_DIR` - directory for saving logs. If not specified, the logs will not be saved to a file
- `LOG_RETENTION` - maximum number of saved log files. Once exceeded, old files will be erased
- `LOG_ROTATION` - maximum size in megabytes of one log file. If exceeded, a new file will be created, the old one will be zipped
- `BROWSER_PATH` - path to the browser executable file. If not specified, the standard pyppeteer browser will be used
