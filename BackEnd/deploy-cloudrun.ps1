# Deploy Backend to Google Cloud Run and Frontend to App Engine
#
# This script builds the Docker image for the backend, pushes it to Google Container Registry, and deploys it to Cloud Run.
# It also deploys the frontend to App Engine if specified.
#
# Usage:
#   powershell -ExecutionPolicy Bypass -File deploy-cloudrun.ps1 [backend|frontend|both]

param(
    [string]$Target = "both"
)

$ProjectId = "concrete-racer-442100-u7"
$Region = "us-west1"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $ScriptDir

if ($Target -eq "backend" -or $Target -eq "both") {
    $Tag = Get-Date -Format "yyyyMMddHHmmss"
    $ImageName = "gcr.io/$ProjectId/botstrap-backend:$Tag"

    Write-Host "[Backend] Building and submitting Docker image to GCR..."
    gcloud builds submit --tag $ImageName .

    Write-Host "[Backend] Deploying to Cloud Run..."
    gcloud run deploy botstrap-backend `
        --image $ImageName `
        --platform managed `
        --region $Region `
        --allow-unauthenticated

    Write-Host "[Backend] Deployment complete!"
}

if ($Target -eq "frontend" -or $Target -eq "both") {
    Write-Host "[Frontend] Deploying to App Engine..."
    Set-Location "$ScriptDir\.."  # Go to project root where app.yaml is
    gcloud app deploy app.yaml --quiet
    Set-Location $ScriptDir  # Return to script dir
    Write-Host "[Frontend] Deployment complete!"
}
