# Voice Setup Guide

## ElevenLabs API Setup

To enable natural voice synthesis for the AI interview agent, you need to set up an ElevenLabs API key.

### 1. Get ElevenLabs API Key

1. Go to [ElevenLabs](https://elevenlabs.io/)
2. Sign up for a free account
3. Navigate to your profile settings
4. Copy your API key

### 2. Set Environment Variable

Add your ElevenLabs API key to your environment:

```bash
export ELEVENLABS_API_KEY="your-api-key-here"
```

Or add it to your `.env` file:
```
ELEVENLABS_API_KEY=your-api-key-here
```

### 3. Features

With ElevenLabs integration, you get:

- **Natural Voice Synthesis**: AI responses sound human-like instead of robotic
- **High Quality Audio**: Professional-grade voice generation
- **Multiple Voice Options**: Choose from various natural-sounding voices
- **Fallback Support**: Falls back to browser's built-in speech synthesis if ElevenLabs is unavailable

### 4. Usage

- **Continuous Listening**: 🎯 button enables natural speech interaction (like OpenAI's speech model)
- **Auto-speak**: AI responses are automatically spoken when received
- **Manual Control**: Click the 🔊 button to replay the last AI message
- **Re-speak Last Message**: Click the 🔁 button to replay the last AI message (saves API calls!)
- **Voice Input**: Use the 🎤 button for one-time speech-to-text input
- **Character Counter**: Shows current usage vs. free tier limit (10,000 chars)

### 5. Character Optimization

The system is optimized to minimize character usage:

- **Concise AI Responses**: AI responses are limited to 2-3 sentences
- **Text Cleaning**: Removes unnecessary words and phrases before speech synthesis
- **Audio Caching**: Reuses generated audio for identical text (saves API calls!)
- **Re-speak Feature**: 🔁 button replays last AI message without new API calls
- **Continuous Listening**: Natural speech interaction without button clicks
- **Smart Fallback**: Uses browser TTS if ElevenLabs is unavailable
- **Usage Tracking**: Real-time character counter with warning indicators

### 6. Free Tier Limits

ElevenLabs free tier includes:
- 10,000 characters per month
- Access to standard voices
- Basic voice settings

**Character Counter Colors:**
- Gray: Normal usage (< 60%)
- Orange: Warning (60-80%)
- Red: Critical (80%+)

For production use, consider upgrading to a paid plan for higher limits and premium voices.

### 7. Troubleshooting

If voice features aren't working:

1. **Microphone Access**: Click the 🎯 button to enable continuous listening (requires user interaction)
2. **Permission Issues**: Allow microphone access when prompted by your browser
3. **API Key**: Check that `ELEVENLABS_API_KEY` is set correctly in your .env file
4. **Character Limits**: Verify your ElevenLabs account has remaining character credits
5. **Browser Console**: Check for any error messages in browser developer tools
6. **Network Issues**: Ensure stable internet connection for speech recognition

**Common Issues:**
- **"Microphone access denied"**: Click the 🎯 button and allow microphone access
- **"No speech detected"**: Speak clearly and try again
- **"Network error"**: Check your internet connection
- **Topic not recognized**: Try saying "arrays", "strings", "trees", etc. clearly

The system will gracefully fall back to browser's built-in speech synthesis if ElevenLabs is unavailable.
