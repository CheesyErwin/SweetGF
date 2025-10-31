# Token Unlock System - Pictures & Gallery

## Overview

Users can spend tokens to unlock picture intimacy levels and expand their gallery size beyond the default limit.

---

## Token Costs

### Picture Unlocks:
- **FLIRTY Pictures**: 50 tokens
  - Unlocks suggestive/teasing pictures
  - Cleavage, lingerie, seductive poses
  
- **INTIMATE Pictures**: 150 tokens
  - Unlocks explicit/nude pictures
  - Full nudity, sexual content
  - Auto-unlocks FLIRTY if not already unlocked

### Gallery Expansion:
- **Cost**: 30 tokens per slot
- **Default Limit**: 6 pictures
- **Maximum Limit**: 30 pictures
- **Can buy**: Multiple slots at once

---

## Default State

**New User:**
- ✅ CASUAL pictures: Always available
- ❌ FLIRTY pictures: Locked (50 tokens)
- ❌ INTIMATE pictures: Locked (150 tokens)
- 📸 Gallery: 6 slots

---

## API Endpoints

### 1. Unlock Picture Level
**Endpoint:** `POST /api/unlock-pictures`

**Request:**
```json
{
  "session_id": "user123",
  "picture_level": "FLIRTY"  // or "INTIMATE"
}
```

**Response (Success):**
```json
{
  "status": "success",
  "message": "FLIRTY pictures unlocked!",
  "tokens_remaining": 25,
  "unlocked_pictures": ["FLIRTY"],
  "gallery_limit": 6
}
```

**Response (Error - Not Enough Tokens):**
```json
{
  "error": "Not enough tokens. Need 50, have 25",
  "tokens_needed": 25
}
```

---

### 2. Expand Gallery
**Endpoint:** `POST /api/expand-gallery`

**Request:**
```json
{
  "session_id": "user123",
  "slots": 3  // Number of slots to add (optional, default 1)
}
```

**Response (Success):**
```json
{
  "status": "success",
  "message": "Gallery expanded by 3 slot(s)!",
  "tokens_remaining": 10,
  "new_gallery_limit": 9,
  "slots_added": 3,
  "cost": 90
}
```

**Response (Error - Not Enough Tokens):**
```json
{
  "error": "Not enough tokens. Need 90, have 60",
  "tokens_needed": 30,
  "max_affordable_slots": 2
}
```

---

