# GitHub Actions Deployment Setup

## Required GitHub Secrets

To enable the automated deployment workflow, you need to configure the following secrets in your GitHub repository:

### Navigation
Go to: **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

### Required Secrets

1. **`ENV`**
   - **Description**: Complete contents of your `.env` file
   - **Value**: Copy the entire contents of your local `src/.env` file
   - **Usage**: Creates the `.env` file inside the Docker container during build

2. **`ACR_USERNAME`**
   - **Description**: Azure Container Registry username
   - **Value**: Your ACR registry name (typically the same as the registry name, e.g., `scsyfyid2bvkqcosureg`)
   - **How to get**: Run `az acr credential show --name scsyfyid2bvkqcosureg --query username -o tsv`

3. **`ACR_PASSWORD`**
   - **Description**: Azure Container Registry password
   - **Value**: Your ACR admin password
   - **How to get**: Run `az acr credential show --name scsyfyid2bvkqcosureg --query passwords[0].value -o tsv`

## Workflow Triggers

The deployment workflow runs automatically when:
- Code is pushed to the `main` branch
- Changes are made to files in the `src/` directory
- Manually triggered via the "Actions" tab (workflow_dispatch)

## What the Workflow Does

1. Checks out your code
2. Authenticates with Azure Container Registry
3. Creates a temporary `.env` file from the `ENV` secret
4. Builds the Docker image from the `src/` directory
5. Tags the image with both `latest` and the git commit SHA
6. Pushes both tags to ACR
7. Cleans up the temporary `.env` file

## Security Notes

- The `.env` file is **never** committed to the repository (it's in `.gitignore`)
- The `.env` file is created temporarily during the build and immediately deleted
- All secrets are stored securely in GitHub Secrets
- Docker build logs may show package installations but will not expose secret values

## Testing the Workflow

After setting up the secrets, you can test the workflow by:
1. Making a small change to a file in `src/`
2. Committing and pushing to the `main` branch
3. Checking the "Actions" tab in GitHub to monitor the workflow execution

## Restart App Service After Deployment

After the workflow completes, restart your Azure App Service to pull the new image:

```bash
az webapp restart --name scsyfyid2bvkq-app --resource-group techworkshop-l300-ai-agents
```

Or configure continuous deployment in Azure App Service to automatically pull and restart when a new image is pushed to ACR.
