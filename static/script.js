// State management
let currentWebSocket = null;
let videoData = null;
let generationStartTime = null;

// Log severity levels for color coding
const LOG_LEVELS = {
    INFO: 'info',
    SUCCESS: 'success',
    ERROR: 'error',
    WARNING: 'warning'
};

// Keywords to detect log types
const LOG_KEYWORDS = {
    'successfully': LOG_LEVELS.SUCCESS,
    'completed': LOG_LEVELS.SUCCESS,
    'done': LOG_LEVELS.SUCCESS,
    'error': LOG_LEVELS.ERROR,
    'failed': LOG_LEVELS.ERROR,
    'exception': LOG_LEVELS.ERROR,
    'warning': LOG_LEVELS.WARNING,
    'started': LOG_LEVELS.INFO,
    'trying': LOG_LEVELS.INFO,
};

// Show specific state container
function showState(stateName) {
    const states = document.querySelectorAll('.state-container');
    states.forEach(state => state.classList.remove('active'));
    
    const targetState = document.getElementById(`${stateName}State`);
    if (targetState) {
        targetState.classList.add('active');
    }
}

// Add log entry to the logs list
function addLog(message, level = LOG_LEVELS.INFO) {
    const logsList = document.getElementById('logsList');
    const logItem = document.createElement('p');
    logItem.className = `log-item log-${level}`;
    
    // Add timestamp
    const timestamp = new Date().toLocaleTimeString();
    logItem.textContent = `[${timestamp}] ${message}`;
    
    logsList.appendChild(logItem);
    
    // Auto-scroll to bottom
    logsList.scrollTop = logsList.scrollHeight;
}

// Determine log level from message
function detectLogLevel(message) {
    const lowerMessage = message.toLowerCase();
    
    for (const [keyword, level] of Object.entries(LOG_KEYWORDS)) {
        if (lowerMessage.includes(keyword)) {
            return level;
        }
    }
    
    return LOG_LEVELS.INFO;
}

// Start video generation
function startGeneration() {
    generationStartTime = Date.now();
    showState('loading');
    document.getElementById('logsList').innerHTML = '';
    addLog('Connecting to generation service...');
    
    // Use Server-Sent Events (SSE) for streaming logs
    const eventSource = new EventSource('/generate-news-video-stream');
    
    eventSource.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            
            // Handle different message types
            if (data.type === 'log') {
                const level = detectLogLevel(data.message);
                addLog(data.message, level);
                updateProgress(data.progress || 0);
            } else if (data.type === 'progress') {
                updateProgress(data.progress);
            } else if (data.type === 'complete') {
                eventSource.close();
                handleGenerationComplete(data);
            }
        } catch (error) {
            console.error('Error parsing event data:', error);
        }
    };
    
    eventSource.onerror = (error) => {
        console.error('EventSource error:', error);
        eventSource.close();
        handleGenerationError('Connection lost during generation');
    };
}

// Update progress bar
function updateProgress(progress) {
    const progressFill = document.getElementById('progressFill');
    const progressText = document.getElementById('progressText');
    
    const percentage = Math.min(progress, 100);
    progressFill.style.width = `${percentage}%`;
    progressText.textContent = `Progress: ${percentage}%`;
}

// Handle successful video generation
function handleGenerationComplete(data) {
    videoData = data;
    
    const generationTime = Math.round((Date.now() - generationStartTime) / 1000);
    
    // Set success details
    document.getElementById('genTime').textContent = `${generationTime}s`;
    document.getElementById('scriptSummary').textContent = `${data.script.split(' ').length} words`;
    document.getElementById('articlesCount').textContent = data.articles.length;
    
    // Set video player
    const videoSource = document.getElementById('videoSource');
    videoSource.src = data.video_url;
    
    addLog('✅ Video generation completed successfully!', LOG_LEVELS.SUCCESS);
    updateProgress(100);
    
    // Show success state after a short delay
    setTimeout(() => {
        showState('success');
    }, 1000);
}

// Handle generation error
function handleGenerationError(errorMessage) {
    document.getElementById('errorMessage').textContent = errorMessage;
    addLog(`❌ Error: ${errorMessage}`, LOG_LEVELS.ERROR);
    
    setTimeout(() => {
        showState('error');
    }, 1000);
}

// Cancel generation
function cancelGeneration() {
    // Close any open connection
    if (currentWebSocket) {
        currentWebSocket.close();
    }
    
    // Reset to initial state
    resetForm();
    addLog('❌ Generation cancelled by user', LOG_LEVELS.WARNING);
}

// Download video
function downloadVideo() {
    if (!videoData || !videoData.video_url) {
        alert('No video available to download');
        return;
    }
    
    const link = document.createElement('a');
    link.href = videoData.video_url;
    link.download = `news-avatar-${Date.now()}.mp4`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    addLog('📥 Video download started', LOG_LEVELS.SUCCESS);
}

// Reset form to initial state
function resetForm() {
    showState('initial');
    videoData = null;
    generationStartTime = null;
    
    // Clear video player
    document.getElementById('videoSource').src = '';
    const videoPlayer = document.getElementById('videoPlayer');
    if (videoPlayer) {
        videoPlayer.load();
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    console.log('Page loaded successfully');
    showState('initial');
});