### 3. Get Token Status
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
  "tokens": 75,
  "unlocked_pictures": ["FLIRTY"],
  "gallery_limit": 6,
  "max_gallery_limit": 30,
  "available_picture_unlocks": [
    {
      "level": "INTIMATE",
      "cost": 150,
      "affordable": false
    }
  ],
  "gallery_expansion": {
    "cost_per_slot": 30,
    "max_affordable_slots": 2,
    "can_expand": true,
    "slots_remaining": 24
  }
}
```

---

## Helper Functions

### Check Picture Level Access
```python
can_send_picture_level(session_id, level)
# Returns: True if level is unlocked
# CASUAL is always True
# FLIRTY/INTIMATE requires unlock
```

### Get Gallery Limit
```python
get_gallery_limit(session_id)
# Returns: Current gallery size limit (default 6)
```

### Get Unlocked Picture Levels
```python
get_unlocked_picture_levels(session_id)
# Returns: set(['FLIRTY', 'INTIMATE'])
```

---

## Usage Examples

### Example 1: Unlock FLIRTY Pictures

**User has 75 tokens**

1. User clicks "Unlock FLIRTY Pictures" button
2. Frontend calls: `POST /api/unlock-pictures`
   ```json
   {"session_id": "user123", "picture_level": "FLIRTY"}
   ```
3. Backend:
   - Checks balance: 75 >= 50 ✅
   - Deducts 50 tokens
   - Adds 'FLIRTY' to unlocked set
   - Returns success

4. User now has:
   - 25 tokens remaining
   - FLIRTY pictures unlocked
   - Can request suggestive pictures

---

### Example 2: Unlock INTIMATE Pictures

**User has 200 tokens**

1. User clicks "Unlock INTIMATE Pictures"
2. Frontend calls: `POST /api/unlock-pictures`
   ```json
   {"session_id": "user123", "picture_level": "INTIMATE"}
   ```
3. Backend:
   - Checks balance: 200 >= 150 ✅
   - Deducts 150 tokens
   - Adds 'INTIMATE' to unlocked set
   - Auto-adds 'FLIRTY' (if not already unlocked)
   - Returns success

4. User now has:
   - 50 tokens remaining
   - Both FLIRTY and INTIMATE unlocked
   - Can request explicit pictures

---

### Example 3: Expand Gallery

**User has 100 tokens, wants 3 more slots**

1. User clicks "Expand Gallery (+3)"
2. Frontend calls: `POST /api/expand-gallery`
   ```json
   {"session_id": "user123", "slots": 3}
   ```
3. Backend:
   - Calculates cost: 3 × 30 = 90 tokens
   - Checks balance: 100 >= 90 ✅
   - Deducts 90 tokens
   - Increases limit: 6 → 9
   - Returns success

4. User now has:
   - 10 tokens remaining
   - Gallery limit: 9 pictures
   - Can save 3 more pictures

---

### Example 4: Check What's Affordable

**User has 60 tokens**

1. Frontend calls: `POST /api/token-status`
2. Backend returns:
   ```json
   {
     "tokens": 60,
     "unlocked_pictures": [],
     "available_picture_unlocks": [
       {"level": "FLIRTY", "cost": 50, "affordable": true},
       {"level": "INTIMATE", "cost": 150, "affordable": false}
     ],
     "gallery_expansion": {
       "cost_per_slot": 30,
       "max_affordable_slots": 2,
       "can_expand": true
     }
   }
   ```

3. UI shows:
   - ✅ Can unlock FLIRTY (50 tokens)
   - ❌ Cannot unlock INTIMATE (need 90 more)
   - ✅ Can expand gallery by 2 slots

---

## Token Earning

**Users earn tokens through:**
- Base: 2 tokens per message
- Bonus: +1 token for compliments
- Total: ~2-3 tokens per message

**Time to unlock:**
- FLIRTY: ~17-25 messages (50 tokens)
- INTIMATE: ~50-75 messages (150 tokens)
- Gallery slot: ~10-15 messages (30 tokens)

---

## Frontend Integration

### Display Token Shop
```javascript
// Get current status
fetch('/api/token-status', {
  method: 'POST',
  body: JSON.stringify({session_id: sessionId})
})
.then(res => res.json())
.then(data => {
  // Show tokens: data.tokens
  // Show unlocked: data.unlocked_pictures
  // Show gallery: data.gallery_limit
  // Show what's affordable
});
```

### Unlock Picture Level
```javascript
function unlockPictures(level) {
  fetch('/api/unlock-pictures', {
    method: 'POST',
    body: JSON.stringify({
      session_id: sessionId,
      picture_level: level
    })
  })
  .then(res => res.json())
  .then(data => {
    if (data.status === 'success') {
      alert(data.message);
      updateTokenDisplay(data.tokens_remaining);
    } else {
      alert(data.error);
    }
  });
}
```

### Expand Gallery
```javascript
function expandGallery(slots) {
  fetch('/api/expand-gallery', {
    method: 'POST',
    body: JSON.stringify({
      session_id: sessionId,
      slots: slots
    })
  })
  .then(res => res.json())
  .then(data => {
    if (data.status === 'success') {
      alert(data.message);
      updateGalleryLimit(data.new_gallery_limit);
    } else {
      alert(data.error);
    }
  });
}
```

---

## Benefits

### For Users:
- **Clear Progression**: Know exactly what tokens unlock
- **Flexible Spending**: Choose pictures or gallery
- **Visible Value**: See what's affordable
- **No Surprises**: Clear costs upfront

### For Monetization:
- **Multiple Sinks**: Pictures AND gallery
- **Recurring Value**: Gallery can expand 24 times
- **Tiered Pricing**: FLIRTY cheaper than INTIMATE
- **Encourages Engagement**: Need to chat to earn

### For Gameplay:
- **Meaningful Choices**: Spend on pictures or gallery?
- **Progression Feel**: Unlock new content over time
- **Reward System**: Tokens feel valuable
- **Gallery Management**: Limited space creates curation

---

## Constants

```python
# Picture unlock costs
PICTURE_UNLOCK_COSTS = {
    'FLIRTY': 50,
    'INTIMATE': 150
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

## Storage

```python
# Session-based storage
unlocked_picture_levels = {}  # {session_id: set(['FLIRTY', 'INTIMATE'])}
gallery_limits = {}           # {session_id: int}
intimacy_tokens = {}          # {session_id: int}
```

---

## Auto-Unlock Logic

**When unlocking INTIMATE:**
- Automatically unlocks FLIRTY (if not already)
- User doesn't pay twice
- Ensures progression makes sense

**Example:**
- User has 150 tokens
- Unlocks INTIMATE directly
- Gets both FLIRTY and INTIMATE
- Pays only 150 tokens (not 200)

---

## Error Handling

**Not Enough Tokens:**
```json
{
  "error": "Not enough tokens. Need 50, have 25",
  "tokens_needed": 25
}
```

**Already Unlocked:**
```json
{
  "error": "FLIRTY pictures already unlocked"
}
```

**Gallery at Max:**
```json
{
  "error": "Gallery already at maximum size (30)"
}
```

**Invalid Level:**
```json
{
  "error": "Invalid picture level"
}
```

---

## Summary

**Complete token unlock system for pictures and gallery:**
- ✅ 3 API endpoints (unlock, expand, status)
- ✅ Picture level unlocks (FLIRTY, INTIMATE)
- ✅ Gallery expansion (6 → 30 slots)
- ✅ Token cost system (50, 150, 30)
- ✅ Helper functions for access checks
- ✅ Auto-unlock logic (INTIMATE → FLIRTY)
- ✅ Comprehensive error handling
- ✅ Frontend-ready JSON responses

**Users can now spend tokens to unlock picture intimacy levels and expand their gallery beyond 6 pictures!** 💰📸✨
