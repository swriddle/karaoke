// Initialize variables
let fuse;
let songData = [];

// Load the JSON data
fetch('/songs-37ed97f71683030562e2.json') // Replace with your actual path to the JSON file
    .then(response => response.json())
    .then(data => {
        songData = data;

        // Initialize Fuse.js with options
        const options = {
            keys: ['title', 'artist'], // Keys to search in
            threshold: 0.4 // Adjust the threshold to control fuzziness
        };

        fuse = new Fuse(songData, options);
    })
    .catch(error => console.error('Error loading song data:', error));

// Perform search and update results
function performSearch() {
    const query = document.getElementById('searchInput').value;

    if (query.trim() === '') {
        displayResults([]); // Clear results if the query is empty
        return;
    }

    const results = fuse.search(query);
    displayResults(results);
}

// Function to display search results
function displayResults(results) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = ''; // Clear previous results

    if (results.length === 0) {
        resultsDiv.innerHTML = '<p>No results found</p>';
        return;
    }

    results.forEach(result => {
        const item = document.createElement('div');
        item.innerHTML = `<strong>${result.item.title}</strong> by ${result.item.artist}`;
        resultsDiv.appendChild(item);
    });
}
