# Per-Picture Unlock System with Blur

## Overview

Each FLIRTY and INTIMATE picture requires tokens to unlock individually. Locked pictures appear blurred in the gallery until purchased. CASUAL pictures are always free and unblurred.

---

## Token Costs (Per Picture)

- **CASUAL**: FREE (always unlocked)
- **FLIRTY**: 10 tokens per picture
- **INTIMATE**: 25 tokens per picture

---

## How It Works

### 1. Picture Generation
When AI generates a picture with `[SEND_IMAGE: ...]` tag:
- System determines intimacy level from tags
- Picture is saved to gallery
- Level is stored in filename or metadata

### 2. Gallery Display
When user opens gallery:
- All pictures are shown
- CASUAL pictures: Clear/unblurred
- FLIRTY/INTIMATE locked: Blurred with unlock button
- Shows cost to unlock each picture

### 3. Picture Unlock
User clicks "Unlock" on a blurred picture:
- Checks token balance
- Deducts tokens (10 for FLIRTY, 25 for INTIMATE)
- Adds picture_id to unlocked set
- Picture becomes unblurred

---

## API Endpoints

### 1. Get Gallery
**Endpoint:** `POST /api/get-gallery`

**Request:**
```json
{
  "session_id": "user123"
}
```

**Response:**
```json
{
  "pictures": [
    {
      "picture_id": "user123_image1.png",
      "filename": "image1.png",
      "path": "/static/images/user123/image1.png",
      "level": "CASUAL",
      "is_unlocked": true,
      "unlock_cost": 0,
      "should_blur": false
    },
    {
      "picture_id": "user123_image2.png",
      "filename": "image2.png",
      "path": "/static/images/user123/image2.png",
      "level": "FLIRTY",
      "is_unlocked": false,
      "unlock_cost": 10,
      "should_blur": true
    },
    {
      "picture_id": "user123_image3.png",
      "filename": "image3.png",
      "path": "/static/images/user123/image3.png",
      "level": "INTIMATE",
      "is_unlocked": false,
      "unlock_cost": 25,
      "should_blur": true
    }
  ],
  "total_pictures": 3,
  "unlocked_count": 1,
  "locked_count": 2,
  "gallery_limit": 6,
  "tokens": 50
}
```

---

### 2. Unlock Picture
**Endpoint:** `POST /api/unlock-picture`

**Request:**
```json
{
  "session_id": "user123",
  "picture_id": "user123_image2.png",
  "picture_level": "FLIRTY"
}
```

**Response (Success):**
```json
{
  "status": "success",
  "message": "Picture unlocked!",
  "tokens_remaining": 40,
  "picture_id": "user123_image2.png",
  "cost": 10,
  "total_unlocked": 2
}
```

**Response (Error - Not Enough Tokens):**
```json
{
  "error": "Not enough tokens. Need 10, have 5",
  "tokens_needed": 5
}
```

**Response (Error - Already Unlocked):**
```json
{
  "error": "Picture already unlocked"
}
```

---

### 3. Token Status
**Endpoint:** `POST /api/token-status`

**Request:**
```json
{
  "session_id": "user123"
}
```

**Response:**
```json
{
  "tokens": 50,
  "unlocked_pictures_count": 3,
  "gallery_limit": 6,
  "max_gallery_limit": 30,
  "picture_unlock_costs": {
    "FLIRTY": {
      "cost": 10,
      "affordable_count": 5
    },
    "INTIMATE": {
      "cost": 25,
      "affordable_count": 2
    }
  },
  "gallery_expansion": {
    "cost_per_slot": 30,
    "max_affordable_slots": 1,
    "can_expand": true,
    "slots_remaining": 24
  }
}
```

---

## Picture Level Detection

### Automatic Detection from Tags
System analyzes picture path/filename to determine level:

```python
def get_picture_level_from_path(picture_path):
    path_lower = picture_path.lower()
    
    if 'intimate' in path_lower or 'explicit' in path_lower or 'nude' in path_lower:
        return 'INTIMATE'
    elif 'flirty' in path_lower or 'suggestive' in path_lower or 'sexy' in path_lower:
        return 'FLIRTY'
    else:
        return 'CASUAL'
```

