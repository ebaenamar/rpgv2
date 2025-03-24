# RPG Maestro Deployment Strategy

This document outlines the step-by-step process to test and deploy the RPG Maestro application, ensuring that all components work correctly both independently and together.

## 1. Local Testing

### 1.1 Backend Testing

```bash
# Build the Docker image
docker build -t rpg-maestro-api:latest .

# Run the Docker container
docker-compose -f docker-compose.test.yml up -d

# Test the API endpoints
python test_docker.py
```

Verify that all tests pass successfully, confirming that:
- The API is accessible
- The scene endpoint returns correct data
- The action endpoint processes player choices correctly
- The Maestro integration is working properly

### 1.2 Frontend Testing

```bash
# Navigate to the frontend directory
cd frontend

# Install dependencies
npm install

# Build the frontend
npm run build

# Start the development server
npm run dev
```

Verify that the frontend builds without errors and runs correctly at http://localhost:3000.

### 1.3 Integration Testing

```bash
# Run the integration test script
./test_integration.sh
```

Manually test the following scenarios:
1. Start a new game
2. View the game objectives
3. Make choices and verify that the scoring system works
4. Confirm that character responses are generated correctly
5. Test the audio playback functionality
6. Verify that scene transitions work properly

## 2. Deployment Preparation

### 2.1 Backend Deployment

1. Create a `.env.production` file with production environment variables
2. Update the Docker configuration for production if needed
3. Test the production Docker build locally

### 2.2 Frontend Deployment

1. Create a `.env.production` file with the production API URL
2. Build the frontend for production:

```bash
cd frontend
NEXT_PUBLIC_API_URL=https://your-production-api-url.com npm run build
```

3. Test the production build locally:

```bash
npm run start
```

## 3. Vercel Deployment

### 3.1 Deploy Backend API

1. Push the changes to GitHub:

```bash
git add .
git commit -m "chore: prepare for deployment"
git push
```

2. Set up a Docker-compatible hosting service (e.g., Heroku, DigitalOcean, AWS)
3. Configure environment variables on the hosting platform
4. Deploy the Docker container
5. Verify that the API is accessible and functioning correctly

### 3.2 Deploy Frontend to Vercel

1. Connect your GitHub repository to Vercel
2. Configure the build settings:
   - Build Command: `cd frontend && npm install && npm run build`
   - Output Directory: `frontend/.next`
3. Set the environment variables in the Vercel dashboard:
   - `NEXT_PUBLIC_API_URL`: URL of your deployed backend API
4. Trigger the deployment
5. Verify that the frontend is accessible and communicating with the backend

## 4. Post-Deployment Verification

1. Test all features in the production environment
2. Monitor error logs and performance
3. Verify that the Maestro integration works correctly in production
4. Test the scoring system and game objectives
5. Ensure that all media (images, audio) is loading correctly

## 5. Rollback Plan

If issues are encountered during deployment:

1. Identify the source of the problem
2. If frontend-related, roll back to the previous Vercel deployment
3. If backend-related, roll back to the previous Docker image
4. Fix the issues locally and repeat the deployment process

## 6. Maintenance and Updates

1. Regularly update dependencies
2. Monitor API usage and performance
3. Implement new features using the same testing and deployment process
4. Always test locally before deploying to production

By following this strategy, we ensure that all components of the RPG Maestro application work correctly both independently and together, providing a seamless experience for users.
