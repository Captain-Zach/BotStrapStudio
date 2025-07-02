# Deploy Backend to Google Cloud Run
#
# This script builds the Docker image, pushes it to Google Container Registry, and deploys it to Cloud Run.
#
# Usage: powershell -ExecutionPolicy Bypass -File deploy-cloudrun.ps1

$ProjectId = "concrete-racer-442100-u7"
$Region = "us-west1"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $ScriptDir

$Tag = Get-Date -Format "yyyyMMddHHmmss"
$ImageName = "gcr.io/$ProjectId/botstrap-backend:$Tag"

Write-Host "Building and submitting Docker image to GCR..."
gcloud builds submit --tag $ImageName .

Write-Host "Deploying to Cloud Run..."
gcloud run deploy botstrap-backend `
    --image $ImageName `
    --platform managed `
    --region $Region `
    --allow-unauthenticated

Write-Host "Deployment complete!"
