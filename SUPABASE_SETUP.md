# Supabase Setup Guide

This guide will walk you through setting up Supabase for the MockInterview.AI platform.

## Prerequisites

- A Supabase account (free tier is sufficient)
- Basic understanding of databases and storage

## Step-by-Step Setup

### 1. Create a Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Sign in or create an account
3. Click **"New Project"**
4. Fill in the details:
   - **Project Name**: MockInterview-AI (or your preferred name)
   - **Database Password**: Choose a strong password (save this!)
   - **Region**: Choose the closest region to your users
   - **Pricing Plan**: Free (for development)
5. Click **"Create new project"**
6. Wait 2-3 minutes for the project to be provisioned

### 2. Get Your API Credentials

1. Once your project is ready, go to **Settings** (gear icon) → **API**
2. You'll see:
   - **Project URL**: Copy this (e.g., `https://xxxxxxxxxxxxx.supabase.co`)
   - **Project API keys**:
     - `anon public`: Copy this (for client-side operations)
     - `service_role`: Copy this (for admin operations, keep it secret!)

3. Add these to your `.env` file:
```env
SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
SUPABASE_KEY=your_anon_public_key_here
SUPABASE_SERVICE_KEY=your_service_role_key_here
```

### 3. Set Up Authentication

Supabase Auth is already configured by default. You can customize it:

1. Go to **Authentication** → **Providers**
2. **Email** provider should be enabled by default
3. Optional: Configure email templates
   - Go to **Authentication** → **Email Templates**
   - Customize the signup confirmation email
   - Customize the password reset email

#### Email Configuration (Optional)

For production, you should configure a custom SMTP server:

1. Go to **Settings** → **Auth**
2. Scroll to **SMTP Settings**
3. Configure your email provider (Gmail, SendGrid, etc.)
4. Test the connection

For development, Supabase's default email service works fine.

### 4. Create Storage Bucket for Recordings

1. Go to **Storage** in the left sidebar
2. Click **"New Bucket"**
3. Configure the bucket:
   - **Name**: `interview-recordings`
   - **Public bucket**: Toggle this based on your needs:
     - **ON** if you want recordings to be publicly accessible via URL
     - **OFF** if you want recordings to be private (recommended)
   - **File size limit**: Set to at least 50MB (for video recordings)
   - **Allowed MIME types**: Leave empty or add:
     - `audio/webm`
     - `audio/wav`
     - `audio/mp3`
     - `video/webm`
     - `video/mp4`

4. Click **"Create bucket"**

#### Set Up Storage Policies

For security, set up Row Level Security (RLS) policies:

1. Click on your `interview-recordings` bucket
2. Go to **Policies**
3. Click **"New Policy"**

**Policy 1: Allow users to upload their own recordings**
```sql
-- Policy name: Users can insert their own recordings
-- Allowed operation: INSERT
-- Target roles: authenticated

-- Check expression:
bucket_id = 'interview-recordings' 
AND (storage.foldername(name))[1] = auth.uid()::text
```

**Policy 2: Allow users to read their own recordings**
```sql
-- Policy name: Users can read their own recordings
-- Allowed operation: SELECT
-- Target roles: authenticated

-- Check expression:
bucket_id = 'interview-recordings' 
AND (storage.foldername(name))[1] = auth.uid()::text
```

**Policy 3: Allow users to delete their own recordings**
```sql
-- Policy name: Users can delete their own recordings
-- Allowed operation: DELETE
-- Target roles: authenticated

-- Check expression:
bucket_id = 'interview-recordings' 
AND (storage.foldername(name))[1] = auth.uid()::text
```

### 5. (Optional) Create Database Tables in Supabase

While Django manages its own database (SQLite in dev), you can also mirror data to Supabase PostgreSQL:

1. Go to **Database** → **Tables**
2. Click **"Create a new table"**

**Note**: For the hackathon, using Django's SQLite is sufficient. For production, you might want to use Supabase's PostgreSQL database.

To use Supabase PostgreSQL in Django:

1. Get your database connection string:
   - Go to **Settings** → **Database**
   - Copy the **Connection string** (Pooling mode)

2. Update your `.env`:
```env
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:6543/postgres
```

3. Install psycopg2:
```powershell
pip install psycopg2-binary
```

4. Update `settings.py`:
```python
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600
    )
}
```

### 6. Test Your Configuration

Run this test script to verify everything works:

```python
# test_supabase.py
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')

print(f"Testing Supabase connection...")
print(f"URL: {url}")

try:
    supabase = create_client(url, key)
    print("✓ Supabase client created successfully")
    
    # Test authentication
    result = supabase.auth.sign_up({
        "email": "test@example.com",
        "password": "testpassword123"
    })
    print("✓ Authentication works")
    
    # Test storage
    buckets = supabase.storage.list_buckets()
    print(f"✓ Storage accessible, found {len(buckets)} bucket(s)")
    
    print("\n✓ All tests passed!")
    
except Exception as e:
    print(f"✗ Error: {e}")
```

Run it:
```powershell
python test_supabase.py
```

### 7. Security Best Practices

1. **Never commit your `.env` file** to Git
2. **Keep your service_role key secret** - only use it server-side
3. **Use RLS policies** to secure your storage and database
4. **Enable email confirmation** for new signups in production
5. **Set up rate limiting** in Supabase dashboard
6. **Monitor usage** in the Supabase dashboard to avoid quota limits

### 8. Monitoring and Maintenance

#### Check Usage
1. Go to **Settings** → **Usage**
2. Monitor:
   - Database size
   - Storage size
   - Bandwidth usage
   - Monthly Active Users (MAU)

#### View Logs
1. Go to **Logs**
2. Select log type:
   - **API Logs**: HTTP requests
   - **Auth Logs**: Authentication events
   - **Storage Logs**: File operations

#### Database Backups (Production)
1. Go to **Settings** → **Database**
2. Set up automated backups (available on Pro plan)
3. For free tier, manually export your database periodically

## Troubleshooting

### Issue: "Invalid API key"
- **Solution**: Double-check your `.env` file has the correct keys
- Make sure you're using `anon public` key, not the `service_role` key for client operations

### Issue: "CORS error"
- **Solution**: Add your domain to allowed origins
- Go to **Settings** → **API** → **API Settings**
- Add `http://localhost:8000` to **Site URL**

### Issue: Storage upload fails
- **Solution**: Check RLS policies
- Verify the bucket name is correct (`interview-recordings`)
- Check file size limits

### Issue: Authentication not working
- **Solution**: Verify email templates are configured
- Check if email confirmation is required
- Look at Auth logs for error details

## Free Tier Limits

Supabase free tier includes:
- **Database**: 500 MB
- **Storage**: 1 GB
- **Bandwidth**: 2 GB
- **Monthly Active Users**: Unlimited
- **API Requests**: Unlimited

For the hackathon, these limits should be more than sufficient!

## Additional Resources

- [Supabase Documentation](https://supabase.com/docs)
- [Supabase Auth Guide](https://supabase.com/docs/guides/auth)
- [Supabase Storage Guide](https://supabase.com/docs/guides/storage)
- [Python Client Documentation](https://supabase.com/docs/reference/python/introduction)

## Support

If you encounter issues:
1. Check the [Supabase Community](https://github.com/supabase/supabase/discussions)
2. Review the [troubleshooting guide](https://supabase.com/docs/guides/platform/troubleshooting)
3. Contact your team's backend developer

---

After completing this setup, your Supabase backend will be ready for the MockInterview.AI platform!
