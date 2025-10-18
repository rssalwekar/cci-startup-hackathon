# Interview User Flow

## Visual Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    USER JOURNEY                              │
└─────────────────────────────────────────────────────────────┘

Step 1: User clicks "Start Interview" button
        ├── From Navbar (green button)
        ├── From Profile Page (hero section)
        └── From Interview List (banner/button)
                    ↓
                    ↓
Step 2: Redirect to /interviews/create/
        (interviews.views.create_interview_view)
                    ↓
                    ↓
Step 3: Redirect to /ai-interview/start/
        Shows: start_interview.html
        ┌─────────────────────────────────────┐
        │  🤖 AI Coding Interview             │
        │                                     │
        │  What you'll experience:            │
        │  ✓ Personalized problems            │
        │  ✓ Real-time AI guidance            │
        │  ✓ Interactive chat                 │
        │  ✓ Built-in code editor             │
        │  ✓ Comprehensive feedback           │
        │                                     │
        │   [Start Interview] (button)        │
        └─────────────────────────────────────┘
                    ↓
                    ↓ (User clicks button - POST request)
                    ↓
Step 4: Create InterviewSession
        (ai_interview.views.start_interview POST handler)
        - Creates session with status='preparing'
        - Assigns to current user
                    ↓
                    ↓
Step 5: Redirect to /ai-interview/interview/{session_id}/
        Shows: interview.html
        ┌─────────────────────────────────────┐
        │  AI Interview Session               │
        │  ┌──────────┐    ┌──────────┐      │
        │  │   Chat   │    │   Code   │      │
        │  │ Interface│    │  Editor  │      │
        │  │          │    │          │      │
        │  │  AI talks│    │  Write   │      │
        │  │  to user │    │  code    │      │
        │  └──────────┘    └──────────┘      │
        │                                     │
        │   [Complete Interview]              │
        └─────────────────────────────────────┘
                    ↓
                    ↓ (User completes interview)
                    ↓
Step 6: Complete Interview (POST to /ai-interview/complete/{session_id}/)
        - Generate AI feedback
        - Update session status to 'completed'
        - Create Interview record for history
        - Save scores and details
                    ↓
                    ↓
Step 7: Redirect to Profile (/profile/)
        - Shows success message with score
        - User sees updated interview history
        ┌─────────────────────────────────────┐
        │  ✓ Interview completed!             │
        │    Overall score: 85/100            │
        │                                     │
        │  [Start Interview] (Ready for next?)│
        │                                     │
        │  Recent Interviews:                 │
        │  • AI Interview - Practice (85/100)│
        │  • Previous interview...            │
        └─────────────────────────────────────┘
```

## Key Integration Points

### 1. Entry Points (All lead to start page)
- **Navbar**: `Start Interview` button → `/interviews/create/`
- **Profile**: Hero section button → `/interviews/create/`
- **Interview List**: Banner button → `/interviews/create/`

### 2. Routing Chain
```
/interviews/create/ 
  → (redirects) → 
/ai-interview/start/ 
  → (POST) → 
/ai-interview/interview/{id}/
  → (completes) →
/profile/ (with success message)
```

### 3. Data Flow
```
User → InterviewSession (ai_interview)
           ↓ (during interview)
     ChatMessage, CodeSubmission
           ↓ (on completion)
     Interview (interviews) ← for history tracking
```

## Files Modified

1. `interviews/views.py` - Redirect to start_interview
2. `ai_interview/views.py` - Create Interview on completion
3. `templates/base.html` - Green "Start Interview" in navbar
4. `templates/accounts/profile.html` - Hero section with button
5. `templates/interviews/interview_list.html` - Info banner with button

## Testing Checklist

- [ ] Click "Start Interview" from navbar
- [ ] Click "Start Interview" from profile page
- [ ] Click "Start Interview" from interview list
- [ ] All three redirect to start_interview.html
- [ ] Start page shows features and welcome message
- [ ] Clicking "Start Interview" button creates session
- [ ] Interview interface loads correctly
- [ ] Complete interview
- [ ] Verify redirected to profile page
- [ ] Check success message shows with score
- [ ] Verify interview appears in "Recent Interviews" section
- [ ] Check that all scores are saved correctly
