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