### AI Tag Examples
- **CASUAL**: `[SEND_IMAGE: cute selfie, smiling]`
- **FLIRTY**: `[SEND_IMAGE: FLIRTY - cleavage, seductive pose]`
- **INTIMATE**: `[SEND_IMAGE: INTIMATE - nude, full body]`

---

## Frontend Implementation

### Display Gallery with Blur
```html
<div class="gallery">
  <!-- For each picture -->
  <div class="picture-card">
    <img 
      src="/static/images/user123/image2.png" 
      class="picture-image ${should_blur ? 'blurred' : ''}"
    />
    
    ${!is_unlocked ? `
      <div class="unlock-overlay">
        <button onclick="unlockPicture('${picture_id}', '${level}')">
          🔒 Unlock for ${unlock_cost} tokens
        </button>
      </div>
    ` : ''}
  </div>
</div>
```

### CSS for Blur Effect
```css
.picture-image.blurred {
  filter: blur(20px);
  -webkit-filter: blur(20px);
}

.unlock-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.5);
}

.unlock-overlay button {
  padding: 10px 20px;
  background: #ff4081;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
}
```

### JavaScript to Unlock
```javascript
async function unlockPicture(pictureId, level) {
  const response = await fetch('/api/unlock-picture', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      session_id: sessionId,
      picture_id: pictureId,
      picture_level: level
    })
  });
  
  const data = await response.json();
  
  if (data.status === 'success') {
    // Remove blur and overlay
    document.querySelector(`[data-picture-id="${pictureId}"]`)
      .classList.remove('blurred');
    
    // Update token display
    updateTokens(data.tokens_remaining);
    
    // Show success message
    showNotification(`Picture unlocked! ${data.tokens_remaining} tokens remaining`);
    
    // Refresh gallery
    loadGallery();
  } else {
    showNotification(data.error, 'error');
  }
}
```

---

## Usage Examples

### Example 1: User Views Gallery

**User has 30 tokens, 6 pictures in gallery**

1. User opens gallery
2. Frontend calls: `POST /api/get-gallery`
3. Backend returns:
   - 2 CASUAL (unblurred, free)
   - 2 FLIRTY (blurred, 10 tokens each)
   - 2 INTIMATE (blurred, 25 tokens each)

4. UI shows:
   - ✅ 2 clear pictures
   - 🔒 2 blurred pictures with "Unlock for 10 tokens"
   - 🔒 2 blurred pictures with "Unlock for 25 tokens"

---

### Example 2: Unlock FLIRTY Picture

**User has 30 tokens, clicks unlock on FLIRTY picture**

1. User clicks "🔒 Unlock for 10 tokens"
2. Frontend calls: `POST /api/unlock-picture`
   ```json
   {
     "session_id": "user123",
     "picture_id": "user123_flirty1.png",
     "picture_level": "FLIRTY"
   }
   ```

3. Backend:
   - Checks balance: 30 >= 10 ✅
   - Deducts 10 tokens
   - Adds to unlocked set
   - Returns success

4. Frontend:
   - Removes blur effect
   - Hides unlock overlay
   - Updates token count: 20
   - Shows notification: "Picture unlocked!"

---

### Example 3: Not Enough Tokens

**User has 5 tokens, tries to unlock INTIMATE (25 tokens)**

1. User clicks "🔒 Unlock for 25 tokens"
2. Backend checks: 5 < 25 ❌
3. Returns error:
   ```json
   {
     "error": "Not enough tokens. Need 25, have 5",
     "tokens_needed": 20
   }
   ```

4. Frontend shows:
   - "Not enough tokens! You need 20 more tokens."
   - "Keep chatting to earn more tokens!"

---

### Example 4: Unlock Multiple Pictures

**User has 50 tokens, wants to unlock 2 FLIRTY + 1 INTIMATE**

1. Unlock FLIRTY #1: 50 - 10 = 40 tokens
2. Unlock FLIRTY #2: 40 - 10 = 30 tokens
3. Unlock INTIMATE #1: 30 - 25 = 5 tokens

Total spent: 45 tokens
Remaining: 5 tokens
Pictures unlocked: 3

