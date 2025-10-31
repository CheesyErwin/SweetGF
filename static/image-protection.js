/**
 * Image Protection System
 * Prevents users from saving locked/blurred images
 */

// Disable right-click on all images
document.addEventListener('DOMContentLoaded', function() {
    protectAllImages();
});

function protectAllImages() {
    // Disable right-click on images
    document.addEventListener('contextmenu', function(e) {
        if (e.target.tagName === 'IMG' || e.target.closest('.picture-card')) {
            e.preventDefault();
            showProtectionMessage();
            return false;
        }
    });

    // Disable drag and drop on images
    document.addEventListener('dragstart', function(e) {
        if (e.target.tagName === 'IMG') {
            e.preventDefault();
            return false;
        }
    });

    // Disable keyboard shortcuts for saving
    document.addEventListener('keydown', function(e) {
        // Ctrl+S or Cmd+S
        if ((e.ctrlKey || e.metaKey) && e.key === 's') {
            e.preventDefault();
            return false;
        }
    });

    // Add protection attributes to all images
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        img.setAttribute('oncontextmenu', 'return false;');
        img.setAttribute('ondragstart', 'return false;');
        img.style.userSelect = 'none';
        img.style.webkitUserSelect = 'none';
        img.style.mozUserSelect = 'none';
        img.style.msUserSelect = 'none';
    });
}

function showProtectionMessage() {
    // Show a brief message that images are protected
    const message = document.createElement('div');
    message.className = 'protection-message';
    message.textContent = '🔒 Images are protected';
    message.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: rgba(0, 0, 0, 0.8);
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        z-index: 10000;
        animation: fadeInOut 2s ease-in-out;
    `;
    
    document.body.appendChild(message);
    
    setTimeout(() => {
        message.remove();
    }, 2000);
}

// Add CSS animation
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeInOut {
        0% { opacity: 0; transform: translateY(-10px); }
        20% { opacity: 1; transform: translateY(0); }
        80% { opacity: 1; transform: translateY(0); }
        100% { opacity: 0; transform: translateY(-10px); }
    }
    
    img {
        pointer-events: auto;
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
        -webkit-user-drag: none;
        -khtml-user-drag: none;
        -moz-user-drag: none;
        -o-user-drag: none;
    }
    
    .picture-card {
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
    }
`;
document.head.appendChild(style);

// Additional protection: Disable inspect element on images (optional)
function disableInspectOnImages() {
    document.addEventListener('keydown', function(e) {
        // F12 or Ctrl+Shift+I or Ctrl+Shift+C
        if (e.key === 'F12' || 
            ((e.ctrlKey || e.metaKey) && e.shiftKey && (e.key === 'I' || e.key === 'C'))) {
            const target = document.elementFromPoint(e.clientX, e.clientY);
            if (target && target.tagName === 'IMG') {
                e.preventDefault();
                showProtectionMessage();
                return false;
            }
        }
    });
}

// Optional: Call this if you want stricter protection
// disableInspectOnImages();

// Watermark function for additional protection
function addWatermark(imageElement, sessionId) {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    
    const img = new Image();
    img.crossOrigin = 'anonymous';
    img.onload = function() {
        canvas.width = img.width;
        canvas.height = img.height;
        
        // Draw original image
        ctx.drawImage(img, 0, 0);
        
        // Add watermark
        ctx.font = '20px Arial';
        ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
        ctx.textAlign = 'center';
        ctx.fillText(`© SweetGF - ${sessionId}`, canvas.width / 2, canvas.height - 30);
        
        // Replace image source with watermarked version
        imageElement.src = canvas.toDataURL();
    };
    img.src = imageElement.src;
}

// Export functions for use in other scripts
window.imageProtection = {
    protectAllImages,
    showProtectionMessage,
    addWatermark
};
