# API Integration Guide

This document explains how to integrate the AI interview system with the Django backend.

## Base URL

```
http://localhost:8000
```

## Authentication

All interview-related endpoints require authentication. Users must be logged in.

### Authentication Flow

1. User signs up: `POST /signup/`
2. User logs in: `POST /login/`
3. Session cookie is set automatically
4. All subsequent requests include the session cookie

## Creating an Interview

### Endpoint
```
POST /interviews/create/
```

### Request Body
```json
{
    "title": "Mock Interview Session",
    "problem_name": "Two Sum",
    "problem_description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
    "difficulty": "easy",
    "language": "python"
}
```

### Response
Redirects to interview detail page with the created interview ID.

## Updating Interview Data

### Endpoint
```
POST /interviews/<interview_id>/save-data/
```

### Request Headers
```
Content-Type: application/json
X-CSRFToken: <csrf_token>
```

### Full Request Body Example
```json
{
    "status": "completed",
    "code": "def twoSum(nums, target):\n    hashmap = {}\n    for i, num in enumerate(nums):\n        complement = target - num\n        if complement in hashmap:\n            return [hashmap[complement], i]\n        hashmap[num] = i",
    "transcript": "AI: Hello! Let's start the interview. Can you explain the Two Sum problem?\nUser: Sure, we need to find two numbers that add up to a target...\n[Full conversation transcript]",
    "scores": {
        "overall": 85,
        "communication": 90,
        "problem_solving": 82,
        "code_quality": 83
    },
    "feedback_report": "Overall Performance:\n\nYou demonstrated strong problem-solving skills and excellent communication throughout the interview. Your approach to the Two Sum problem was methodical and well-explained.\n\nKey Observations:\n- Clearly articulated your thought process\n- Asked relevant clarifying questions\n- Wrote clean, readable code\n- Considered time and space complexity\n\nAreas noted for improvement are detailed below.",
    "strengths": "- Excellent verbal communication\n- Clear explanation of approach before coding\n- Good use of hash map for optimization\n- Proper variable naming\n- Considered edge cases",
    "areas_for_improvement": "- Could have discussed edge cases earlier\n- Spent slightly too much time on initial brute force approach\n- Could improve on analyzing time complexity upfront",
    "feedback_points": [
        {
            "category": "communication",
            "is_positive": true,
            "point": "Clearly explained your approach before starting to code"
        },
        {
            "category": "communication",
            "is_positive": true,
            "point": "Asked clarifying questions about input constraints"
        },
        {
            "category": "problem_solving",
            "is_positive": true,
            "point": "Recognized the optimization opportunity with hash map"
        },
        {
            "category": "problem_solving",
            "is_positive": false,
            "point": "Could have identified the optimal approach sooner"
        },
        {
            "category": "code_quality",
            "is_positive": true,
            "point": "Used descriptive variable names like 'complement' and 'hashmap'"
        },
        {
            "category": "code_quality",
            "is_positive": true,
            "point": "Code was clean and easy to read"
        },
        {
            "category": "testing",
            "is_positive": false,
            "point": "Did not walk through test cases before submitting"
        },
        {
            "category": "time_management",
            "is_positive": true,
            "point": "Completed the problem within the allocated time"
        }
    ],
    "notes": [
        {
            "content": "User asked about whether the array is sorted",
            "type": "question_asked",
            "timestamp": "2025-01-15T10:30:15Z"
        },
        {
            "content": "User initially suggested brute force O(n²) approach",
            "type": "observation",
            "timestamp": "2025-01-15T10:31:30Z"
        },
        {
            "content": "AI provided hint about using a hash map",
            "type": "hint_given",
            "timestamp": "2025-01-15T10:35:00Z"
        },
        {
            "content": "User optimized solution to O(n) time complexity",
            "type": "code_change",
            "timestamp": "2025-01-15T10:38:20Z"
        }
    ]
}
```

### Response
```json
{
    "success": true,
    "message": "Interview data saved successfully"
}
```

## Uploading Recording

### Endpoint
```
POST /interviews/<interview_id>/upload-recording/
```

