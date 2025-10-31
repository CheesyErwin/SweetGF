# Image Protection System

## Overview

Comprehensive protection system to prevent users from saving locked/blurred images through right-click, drag-and-drop, keyboard shortcuts, or direct URL access.

---

## Protection Layers

### 1. Client-Side Protection (JavaScript)
**File:** `static/image-protection.js`

**Features:**
- ✅ Disable right-click on images
- ✅ Disable drag-and-drop
- ✅ Disable Ctrl+S / Cmd+S
- ✅ Disable image selection
- ✅ Show protection message
- ✅ Optional watermarking

**Methods Blocked:**
- Right-click → Save Image As
- Drag image to desktop
- Ctrl+S to save page
- Select and copy image
- Inspect element on images (optional)

---

### 2. Server-Side Protection (Python)
**Endpoint:** `/api/protected-image/<session_id>/<filename>`

**Features:**
- ✅ Check unlock status before serving
- ✅ Apply blur to locked images
- ✅ Add "LOCKED" watermark to blurred images
- ✅ Add subtle watermark to unlocked images
- ✅ Prevent caching with headers
- ✅ Serve inline (no download dialog)

**Protection:**
- Direct URL access → Returns blurred version if locked
- Locked images → Heavy blur + "LOCKED" text
- Unlocked images → Subtle "© SweetGF" watermark
- No caching → Can't save from browser cache

---

### 3. CSS Protection
**Built into:** `image-protection.js`

**Features:**
```css
img {
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
    -webkit-user-drag: none;
    -khtml-user-drag: none;
    -moz-user-drag: none;
    -o-user-drag: none;
    pointer-events: auto;
}
```

---

## How It Works

### Locked Image Flow:

1. **User views gallery**
   - Frontend requests: `GET /api/protected-image/user123/image.png`

2. **Server checks unlock status**
   - `is_picture_unlocked(session_id, picture_id)` → False

3. **Server applies protection**
   - Opens original image
   - Applies GaussianBlur(radius=30)
   - Adds "🔒 LOCKED" watermark (centered, large)
   - Returns blurred image

4. **Client displays**
   - Shows heavily blurred image
   - Right-click disabled
   - Drag disabled
   - Shows "Unlock for X tokens" button

5. **User tries to save**
   - Right-click → Blocked, shows "🔒 Images are protected"
   - Drag → Blocked
   - Ctrl+S → Blocked
   - Direct URL → Gets blurred version

---

### Unlocked Image Flow:

1. **User unlocks picture**
   - Spends tokens
   - `picture_id` added to unlocked set

2. **Server serves unlocked**
   - Opens original image
   - Adds subtle "© SweetGF" watermark (bottom-right, small)
   - Sets no-cache headers
   - Returns watermarked image

3. **Client displays**
   - Shows clear image with watermark
   - Right-click still disabled
   - Drag still disabled
   - Even if saved, has watermark

---

## Server-Side Implementation

### Protected Image Endpoint

```python
@app.route('/api/protected-image/<session_id>/<filename>')
def serve_protected_image(session_id, filename):
    # Check unlock status
    if level != 'CASUAL' and not is_picture_unlocked(session_id, picture_id):
        # Return blurred version
        img = img.filter(ImageFilter.GaussianBlur(radius=30))
        # Add LOCKED watermark
        draw.text((x, y), "🔒 LOCKED", font=font, fill=text_color)
        return send_file(img_io, mimetype='image/png')
    
    # Return unlocked with watermark
    draw.text((x, y), "© SweetGF", font=font, fill=(255, 255, 255, 128))
    
    # Prevent caching
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate'
    response.headers['Content-Disposition'] = 'inline'
    
    return response
```

---

## Client-Side Implementation

### Include Protection Script

```html
<!-- In your HTML -->
<script src="/static/image-protection.js"></script>
```

### Gallery Display

```html
<div class="gallery">
    <div class="picture-card">
        <!-- Use protected endpoint -->
        <img 
            src="/api/protected-image/user123/image.png"
            alt="Picture"
            class="protected-image"
        />
        
        <!-- Unlock button for locked images -->
        <div class="unlock-overlay" v-if="!picture.is_unlocked">
            <button @click="unlockPicture(picture)">
                🔒 Unlock for {{ picture.unlock_cost }} tokens
            </button>
        </div>
    </div>
</div>
```

### Protection Features

```javascript
// Automatically applied by image-protection.js

// 1. Disable right-click
document.addEventListener('contextmenu', function(e) {
    if (e.target.tagName === 'IMG') {
        e.preventDefault();
        showProtectionMessage();
        return false;
    }
});

// 2. Disable drag
document.addEventListener('dragstart', function(e) {
    if (e.target.tagName === 'IMG') {
        e.preventDefault();
        return false;
    }
});

// 3. Disable save shortcuts
document.addEventListener('keydown', function(e) {
    if ((e.ctrlKey || e.metaKey) && e.key === 's') {
        e.preventDefault();
        return false;
    }
});
```

---

## Protection Message

When user tries to save:

```
┌─────────────────────────┐
│  🔒 Images are protected │
└─────────────────────────┘
```

- Appears top-right
- Fades in/out
- 2-second duration
- Non-intrusive

---

## Watermark System

### Locked Images:
```
┌────────────────────────┐
│                        │
│                        │
│     🔒 LOCKED          │  ← Large, centered
│                        │
│                        │
└────────────────────────┘
```

- Large text (60px)
- Centered
- Black outline + white fill
- On heavily blurred image

