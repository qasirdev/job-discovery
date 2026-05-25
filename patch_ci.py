import yaml

with open('.github/workflows/ci.yml', 'r') as f:
    content = f.read()

# Add workflow_dispatch to the "on" block
if "workflow_dispatch:" not in content:
    content = content.replace("  pull_request:\n    branches: [\"main\"]\n", "  pull_request:\n    branches: [\"main\"]\n  workflow_dispatch:\n")

# Replace docker-build with docker-build-push
new_docker_job = """
  docker-build-push:
    name: Docker Build, Push & Sign
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    timeout-minutes: 20
    needs: [test-backend, test-frontend, prompt-regression-fast]
    permissions:
      contents: read
      packages: write
      id-token: write
    outputs:
      IMAGE_DIGEST: ${{ steps.build_push.outputs.digest }}
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Install cosign
        uses: sigstore/cosign-installer@v3.5.0
        
      - name: Log in to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
          
      - name: Log in to Azure Container Registry
        uses: docker/login-action@v3
        with:
          registry: acrjobdiscovery.azurecr.io
          username: ${{ secrets.ACR_USERNAME }}
          password: ${{ secrets.ACR_PASSWORD }}
          
      - name: Log in to Amazon ECR
        uses: docker/login-action@v3
        with:
          registry: public.ecr.aws/your-registry
          username: ${{ secrets.AWS_ACCESS_KEY_ID }}
          password: ${{ secrets.AWS_SECRET_ACCESS_KEY }}

      - name: Build and push image
        id: build_push
        uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: |
            ghcr.io/qasirmehmood/job-discovery:${{ github.sha }}
            ghcr.io/qasirmehmood/job-discovery:latest
            acrjobdiscovery.azurecr.io/job-discovery:${{ github.sha }}
            acrjobdiscovery.azurecr.io/job-discovery:latest
            public.ecr.aws/your-registry/job-discovery:${{ github.sha }}
            public.ecr.aws/your-registry/job-discovery:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Sign the published Docker image
        env:
          COSIGN_EXPERIMENTAL: "true"
        run: cosign sign --yes ghcr.io/qasirmehmood/job-discovery@${{ steps.build_push.outputs.digest }}

      - name: Verify image signature
        run: cosign verify --certificate-identity-regexp=.* --certificate-oidc-issuer=https://token.actions.githubusercontent.com ghcr.io/qasirmehmood/job-discovery@${{ steps.build_push.outputs.digest }}
"""

import re
content = re.sub(r"  docker-build:.*?(?=  trivy-scan:)", new_docker_job + "\n", content, flags=re.DOTALL)

# Update trivy-scan needs
content = content.replace("needs: docker-build", "needs: docker-build-push")

# Update prompt-regression-full and eval-regression-rag needs
content = content.replace("needs: docker-build", "needs: docker-build-push")

terraform_jobs = """
  terraform-validate:
    name: Terraform Validate & Plan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
        
      - name: Cache Azure Terraform
        uses: actions/cache@v4
        with:
          path: infrastructure/terraform/azure/.terraform
          key: ${{ runner.os }}-tf-azure-${{ hashFiles('infrastructure/terraform/azure/.terraform.lock.hcl') }}
          
      - name: Terraform Init Azure
        working-directory: infrastructure/terraform/azure
        run: terraform init -backend=false
        
      - name: Terraform Validate Azure
        working-directory: infrastructure/terraform/azure
        run: terraform validate
        
      - name: Cache AWS Terraform
        uses: actions/cache@v4
        with:
          path: infrastructure/terraform/aws/.terraform
          key: ${{ runner.os }}-tf-aws-${{ hashFiles('infrastructure/terraform/aws/.terraform.lock.hcl') }}

      - name: Terraform Init AWS
        working-directory: infrastructure/terraform/aws
        run: terraform init -backend=false
        
      - name: Terraform Validate AWS
        working-directory: infrastructure/terraform/aws
        run: terraform validate
        
      - name: Terraform Plan Azure
        if: github.event_name == 'push' && github.ref == 'refs/heads/main'
        working-directory: infrastructure/terraform/azure
        run: terraform plan -out=plan.tfplan
        
      - name: Upload Azure Plan
        if: github.event_name == 'push' && github.ref == 'refs/heads/main'
        uses: actions/upload-artifact@v4
        with:
          name: azure-tf-plan
          path: infrastructure/terraform/azure/plan.tfplan

      - name: Terraform Plan AWS
        if: github.event_name == 'push' && github.ref == 'refs/heads/main'
        working-directory: infrastructure/terraform/aws
        run: terraform plan -out=plan.tfplan
        
      - name: Upload AWS Plan
        if: github.event_name == 'push' && github.ref == 'refs/heads/main'
        uses: actions/upload-artifact@v4
        with:
          name: aws-tf-plan
          path: infrastructure/terraform/aws/plan.tfplan

  terraform-apply:
    name: Terraform Apply
    if: github.event_name == 'workflow_dispatch'
    runs-on: ubuntu-latest
    environment: production
    needs: [terraform-validate, docker-build-push]
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      
      - name: Download Azure Plan
        uses: actions/download-artifact@v4
        with:
          name: azure-tf-plan
          path: infrastructure/terraform/azure/
          
      - name: Terraform Apply Azure
        working-directory: infrastructure/terraform/azure
        run: |
          terraform init
          terraform apply -auto-approve plan.tfplan

      - name: Download AWS Plan
        uses: actions/download-artifact@v4
        with:
          name: aws-tf-plan
          path: infrastructure/terraform/aws/
          
      - name: Terraform Apply AWS
        working-directory: infrastructure/terraform/aws
        run: |
          terraform init
          terraform apply -auto-approve plan.tfplan
"""

content += "\n" + terraform_jobs

with open('.github/workflows/ci.yml', 'w') as f:
    f.write(content)