### Request
```
Content-Type: multipart/form-data

recording: <file>
```

### Python Example
```python
import requests

url = "http://localhost:8000/interviews/1/upload-recording/"
files = {'recording': open('interview_recording.webm', 'rb')}

response = requests.post(url, files=files)
print(response.json())
```

### Response
```json
{
    "success": true,
    "url": "https://your-supabase-url.supabase.co/storage/v1/object/public/interview-recordings/...",
    "message": "Recording uploaded successfully"
}
```

## Data Models

### Interview Status Options
- `scheduled`: Interview is scheduled but not started
- `in_progress`: Interview is currently ongoing
- `completed`: Interview has been finished
- `cancelled`: Interview was cancelled

### Difficulty Options
- `easy`
- `medium`
- `hard`

### Feedback Categories
- `communication`: How well the candidate communicates
- `problem_solving`: Problem-solving approach and logic
- `code_quality`: Code cleanliness, readability, and best practices
- `testing`: Testing approach and edge case consideration
- `time_management`: How well time was managed during the interview
- `clarification`: How well the candidate asked clarifying questions

### Note Types
- `observation`: General observation about the interview
- `hint_given`: AI provided a hint
- `question_asked`: Candidate asked a question
- `code_change`: Significant code change was made

## Example Integration Flow

### 1. User Starts Interview
```python
# Frontend creates interview
interview_data = {
    "title": "Practice Session",
    "problem_name": "Valid Parentheses",
    "problem_description": "Given a string containing just...",
    "difficulty": "medium",
    "language": "python"
}

# Interview is created, get interview_id
interview_id = created_interview.id
```

### 2. During Interview
```python
# Periodically save progress
progress_data = {
    "status": "in_progress",
    "code": current_code,
    "transcript": current_transcript
}

requests.post(f"/interviews/{interview_id}/save-data/", json=progress_data)
```

### 3. After Interview
```python
# Save final data
final_data = {
    "status": "completed",
    "code": final_code,
    "transcript": full_transcript,
    "scores": calculated_scores,
    "feedback_report": generated_report,
    "strengths": identified_strengths,
    "areas_for_improvement": identified_improvements,
    "feedback_points": detailed_feedback,
    "notes": interview_notes
}

requests.post(f"/interviews/{interview_id}/save-data/", json=final_data)

# Upload recording
files = {'recording': recording_file}
requests.post(f"/interviews/{interview_id}/upload-recording/", files=files)
```

## Error Handling

### Common Error Responses

#### 404 Not Found
```json
{
    "error": "Interview not found"
}
```

#### 403 Forbidden
```json
{
    "error": "You don't have permission to access this interview"
}
```

#### 400 Bad Request
```json
{
    "error": "Invalid data format"
}
```

#### 500 Internal Server Error
```json
{
    "error": "An error occurred: <error details>"
}
```

## Best Practices

1. **Always update status**: Update the interview status as it progresses
2. **Save incrementally**: Save interview data periodically, not just at the end
3. **Handle errors**: Always check response status and handle errors gracefully
4. **Upload recordings last**: Upload the recording after all other data is saved
5. **Use timestamps**: Include accurate timestamps for notes
6. **Categorize feedback**: Organize feedback points by category for better display
7. **Validate data**: Ensure scores are between 0-100 and status values are valid

## Testing

### Using curl (Windows PowerShell)

```powershell
# Create interview
$body = @{
    title = "Test Interview"
    problem_name = "Test Problem"
    problem_description = "Test Description"
    difficulty = "medium"
    language = "python"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/interviews/create/" `
    -Method POST `
    -Body $body `
    -ContentType "application/json" `
    -SessionVariable session

# Save data
$updateBody = @{
    status = "completed"
    code = "def solution(): pass"
    scores = @{
        overall = 85
        communication = 90
    }
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/interviews/1/save-data/" `
    -Method POST `
    -Body $updateBody `
    -ContentType "application/json" `
    -WebSession $session
```

## Support

For integration issues or questions, contact the backend team or refer to the main README.md file.
