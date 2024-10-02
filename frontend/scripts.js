// Indexing page functionality
function setupIndexingPage() {
    const linkContainer = document.getElementById('linkContainer');
    const newLinkInput = document.getElementById('newLink');
    const addLinkButton = document.getElementById('addLink');
    const submitButton = document.querySelector('button[type="submit"]');
    const messageDiv = document.getElementById('message');
    const spinner = document.createElement('svg'); // Create spinner element
    spinner.className = 'animate-spin h-5 w-5 text-white hidden'; // Set classes
    spinner.innerHTML = `
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
    `;
    submitButton.appendChild(spinner); // Append spinner to submit button

    function addLink(link) {
        const linkElement = document.createElement('div');
        linkElement.className = 'flex items-center';
        linkElement.innerHTML = `
            <input type="text" name="websites" value="${link}" readonly class="flex-grow mr-2 border border-gray-300 rounded-md shadow-sm bg-gray-100 h-10 px-3" />
            <button type="button" class="deleteLink px-4 h-10 bg-red-600 text-white rounded hover:bg-red-700">Delete</button>
        `;
        linkContainer.appendChild(linkElement);

        linkElement.querySelector('.deleteLink').addEventListener('click', () => {
            linkContainer.removeChild(linkElement);
        });
    }

    addLinkButton.addEventListener('click', () => {
        const link = newLinkInput.value.trim();
        if (link) {
            addLink(link);
            newLinkInput.value = '';
        }
    });

    document.getElementById('indexForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData();

        // Append files
        const fileInput = document.getElementById('files');
        for (const file of fileInput.files) {
            if (file.name) { // Ensure the file has a name
                formData.append('files', file);
            }
        }

        // Append websites as a comma-separated string
        const websites = Array.from(document.getElementsByName('websites'))
                               .map(input => input.value)
                               .filter(value => value !== '')
                               .join(',');
        formData.append('websites', websites);

        // Show spinner and disable button
        spinner.classList.remove('hidden');
        submitButton.disabled = true;
        messageDiv.textContent = ''; // Clear previous messages

        try {
            const response = await fetch('/index', {
                method: 'POST',
                body: formData
            });
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Unknown error');
            }
            const result = await response.json();
            messageDiv.textContent = result.message;
        } catch (error) {
            console.error('Error:', error);
            messageDiv.textContent = 'An error occurred during indexing.';
        } finally {
            // Hide spinner and enable button
            spinner.classList.add('hidden');
            submitButton.disabled = false;
        }
    });
}

// Generation page functionality
function setupGenerationPage() {
    const form = document.getElementById('generationForm');
    const submitBtn = document.getElementById('submitBtn');
    const btnText = document.getElementById('btnText');
    const spinner = document.getElementById('spinner');
    const answerDiv = document.getElementById('answer');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        
        // Show spinner and disable button
        btnText.textContent = 'Generating...';
        spinner.classList.remove('hidden');
        submitBtn.disabled = true;
        answerDiv.classList.add('hidden');
        
        try {
            const response = await fetch('/generate', {
                method: 'POST',
                body: formData
            });
            const result = await response.json();
            answerDiv.textContent = result.answer;
            answerDiv.classList.remove('hidden');
        } catch (error) {
            console.error('Error:', error);
            answerDiv.textContent = 'An error occurred during generation.';
            answerDiv.classList.remove('hidden');
        } finally {
            // Hide spinner and enable button
            btnText.textContent = 'Generate';
            spinner.classList.add('hidden');
            submitBtn.disabled = false;
        }
    });
}

// Check which page we're on and setup accordingly
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('indexForm')) {
        setupIndexingPage();
    } else if (document.getElementById('generationForm')) {
        setupGenerationPage();
    }
});