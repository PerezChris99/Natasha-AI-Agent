// Dark/Light Mode Toggle
document.getElementById('mode-toggle').addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    let icon = document.getElementById('mode-toggle').getElementsByTagName('img')[0];

    if (document.body.classList.contains('dark-mode')) {
        icon.src = '/static/assets/icons/moon.png';  // Change to moon icon in dark mode
    } else {
        icon.src = '/static/assets/icons/sun.png';  // Change to sun icon in light mode
    }
});

// Voice Command Activation
document.getElementById('voice-command-btn').addEventListener('click', () => {
    startVoiceCommand();
});

function startVoiceCommand() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US';
    recognition.interimResults = false;

    recognition.start();

    recognition.onresult = function (event) {
        const command = event.results[0][0].transcript.toLowerCase();
        console.log('Voice Command:', command);

        if (command.includes('search')) {
            performWebSearch(command);
        } else if (command.includes('open')) {
            openApplication(command);
        } else if (command.includes('play')) {
            playMedia(command);
        } else {
            alert('Command not recognized.');
        }
    };

    recognition.onerror = function (event) {
        console.error('Speech recognition error:', event.error);
        alert('There was an error with the speech recognition.');
    };
}

// Perform Web Search
function performWebSearch(command) {
    const query = command.replace('search', '').trim();
    if (query) {
        window.open(`https://www.google.com/search?q=${query}`, '_blank');
    }
}

// Open Application (simplified for browsers)
function openApplication(command) {
    if (command.includes('browser')) {
        window.open('https://www.google.com', '_blank');
    } else {
        alert('Application not recognized.');
    }
}

// Play Media (simplified to opening a local media player)
function playMedia(command) {
    if (command.includes('play')) {
        alert('Playing media...');
        // Add further media control logic here (e.g., opening media players)
    } else {
        alert('Media not recognized.');
    }
}

// Function to start voice control
function startVoiceControl() {
    // Show a message while listening
    alert("Listening for your command...");

    // Call Flask route to process speech-to-text
    fetch('/voice/command')
        .then(response => response.json())
        .then(data => {
            const command = data.command;
            if (command) {
                alert(`You said: ${command}`);
                processVoiceCommand(command);
            } else {
                alert("Sorry, I didn't catch that.");
            }
        });
}

// Process the voice command
function processVoiceCommand(command) {
    if (command.includes("search")) {
        const query = command.replace("search", "").trim();
        performAction('search', query);
    } else if (command.includes("open")) {
        const app = command.replace("open", "").trim();
        performAction('open', app);
    } else if (command.includes("play")) {
        const media = command.replace("play", "").trim();
        performAction('play', media);
    } else {
        alert("Sorry, I couldn't understand that command.");
    }
}

function performAction(action, data) {
    if (action === 'search') {
        fetch(`/action/search?q=${data}`)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert("Search complete!");
                } else {
                    alert("Search failed.");
                }
            });
    } else if (action === 'open') {
        fetch(`/action/open?app=${data}`)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert(`${data.app} is now open!`);
                } else {
                    alert("Failed to open the application.");
                }
            });
    } else if (action === 'play') {
        fetch(`/action/play?media=${data}`)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert(`Playing media: ${data.media}`);
                } else {
                    alert("Failed to play media.");
                }
            });
    }
}

function playSpotifyTrack(trackName) {
    fetch(`/action/play/spotify?track=${trackName}`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert(`Now playing on Spotify: ${data.track}`);
            } else {
                alert("Failed to play track.");
            }
        });
}

function playYouTubeVideo(url) {
    fetch(`/action/play/youtube?url=${url}`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert(`Now playing video: ${data.video}`);
            } else {
                alert("Failed to play video.");
            }
        });
}
