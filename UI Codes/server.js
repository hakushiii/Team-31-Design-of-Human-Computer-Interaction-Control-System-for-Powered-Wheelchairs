const express = require('express');
const fs = require('fs');
const app = express();
const path = require('path');
const port = 3000;


app.use(express.json());

// Serve static files from the current directory and 'public' directory
app.use(express.static(__dirname));
app.use(express.static(path.join(__dirname, 'public')));

// Handle POST request to '/saveData'
app.post('/saveData', (req, res) => {
    // Extract combinedValues from the request body
    const { combinedValues } = req.body;

    // Initialize data object
    let data = {};

    try {
        // Read the content of 'data.json' file and parse it to JSON
        const rawData = fs.readFileSync('data.json');
        data = JSON.parse(rawData);
    } catch (error) {
        console.error('Error reading data from file:', error.message);
    }

    // Update data object with new combinedValues if provided
    if (combinedValues) {
        data.combinedValues = combinedValues;
    }

    try {
        // Write the updated data object back to 'data.json' file
        fs.writeFileSync('data.json', JSON.stringify(data, null, 2));
        console.log('Data saved successfully.');
    } catch (error) {
        console.error('Error writing data to file:', error.message);
    }

    // Respond with a JSON message indicating successful data save
    res.json({ message: 'Data saved successfully.' });
});

// Handle POST request to '/storeCommand'
app.post('/storeCommand', express.json(), (req, res) => {
    // Extract command from the request body
    const { command } = req.body;

    // Store the command in a JSON file named 'command.json'
    fs.writeFileSync('command.json', JSON.stringify({ command }));

    // Respond with a success message
    res.send('Command stored successfully.');
});

// Define routes for various HTML files
app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname, 'public', 'main.html'));
});

app.get('/speed', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'speed.html'));
});

app.get('/eog', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'eog.html'));
});

app.get('/eeg', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'eeg.html'));
});

app.get('/control', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'test2.html'));
});

app.get('/direction', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'direction.html'));
});

app.get('/help', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'help.html'));
});

// Start the server and listen on the specified port
app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});