---

## Token Economics

### Earning Rate:
- Base: 2 tokens per message
- Bonus: +1 for compliments
- Average: 2-3 tokens per message

### Unlock Times:
- **FLIRTY picture**: ~3-5 messages (10 tokens)
- **INTIMATE picture**: ~8-13 messages (25 tokens)
- **Gallery slot**: ~10-15 messages (30 tokens)

### Example Session:
User chats for 20 messages:
- Earns: ~40-60 tokens
- Can unlock: 4 FLIRTY or 1-2 INTIMATE pictures
- Or: 1 gallery slot + 1 FLIRTY picture

---

## Benefits

### For Users:
- **Granular Control**: Unlock only pictures they want
- **Lower Barrier**: 10 tokens vs 50 for level unlock
- **Visual Feedback**: See what's locked with blur
- **Flexible Spending**: Choose which pictures to unlock
- **Collection Building**: Gradually build gallery

### For Monetization:
- **More Opportunities**: Each picture is a purchase
- **Lower Friction**: Smaller purchases feel easier
- **Recurring Revenue**: New pictures = new purchases
- **Visible Value**: Users see what they're buying
- **Engagement Loop**: Chat → Earn → Unlock → Repeat

### For Gameplay:
- **Progression Feel**: Unlock pictures over time
- **Meaningful Choices**: Which pictures to unlock first?
- **Gallery Curation**: Limited slots + unlock costs
- **Discovery**: See blurred previews of content
- **Reward System**: Unlock feels like achievement

---

## Storage

```python
# Per-session storage
unlocked_pictures = {
    'user123': {
        'user123_image1.png',
        'user123_image2.png',
        'user123_image5.png'
    }
}

# Picture ID format: {session_id}_{filename}
```

---

## Helper Functions

```python
# Check if specific picture is unlocked
is_picture_unlocked(session_id, picture_id)
# Returns: True/False

# Get all unlocked pictures for session
get_unlocked_pictures(session_id)
# Returns: set(['picture_id_1', 'picture_id_2', ...])

# Determine picture level from path
get_picture_level_from_path(picture_path)
# Returns: 'CASUAL', 'FLIRTY', or 'INTIMATE'
```

---

## Constants

```python
# Per-picture unlock costs
PICTURE_UNLOCK_COSTS = {
    'FLIRTY': 10,
    'INTIMATE': 25
}

# Gallery settings
GALLERY_EXPANSION_COST = 30
DEFAULT_GALLERY_LIMIT = 6
MAX_GALLERY_LIMIT = 30

# Token earning
TOKENS_PER_MESSAGE = 2
TOKENS_FOR_COMPLIMENT = 1
```

---

## Error Handling

**Not Enough Tokens:**
```json
{
  "error": "Not enough tokens. Need 10, have 5",
  "tokens_needed": 5
}
```

**Already Unlocked:**
```json
{
  "error": "Picture already unlocked"
}
```

**Invalid Picture Level:**
```json
{
  "error": "Invalid picture level"
}
```

**CASUAL Unlock Attempt:**
```json
{
  "error": "CASUAL pictures don't need to be unlocked"
}
```

---

## Migration from Level-Based System

**Old System:**
- Unlock entire FLIRTY level: 50 tokens
- All FLIRTY pictures unlocked at once

**New System:**
- Unlock each FLIRTY picture: 10 tokens
- More granular, lower barrier
- Users unlock what they want

**Advantage:**
- 5 FLIRTY pictures = 50 tokens total (same cost)
- But users can unlock 1 at a time
- Feels more affordable and flexible

---

## Summary

**Complete per-picture unlock system:**
- ✅ Individual picture unlocks (10/25 tokens)
- ✅ Blur effect for locked pictures
- ✅ Gallery API with unlock status
- ✅ Unlock API for individual pictures
- ✅ Automatic level detection
- ✅ Token status with affordability
- ✅ Frontend-ready JSON responses
- ✅ Lower costs, more flexibility
- ✅ Better user experience
- ✅ More monetization opportunities

**Each FLIRTY and INTIMATE picture now requires individual unlock with tokens, staying blurred until purchased!** 🔒💰✨
