# RowService
[![Backend tests]https://github.com/Leakplanting/RowService/blob/main/.github/workflows/test.yml/badge.svg
[![codecov](https://codecov.io/gh/Leakplanting/RowService/graph/badge.svg?token=RIO97WJHBP)](https://codecov.io/gh/Leakplanting/RowService)
A Flask-based microservice for managing row data.

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in `.env`:
```
MONGODB_CONN=your_mongodb_connection_string
PORT=5001
```

3. Run the service:
```bash
python api.py
```

## Docker

Build and run locally:
```bash
docker build -t row-service .
docker run -p 5001:5001 --env-file .env row-service
```

## Azure Deployment

This service is configured for deployment to Azure Container Apps using GitHub Actions.

### Prerequisites

1. Azure Container Registry (ACR)
2. Azure Container Apps environment
3. GitHub repository secrets:
   - `AZURE_CREDENTIALS`: Service principal credentials
   - `REGISTRY_USERNAME`: ACR username
   - `REGISTRY_PASSWORD`: ACR password
   - `MONGODB_CONN`: MongoDB connection string

### Deployment Process

1. Push to the main branch to trigger automatic deployment
2. Or manually trigger the workflow from GitHub Actions tab

For detailed setup instructions, see the [Azure deployment guide](docs/azure-deployment.md).
