# Deployment Guide for Tech Trades

This guide will walk you through deploying your Tech Trades application to Vercel.

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Git Repository**: Your code should be in a Git repository (GitHub, GitLab, or Bitbucket)
3. **Vercel CLI** (optional): Install with `npm i -g vercel`

## Project Structure for Vercel

Your project has been configured with the following structure for Vercel deployment:

```
TechTransferAnnouncement/
├── api/
│   ├── index.py          # Serverless Flask API
│   └── companies.json    # Company data
├── frontend/
│   ├── src/             # React source code
│   ├── dist/            # Build output (auto-generated)
│   └── package.json     # Frontend dependencies
├── vercel.json          # Vercel configuration
└── requirements.txt     # Python dependencies
```

## Deployment Steps

### Method 1: Deploy via Vercel Dashboard (Recommended)

1. **Connect Repository**
   - Go to [vercel.com/dashboard](https://vercel.com/dashboard)
   - Click "New Project"
   - Import your Git repository
   - Select your repository and click "Import"

2. **Configure Project**
   - **Framework Preset**: Vercel should auto-detect "Other" or "Vite"
   - **Root Directory**: Leave as `.` (root)
   - **Build Command**: `cd frontend && npm run build`
   - **Output Directory**: `frontend/dist`
   - **Install Command**: `cd frontend && npm install`

3. **Deploy**
   - Click "Deploy"
   - Wait for build to complete
   - Your app will be live at `https://your-project-name.vercel.app`

### Method 2: Deploy via Vercel CLI

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy from Project Root**
   ```bash
   vercel
   ```

4. **Follow Prompts**
   - Set up and deploy: `Y`
   - Which scope: Select your team/personal account
   - Link to existing project: `N` (for first deployment)
   - Project name: `tech-trades` (or your preferred name)
   - In which directory: `.` (current directory)

## Environment Variables

The application uses external APIs that might require environment variables in production:

### Optional Environment Variables

You can set these in the Vercel dashboard under Project Settings > Environment Variables:

- `CLEARBIT_API_KEY` - For company logo fetching (optional, uses free tier by default)
- `CUSTOM_FONTS_URL` - Custom font CDN (optional, uses Google Fonts by default)

## API Endpoints

After deployment, your API endpoints will be available at:

- `https://your-domain.vercel.app/api/companies` - Get company list
- `https://your-domain.vercel.app/api/generate-flyer` - Generate flyer
- `https://your-domain.vercel.app/api/health` - Health check

## Custom Domain (Optional)

1. Go to your project dashboard on Vercel
2. Click "Settings" → "Domains"
3. Add your custom domain
4. Update your DNS records as instructed
5. Update `vercel.json` and `index.html` with your domain

## Troubleshooting

### Common Issues

1. **Build Fails - "Command failed"**
   - Check that `frontend/package.json` has correct build script
   - Ensure all dependencies are listed in `package.json`

2. **API Routes Don't Work**
   - Verify `api/index.py` is present
   - Check `requirements.txt` has all Python dependencies
   - Ensure `vercel.json` routes are correct

3. **Companies Not Loading**
   - Verify `api/companies.json` exists
   - Check browser console for API errors

4. **Fonts Not Loading**
   - Fonts are downloaded dynamically from Google Fonts
   - Check network connectivity in serverless environment

5. **Image Generation Fails**
   - Verify all Python dependencies are installed
   - Check Vercel function logs for errors

### Debugging

1. **Check Vercel Function Logs**
   ```bash
   vercel logs https://your-project-name.vercel.app
   ```

2. **Local Testing**
   ```bash
   # Test frontend locally
   cd frontend
   npm run dev
   
   # Test API locally
   cd api
   python index.py
   ```

3. **Build Preview**
   ```bash
   cd frontend
   npm run build
   npm run preview
   ```

## Performance Optimization

Your deployment includes several optimizations:

1. **Code Splitting**: React components are automatically chunked
2. **Asset Optimization**: Images and fonts are optimized
3. **CDN**: Vercel's global CDN serves your assets
4. **Serverless Functions**: API scales automatically with demand

## Security Considerations

1. **CORS**: Properly configured for your domain
2. **File Uploads**: Temporary files are handled securely
3. **API Rate Limiting**: Consider implementing rate limiting for production

## Monitoring

1. **Vercel Analytics**: Available in your dashboard
2. **Function Metrics**: Monitor API performance
3. **Error Tracking**: Set up error monitoring service

## Next Steps

1. **Set up monitoring** with services like Sentry or LogRocket
2. **Configure analytics** with Google Analytics or Vercel Analytics
3. **Set up CI/CD** for automated deployments
4. **Add tests** for both frontend and backend
5. **Consider database** for user data if needed

## Support

- **Vercel Docs**: [vercel.com/docs](https://vercel.com/docs)
- **Community**: [vercel.com/community](https://vercel.com/community)
- **GitHub Issues**: Create issues in your repository for project-specific problems

---

Your Tech Trades application should now be successfully deployed to Vercel! 🚀 