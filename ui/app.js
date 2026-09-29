document.addEventListener('DOMContentLoaded', () => {
    const navGenerate = document.getElementById('nav-generate');
    const navGallery = document.getElementById('nav-gallery');
    const screenGenerate = document.getElementById('screen-generate');
    const screenGallery = document.getElementById('screen-gallery');
    const urlText = document.getElementById('url-text');
    
    // Gallery Data
    const galleryData = [
        "scenic landscape",
        "portrait, freckles",
        "bowl of fruit",
        "bluejay macro",
        "fairytale treehouse",
        "polar bear, openpose"
    ];

    const galleryGrid = document.querySelector('.gallery-grid');

    // Navigation Logic
    function switchScreen(screen) {
        if (screen === 'generate') {
            navGenerate.classList.add('active');
            navGallery.classList.remove('active');
            screenGenerate.classList.add('active');
            screenGallery.classList.remove('active');
            urlText.textContent = 'imaginairy.app / generate';
        } else if (screen === 'gallery') {
            navGallery.classList.add('active');
            navGenerate.classList.remove('active');
            screenGallery.classList.add('active');
            screenGenerate.classList.remove('active');
            urlText.textContent = 'imaginairy.app / gallery';
            renderGallery();
        }
    }

    navGenerate.addEventListener('click', (e) => {
        e.preventDefault();
        switchScreen('generate');
    });

    navGallery.addEventListener('click', (e) => {
        e.preventDefault();
        switchScreen('gallery');
    });

    // Render Gallery Cards
    async function renderGallery() {
        galleryGrid.innerHTML = '<p>Loading gallery...</p>';
        try {
            const res = await fetch('/api/history');
            const data = await res.json();
            galleryGrid.innerHTML = '';
            data.forEach(item => {
                const card = document.createElement('div');
                card.className = 'gallery-card';
                
                const img = document.createElement('img');
                img.src = item.image_url;
                img.style.width = '100%';
                img.style.height = '150px';
                img.style.objectFit = 'cover';
                img.style.borderRadius = 'var(--border-radius-md)';
                
                const promptText = document.createElement('p');
                promptText.textContent = item.prompt;

                card.appendChild(img);
                card.appendChild(promptText);
                galleryGrid.appendChild(card);
            });
        } catch (e) {
            galleryGrid.innerHTML = '<p>Error loading gallery</p>';
        }
    }

    // Generate Button Logic
    const generateBtn = document.getElementById('generate-btn');
    const previewPlaceholder = document.querySelector('.preview-placeholder');

    generateBtn.addEventListener('click', async () => {
        const originalText = generateBtn.innerHTML;
        generateBtn.innerHTML = 'Generating...';
        generateBtn.style.opacity = '0.7';
        generateBtn.style.pointerEvents = 'none';
        
        previewPlaceholder.innerHTML = '<p style="color: var(--teal-primary);">Generating image...</p>';

        const promptVal = document.getElementById('prompt').value || 'a scenic landscape';
        const modelVal = document.getElementById('model').value;
        const sizeVal = document.getElementById('image-size').value;
        const stepsVal = document.getElementById('steps').value;

        try {
            const response = await fetch('/api/generate_ui', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    prompt: promptVal,
                    model: modelVal,
                    image_size: sizeVal,
                    steps: parseInt(stepsVal) || 5,
                    controlnet: "None"
                })
            });
            const data = await response.json();
            
            generateBtn.innerHTML = originalText;
            generateBtn.style.opacity = '1';
            generateBtn.style.pointerEvents = 'all';
            
            previewPlaceholder.style.backgroundColor = 'transparent';
            previewPlaceholder.style.border = 'none';
            previewPlaceholder.innerHTML = `
                <img src="${data.image_url}" style="width: 100%; height: 100%; border-radius: var(--border-radius-lg); object-fit: contain; box-shadow: var(--shadow-md);" />
            `;
        } catch (e) {
            generateBtn.innerHTML = originalText;
            generateBtn.style.opacity = '1';
            generateBtn.style.pointerEvents = 'all';
            previewPlaceholder.innerHTML = '<p style="color: red;">Failed to generate image.</p>';
        }
    });
});
