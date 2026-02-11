// Album Management System
let albums = [
    { title: "Album Title", images: ["DSC00971.jpg.jpeg", "IMG_8984.JPG.jpeg", "STAMINA.jpg.jpeg"] }
];

let currentAlbumIndex = 0;
let selectedFiles = [];
let selectedFilesForChange = [];

document.addEventListener('DOMContentLoaded', function() {
    // Menu button
    const menuBtn = document.getElementById('album-menu-btn');
    const menuModal = document.getElementById('album-modal');
    const changeModal = document.getElementById('change-album-modal');
    const addModal = document.getElementById('add-album-modal');
    
    // Close buttons
    const closeButtons = document.querySelectorAll('.close');
    
    // Menu options
    const modalOptions = document.querySelectorAll('.modal-btn[data-action]');
    
    // Event listeners
    menuBtn.addEventListener('click', () => {
        updateAlbumSelect();
        menuModal.classList.add('show');
    });
    
    closeButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.target.closest('.album-modal').classList.remove('show');
        });
    });
    
    // Close modal when clicking outside
    window.addEventListener('click', (e) => {
        if (e.target.classList.contains('album-modal')) {
            e.target.classList.remove('show');
        }
    });
    
    // Modal option buttons
    modalOptions.forEach(btn => {
        btn.addEventListener('click', () => {
            const action = btn.getAttribute('data-action');
            menuModal.classList.remove('show');
            
            if (action === 'add') {
                selectedFiles = [];
                document.getElementById('new-album-input').value = '';
                document.getElementById('add-image-input').value = '';
                document.getElementById('add-selected-images').innerHTML = '';
                addModal.classList.add('show');
            } else if (action === 'change') {
                selectedFilesForChange = [];
                document.getElementById('change-image-input').value = '';
                document.getElementById('change-selected-images').innerHTML = '';
                changeModal.classList.add('show');
            } else if (action === 'remove') {
                removeAlbum();
            }
        });
    });
    
    // Add album
    const confirmAddBtn = document.getElementById('confirm-add-btn');
    const newAlbumInput = document.getElementById('new-album-input');
    const addImageInput = document.getElementById('add-image-input');
    
    addImageInput.addEventListener('change', (e) => {
        selectedFiles = Array.from(e.target.files);
        updateAddImagePreview();
    });
    
    confirmAddBtn.addEventListener('click', () => {
        const title = newAlbumInput.value.trim();
        if (title) {
            const imageNames = selectedFiles.map(file => file.name);
            albums.push({ title: title, images: imageNames });
            currentAlbumIndex = albums.length - 1;
            updateDisplay();
            addModal.classList.remove('show');
            alert(`Album "${title}" added successfully!`);
        } else {
            alert('Please enter an album title');
        }
    });
    
    // Change album
    const confirmChangeBtn = document.getElementById('confirm-change-btn');
    const albumSelect = document.getElementById('album-select');
    const changeImageInput = document.getElementById('change-image-input');
    
    changeImageInput.addEventListener('change', (e) => {
        selectedFilesForChange = Array.from(e.target.files);
        updateChangeImagePreview();
    });
    
    confirmChangeBtn.addEventListener('click', () => {
        const selectedTitle = albumSelect.value;
        if (selectedTitle) {
            const index = albums.findIndex(a => a.title === selectedTitle);
            if (index !== -1) {
                if (selectedFilesForChange.length > 0) {
                    albums[index].images = selectedFilesForChange.map(file => file.name);
                }
                currentAlbumIndex = index;
                updateDisplay();
                changeModal.classList.remove('show');
                alert(`Switched to album: ${selectedTitle}`);
            }
        } else {
            alert('Please select an album');
        }
    });
});

function updateAlbumSelect() {
    const select = document.getElementById('album-select');
    // Clear existing options except the first one
    while (select.options.length > 1) {
        select.remove(1);
    }
    
    // Add albums to select
    albums.forEach(album => {
        const option = document.createElement('option');
        option.value = album.title;
        option.textContent = album.title;
        select.appendChild(option);
    });
}

function updateAddImagePreview() {
    const previewContainer = document.getElementById('add-selected-images');
    previewContainer.innerHTML = '';
    
    selectedFiles.forEach((file, index) => {
        const reader = new FileReader();
        reader.onload = (e) => {
            const div = document.createElement('div');
            div.className = 'image-preview-item';
            div.innerHTML = `
                <img src="${e.target.result}" alt="Preview">
                <button type="button" class="remove-preview" data-index="${index}">✕</button>
            `;
            previewContainer.appendChild(div);
            
            div.querySelector('.remove-preview').addEventListener('click', () => {
                selectedFiles.splice(index, 1);
                updateAddImagePreview();
            });
        };
        reader.readAsDataURL(file);
    });
}

function updateChangeImagePreview() {
    const previewContainer = document.getElementById('change-selected-images');
    previewContainer.innerHTML = '';
    
    selectedFilesForChange.forEach((file, index) => {
        const reader = new FileReader();
        reader.onload = (e) => {
            const div = document.createElement('div');
            div.className = 'image-preview-item';
            div.innerHTML = `
                <img src="${e.target.result}" alt="Preview">
                <button type="button" class="remove-preview" data-index="${index}">✕</button>
            `;
            previewContainer.appendChild(div);
            
            div.querySelector('.remove-preview').addEventListener('click', () => {
                selectedFilesForChange.splice(index, 1);
                updateChangeImagePreview();
            });
        };
        reader.readAsDataURL(file);
    });
}

function removeAlbum() {
    if (albums.length <= 1) {
        alert('Cannot remove the last album');
        return;
    }
    
    const confirmRemove = confirm(`Are you sure you want to remove "${albums[currentAlbumIndex].title}"?`);
    if (confirmRemove) {
        albums.splice(currentAlbumIndex, 1);
        currentAlbumIndex = 0;
        updateDisplay();
        alert('Album removed successfully');
    }
}

function updateDisplay() {
    const currentAlbum = albums[currentAlbumIndex];
    
    // Update title
    document.getElementById('album-title').textContent = currentAlbum.title;
    
    // Update images
    const imagesContainer = document.querySelector('.album-images-container');
    imagesContainer.innerHTML = '';
    
    if (currentAlbum.images.length > 0) {
        currentAlbum.images.forEach((image, index) => {
            const img = document.createElement('img');
            img.src = `/static/images/${image}`;
            img.alt = `Album image ${index + 1}`;
            img.className = 'album-image';
            // img.addEventListener('click', () => removeImage(index)); // Disabled
            // img.title = 'Click to remove image'; // Disabled
            imagesContainer.appendChild(img);
        });
    } else {
        imagesContainer.innerHTML = '<p>No images for this album</p>';
    }
}

function removeImage(index) {
    const currentAlbum = albums[currentAlbumIndex];
    const confirmRemove = confirm(`Remove image: ${currentAlbum.images[index]}?`);
    if (confirmRemove) {
        currentAlbum.images.splice(index, 1);
        updateDisplay();
    }
}

// Initialize display
updateDisplay();
