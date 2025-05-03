# Bunq Hackathon Project

This repository contains a Next.js application with a frontend and backend setup, configured with Docker for both development and production environments.

## Project Structure

```
bunq-hackathon-6.0/
├── docker-compose.yml          # Docker Compose for local development
├── frontend/                   # Next.js frontend application
│   ├── Dockerfile              # Multi-stage Docker build for Next.js
│   └── ...                     # Next.js app files
└── backend/                    # Python backend
    ├── requirements.txt        # Python dependencies
    └── ...                     # Backend files
```

## Development Setup

### Prerequisites

- Docker and Docker Compose
- Node.js 20+ (optional, for local development without Docker)

### Running with Docker Compose

To start the entire application stack locally:

```bash
docker-compose up
```

This will start:
1. Frontend service on http://localhost:3000
2. PostgreSQL database on localhost:5432
3. MinIO (S3-compatible storage) with:
   - API on http://localhost:9000
   - Web console on http://localhost:9001 (login: minioadmin/minioadmin)

To run in detached mode:

```bash
docker-compose up -d
```

### Environment Variables

The following environment variables are set up in the docker-compose.yml:

#### Frontend
- `DATABASE_URL`: Connection string for PostgreSQL
- `BLOB_STORAGE_ENDPOINT`: MinIO endpoint for S3-compatible storage
- `BLOB_STORAGE_ACCESS_KEY`: MinIO access key
- `BLOB_STORAGE_SECRET_KEY`: MinIO secret key
- `BLOB_STORAGE_BUCKET`: MinIO bucket name

#### Database
- `POSTGRES_USER`: Database user
- `POSTGRES_PASSWORD`: Database password
- `POSTGRES_DB`: Database name

#### MinIO
- `MINIO_ROOT_USER`: MinIO root user
- `MINIO_ROOT_PASSWORD`: MinIO root password

## Production Deployment

The frontend Dockerfile is configured for production deployment with a multi-stage build process:

1. **deps**: Installs dependencies
2. **builder**: Builds the Next.js application
3. **runner**: Creates a minimal production image

### AWS Deployment Considerations

For production deployment on AWS:

1. **Frontend**: 
   - Deploy using AWS ECS/Fargate, Elastic Beanstalk, or App Runner
   - Configure with appropriate IAM roles

2. **Database**:
   - Replace PostgreSQL container with Amazon RDS or Aurora
   - Update the `DATABASE_URL` environment variable

3. **Blob Storage**:
   - Replace MinIO with Amazon S3
   - Update the S3 environment variables with AWS credentials or IAM roles
   - Set up proper CORS configuration for S3 buckets

### GitHub Actions CI/CD Workflow

This project includes a GitHub Actions workflow that automatically deploys the frontend to AWS when changes are merged to the `production` branch:

1. **Setup GitHub Secrets**:
   - `AWS_ACCESS_KEY_ID`: Your AWS access key
   - `AWS_SECRET_ACCESS_KEY`: Your AWS secret key
   - `AWS_REGION`: The AWS region (e.g., `us-east-1`)
   - `AWS_ECR_REPOSITORY`: The name of your ECR repository
   - `AWS_ECS_CLUSTER`: The name of your ECS cluster
   - `AWS_ECS_SERVICE`: The name of your ECS service

2. **Workflow Overview**:
   - The workflow builds the Docker container for the frontend using the Dockerfile in the frontend directory
   - Pushes the built image to Amazon ECR with two tags: latest and the commit SHA
   - Triggers a new deployment of your ECS service to use the new image

3. **Customizing the Workflow**:
   - The workflow is defined in `.github/workflows/aws-deploy.yml`
   - Adjust the deployment steps according to your specific AWS infrastructure

## Local Development (Without Docker)

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Backend

```bash
cd backend
pip install -r requirements.txt
python index.py
```

## Additional Information

- The frontend is a Next.js application using App Router
- Authentication is handled in the `(auth)` directory
- Chat functionality is in the `(chat)` directory
- The backend uses Python with Bunq API integration