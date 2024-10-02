// Indexing page functionality
function setupIndexingPage() {
    const linkContainer = document.getElementById('linkContainer');
    const newLinkInput = document.getElementById('newLink');
    const addLinkButton = document.getElementById('addLink');

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
        const formData = new FormData(e.target);
        
        try {
            const response = await fetch('/index', {
                method: 'POST',
                body: formData
            });
            const result = await response.json();
            document.getElementById('message').textContent = result.message;
        } catch (error) {
            console.error('Error:', error);
            document.getElementById('message').textContent = 'An error occurred during indexing.';
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