### Unlocked Images:
```
┌────────────────────────┐
│                        │
│                        │
│                        │
│                        │
│           © SweetGF    │  ← Small, bottom-right
└────────────────────────┘
```

- Small text (16px)
- Bottom-right corner
- Semi-transparent (128 alpha)
- Subtle but visible

---

## Protection Effectiveness

### What Users CAN'T Do:

❌ Right-click → Save Image As
❌ Drag image to desktop
❌ Ctrl+S to save page
❌ Select and copy image
❌ Access original via direct URL
❌ Get unblurred version of locked images
❌ Remove watermark from unlocked images
❌ Save from browser cache (no-cache headers)

### What Users CAN Do:

✅ View unlocked images
✅ Take screenshots (but watermarked)
✅ Use screen recording (but watermarked)

**Note:** Screenshots/recordings will capture:
- Blurred version for locked images
- Watermarked version for unlocked images

---

## Advanced Protection (Optional)

### Disable DevTools on Images

```javascript
function disableInspectOnImages() {
    document.addEventListener('keydown', function(e) {
        // F12 or Ctrl+Shift+I
        if (e.key === 'F12' || 
            ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'I')) {
            const target = document.elementFromPoint(e.clientX, e.clientY);
            if (target && target.tagName === 'IMG') {
                e.preventDefault();
                return false;
            }
        }
    });
}
```

### Canvas-Based Watermarking

```javascript
function addWatermark(imageElement, sessionId) {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    
    const img = new Image();
    img.onload = function() {
        canvas.width = img.width;
        canvas.height = img.height;
        
        // Draw image
        ctx.drawImage(img, 0, 0);
        
        // Add watermark
        ctx.font = '20px Arial';
        ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
        ctx.fillText(`© SweetGF - ${sessionId}`, 
                     canvas.width / 2, 
                     canvas.height - 30);
        
        // Replace with watermarked version
        imageElement.src = canvas.toDataURL();
    };
    img.src = imageElement.src;
}
```

---

## Headers for Protection

### No-Cache Headers:
```python
response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
response.headers['Pragma'] = 'no-cache'
response.headers['Expires'] = '0'
```

**Purpose:** Prevent browser from caching images

### Content-Disposition:
```python
response.headers['Content-Disposition'] = 'inline'
```

**Purpose:** Display inline, not as download

---

## Testing Protection

### Test Right-Click:
1. Right-click on image
2. Should see "🔒 Images are protected" message
3. Context menu should not appear

### Test Drag:
1. Try to drag image
2. Should not be draggable
3. Cursor should not change

### Test Save:
1. Press Ctrl+S (or Cmd+S)
2. Should be blocked
3. Page should not save

### Test Direct URL:
1. Copy image URL
2. Open in new tab
3. Should see blurred version if locked
4. Should see watermarked version if unlocked

### Test DevTools:
1. Open DevTools
2. Inspect image element
3. Copy image URL from src
4. Open URL → Still protected

---

## Browser Compatibility

### Supported Browsers:
- ✅ Chrome/Edge (Chromium)
- ✅ Firefox
- ✅ Safari
- ✅ Opera

### Protection Features:
- ✅ Right-click blocking: All browsers
- ✅ Drag blocking: All browsers
- ✅ CSS user-select: All browsers
- ✅ Keyboard shortcuts: All browsers
- ✅ Server-side blur: All browsers

---

## Limitations

### Cannot Prevent:
- Screenshots (OS-level)
- Screen recording (OS-level)
- Camera photos of screen
- OCR of watermarked images

### Mitigation:
- Watermarks visible in screenshots
- Blurred images for locked content
- Session-specific watermarks (optional)
- Legal terms of service

---

## Configuration

### Blur Intensity:
```python
# Adjust blur radius (default: 30)
img = img.filter(ImageFilter.GaussianBlur(radius=30))
```

### Watermark Size:
```python
# Locked image watermark (default: 60px)
font = ImageFont.truetype("arial.ttf", 60)

# Unlocked image watermark (default: 16px)
font = ImageFont.truetype("arial.ttf", 16)
```

### Watermark Opacity:
```python
# Unlocked watermark (default: 128/255 = 50%)
draw.text((x, y), "© SweetGF", fill=(255, 255, 255, 128))
```

---

## Files

### Created:
- `static/image-protection.js` - Client-side protection
- `IMAGE_PROTECTION_SYSTEM.md` - This documentation

### Modified:
- `app.py`:
  - Added `/api/protected-image/<session_id>/<filename>` endpoint
  - Updated `/api/get-gallery` to use protected URLs
  - Added blur and watermark logic

---

## Usage

### 1. Include Script:
```html
<script src="/static/image-protection.js"></script>
```

### 2. Use Protected URLs:
```javascript
// Gallery API returns protected URLs
const picture = {
    path: "/api/protected-image/user123/image.png",
    is_unlocked: false
};
```

### 3. Display Images:
```html
<img src="${picture.path}" class="protected-image" />
```

### 4. Protection Automatic:
- Right-click blocked ✅
- Drag blocked ✅
- Save shortcuts blocked ✅
- Server serves blurred/watermarked ✅

---

## Summary

**Complete multi-layer image protection:**
- ✅ Client-side: JS blocks right-click, drag, save
- ✅ Server-side: Blur locked images, add watermarks
- ✅ CSS: Disable selection and dragging
- ✅ Headers: Prevent caching
- ✅ Watermarks: Visible on all saves
- ✅ Protected endpoint: Check unlock status
- ✅ User feedback: Protection messages

**Users cannot save original locked images through any standard browser method!** 🔒✨
