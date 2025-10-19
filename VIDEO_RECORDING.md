# Video Recording Feature

This document explains the video recording functionality implemented for the AI coding interview platform.

## Overview

The video recording feature allows users to record their entire interview session, including screen capture and audio, which is then displayed on the results page.

## How It Works

### 1. **Browser-Based Recording**
- Uses the **MediaRecorder API** with **getDisplayMedia()** for screen capture
- Records both video (screen) and audio (microphone)
- Supports multiple video codecs with fallback options:
  - Primary: `video/webm;codecs=vp9,opus`
  - Fallback: `video/webm;codecs=vp8,opus`
  - Final fallback: `video/webm`

### 2. **Recording Process**
1. **Start Recording**: User clicks "🎥 Start Recording" button
2. **Permission Request**: Browser asks for screen sharing permission
3. **Stream Setup**: Creates MediaRecorder with optimal settings:
   - Video: 1920x1080 @ 30fps, 2.5 Mbps
   - Audio: 44.1kHz, 128 kbps with noise suppression
4. **Data Collection**: Records data in 1-second chunks
5. **Stop Recording**: User clicks "⏹️ Stop Recording" or ends interview
6. **Upload**: Video is automatically uploaded to the server

### 3. **File Storage**
- Videos are stored in Django's `media/interview_recordings/` directory
- Filename format: `interview_{timestamp}.webm`
- Database tracks the recording metadata in `InterviewRecording` model

### 4. **Results Page Display**
- Videos are displayed in the results page using HTML5 `<video>` element
- Supports both WebM and MP4 formats for maximum browser compatibility
- Includes video controls (play, pause, seek, volume, fullscreen)

## Technical Implementation

### Frontend (JavaScript)
```javascript
// Start recording
async function startVideoRecording() {
    recordingStream = await navigator.mediaDevices.getDisplayMedia({
        video: { mediaSource: 'screen', width: { ideal: 1920 }, height: { ideal: 1080 } },
        audio: { echoCancellation: true, noiseSuppression: true }
    });
    
    mediaRecorder = new MediaRecorder(recordingStream, options);
    mediaRecorder.start(1000); // 1-second chunks
}

// Stop and upload
async function stopVideoRecording() {
    mediaRecorder.stop();
    const blob = new Blob(recordedChunks, { type: 'video/webm' });
    await uploadVideoToServer(blob);
}
```

### Backend (Django)
```python
@login_required
def upload_video(request):
    video_file = request.FILES['video']
    recording, created = InterviewRecording.objects.get_or_create(session=session)
    recording.video_file = video_file
    recording.save()
    return JsonResponse({'success': True, 'video_url': recording.video_file.url})
```

## User Experience

### Starting a Recording
1. Click "🎥 Start Recording" button during interview
2. Browser prompts for screen sharing permission
3. Choose what to share (entire screen, window, or tab)
4. Recording begins automatically
5. Button changes to "⏹️ Stop Recording" with pulsing animation

### During Recording
- Button shows red pulsing animation to indicate active recording
- User can continue with interview normally
- If user stops screen sharing, recording automatically stops

### Ending Recording
- Click "⏹️ Stop Recording" button, OR
- Click "End Interview" (automatically stops recording)
- Video is processed and uploaded to server
- User is redirected to results page where video is displayed

## Browser Compatibility

### Supported Browsers
- **Chrome/Chromium**: Full support
- **Firefox**: Full support
- **Safari**: Limited support (may require different codec)
- **Edge**: Full support

### Requirements
- HTTPS connection (required for screen capture API)
- Modern browser with MediaRecorder API support
- User permission for screen sharing

## File Sizes and Performance

### Typical File Sizes
- **1 minute recording**: ~15-20 MB
- **10 minute interview**: ~150-200 MB
- **30 minute interview**: ~450-600 MB

### Optimization Features
- Efficient WebM codec with VP9/VP8 compression
- Adaptive bitrate based on content
- Chunked recording to prevent memory issues
- Automatic cleanup of temporary data

## Security and Privacy

### Data Handling
- Videos are stored locally on the server
- Only accessible to the user who created the recording
- No third-party video processing services used
- Videos can be deleted by removing the session

### Permissions
- Users must explicitly grant screen sharing permission
- Recording only starts after user confirmation
- Users can stop recording at any time
- No automatic recording without user action

## Troubleshooting

### Common Issues
1. **"Failed to start screen recording"**
   - Ensure HTTPS connection
   - Check browser permissions
   - Try refreshing the page

2. **"No video file provided"**
   - Recording may have failed silently
   - Check browser console for errors
   - Try starting recording again

3. **"Video not displaying"**
   - Check if video file exists in media directory
   - Verify browser supports WebM format
   - Check Django media settings

### Browser Console Messages
- `"Video recording started"` - Recording began successfully
- `"Video blob created, size: X bytes"` - Video processed
- `"Video uploaded successfully"` - Upload completed
- `"Screen sharing ended by user"` - User stopped sharing

## Future Enhancements

### Potential Improvements
1. **Compression**: Add server-side video compression
2. **Streaming**: Implement real-time video streaming
3. **Analytics**: Add video analytics and insights
4. **Cloud Storage**: Integrate with cloud storage services
5. **Transcription**: Add automatic speech-to-text from video audio
6. **Thumbnails**: Generate video thumbnails for quick preview

### Performance Optimizations
1. **Progressive Upload**: Upload video chunks during recording
2. **Background Processing**: Process videos in background tasks
3. **CDN Integration**: Serve videos through content delivery network
4. **Mobile Support**: Optimize for mobile screen recording
