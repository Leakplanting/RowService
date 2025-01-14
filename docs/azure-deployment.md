# Azure Deployment Guide

This guide provides step-by-step instructions for setting up Azure resources and GitHub Actions for deploying the RowService.

## 1. Azure CLI Setup

1. Install Azure CLI:
   ```bash
   brew install azure-cli   # For macOS
   ```

2. Login to Azure:
   ```bash
   az login
   ```

## 2. Create Azure Resources

1. Create a Resource Group:
   ```bash
   az group create --name your-resource-group --location westeurope
   ```

2. Create Azure Container Registry:
   ```bash
   az acr create \
     --resource-group your-resource-group \
     --name your-registry-name \
     --sku Basic
   ```

3. Create Container Apps Environment:
   ```bash
   az containerapp env create \
     --name production \
     --resource-group your-resource-group \
     --location westeurope
   ```

## 3. Set Up Service Principal

1. Get your subscription ID:
   ```bash
   az account show --query id -o tsv
   ```

2. Create a service principal with Contributor access:
   ```bash
   az ad sp create-for-rbac \
     --name "row-service-github" \
     --role contributor \
     --scopes /subscriptions/{subscription-id}/resourceGroups/{resource-group} \
     --sdk-auth
   ```

3. Save the JSON output - you'll need it for GitHub secrets.

## 4. Configure GitHub Secrets

Add the following secrets in your GitHub repository (Settings → Secrets and variables → Actions):

1. `AZURE_CREDENTIALS`: Entire JSON output from service principal creation
2. `REGISTRY_USERNAME`: Get from Azure Portal → Container Registry → Access keys
3. `REGISTRY_PASSWORD`: Get from Azure Portal → Container Registry → Access keys
4. `MONGODB_CONN`: Your MongoDB connection string

## 5. Update Workflow File

In `.github/workflows/azure-deploy.yml`, update these environment variables:

```yaml
env:
  AZURE_CONTAINER_REGISTRY: "your-registry-name"  # Your ACR name
  RESOURCE_GROUP: "your-resource-group"           # Your resource group
  CONTAINER_APP_NAME: "row-service-app"          # Desired app name
  CONTAINER_APP_ENVIRONMENT: "production"         # Environment name
```

## 6. Deploy

1. Push your changes to the main branch:
   ```bash
   git add .
   git commit -m "Configure Azure deployment"
   git push origin main
   ```

2. Monitor the deployment:
   - Go to GitHub repository → Actions tab
   - Click on the running workflow to see details

## 7. Verify Deployment

1. Get the application URL:
   ```bash
   az containerapp show \
     --name row-service-app \
     --resource-group your-resource-group \
     --query properties.configuration.ingress.fqdn \
     --output tsv
   ```

2. Test the endpoint:
   ```bash
   curl https://{your-app-url}/fields
   ```

## Troubleshooting

1. Check application logs:
   ```bash
   az containerapp logs show \
     --name row-service-app \
     --resource-group your-resource-group \
     --follow
   ```

2. Review environment variables:
   ```bash
   az containerapp show \
     --name row-service-app \
     --resource-group your-resource-group \
     --query properties.configuration.secrets
   ```
