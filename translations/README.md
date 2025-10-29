# Translation System

Modular translation system using JSON files for easy maintenance and extensibility.

## Structure

```
translations/
├── en.json       # English translations
├── zh.json       # Traditional Chinese translations
└── README.md     # This file
```

## Features

✅ **Modular** - Translations in separate JSON files  
✅ **Async Loading** - Loaded dynamically from server  
✅ **Fallback** - Embedded translations if loading fails  
✅ **Complete** - All UI text translated  
✅ **Maintainable** - Easy to edit and version control  

## Translation Keys

### Core UI
- `title` - Page title
- `welcomeTitle` - Welcome message title
- `welcomeText1` - Welcome message (with {name} placeholder)
- `welcomeText2` - Welcome message second line

### Age Verification
- `ageTitle` - Age verification title
- `ageWarning` - Warning text
- `ageQuestion` - Age question
- `ageYes` - Yes button
- `ageNo` - No button
- `ageConsent` - Consent text
- `ageAlert` - Alert message

### Name Modal
- `welcomeModalTitle` - Modal title
- `chooseGirlfriend` - Choose girlfriend label
- `nameLabel` - Name input label
- `namePlaceholder` - Name input placeholder
- `personalityLabel` - Personality label
- `hairColorLabel` - Hair color label
- `eyeColorLabel` - Eye color label
- `bodyShapeLabel` - Body shape label
- `breastSizeLabel` - Breast size label
- `outfitLabel` - Outfit label
- `pictureStyle` - Picture style label
- `createButton` - Create button text
- `customizeHint` - Customization hint

### Chat Interface
- `clearChat` - Clear chat button
- `messagePlaceholder` - Message input placeholder
- `sendButton` - Send button text

### Affection & Tokens
- `points` - Points label
- `tokens` - Tokens label
- `unlockFlirty` - Unlock flirty button
- `unlockIntimate` - Unlock intimate button

### Token Purchase
- `purchaseTitle` - Purchase modal title
- `purchaseMessage` - Purchase message
- `purchaseCancel` - Cancel button
- `purchaseBestValue` - Best value badge
- `purchaseBtn` - Purchase button
- `purchaseSuccess` - Success message (with {amount} placeholder)
- `insufficientTokens` - Insufficient tokens message

### Image Generation
- `sendingPhoto` - Sending photo message
- `failedToLoad` - Failed to load message
- `imageUnavailable` - Image unavailable message
- `comfyuiOffline` - ComfyUI offline message
- `generationTimeout` - Timeout message
- `checkComfyui` - Check ComfyUI message
- `generationFailed` - Generation failed message

### Other
- `startConversationFirst` - Start conversation first message

### Nested Objects

#### Personalities
```json
"personalities": {
  "shy": "Shy & Sweet",
  "playful": "Playful & Cute",
  "confident": "Bold & Confident",
  ...
}
```

#### Personality Greetings
```json
"personalityGreetings": {
  "shy": "*blushes* H-hi...",
  "playful": "Hiii~! ✨",
  ...
}
```

#### Outfits
```json
"outfits": {
  "casual": "Casual Clothes",
  "dress": "Cute Dress",
  ...
}
```

#### Compositions
```json
"compositions": {
  "face": "Face Only",
  "half": "Half Body",
  "full": "Full Body"
}
```

#### Presets
```json
"presets": {
  "luna": {
    "name": "Luna",
    "desc": "Shy & Sweet",
    "greeting": "..."
  },
  ...
}
```

## Usage

### Loading Translations

Translations are loaded automatically on page load:

```javascript
async function loadTranslations() {
    const [enData, zhData] = await Promise.all([
        fetch('/translations/en.json').then(r => r.json()),
        fetch('/translations/zh.json').then(r => r.json())
    ]);
    translations = { en: enData, zh: zhData };
}
```

### Using Translations

```javascript
const t = translations[currentLanguage];

// Simple text
element.textContent = t.welcomeTitle;

// With placeholder
element.textContent = t.welcomeText1.replace('{name}', name);

// Nested object
element.textContent = t.personalities.shy;
```

### Updating Title

```javascript
function updatePageTitle() {
    const t = translations[currentLanguage];
    document.title = t.title;
}
```

## Adding New Languages

1. Create new JSON file: `translations/xx.json`
2. Copy structure from `en.json`
3. Translate all values
4. Update Flask route to include new language:

```python
@app.route('/translations/<lang>.json')
def get_translation(lang):
    if lang not in ['en', 'zh', 'xx']:  # Add 'xx'
        return jsonify({"error": "Invalid language"}), 404
    ...
```

5. Update language selector in HTML

## Adding New Translation Keys

1. Add key to both `en.json` and `zh.json`:

```json
// en.json
{
  "newKey": "New English Text"
}

// zh.json
{
  "newKey": "新的中文文本"
}
```

2. Use in HTML/JavaScript:

```javascript
const t = translations[currentLanguage];
element.textContent = t.newKey;
```

## Placeholders

Use `{placeholder}` syntax for dynamic values:

```json
{
  "welcomeText": "Hi {name}, you have {points} points!"
}
```

Replace in code:

```javascript
text = t.welcomeText
  .replace('{name}', userName)
  .replace('{points}', userPoints);
```

## Fallback System

If JSON loading fails, embedded translations are used:

```javascript
try {
    // Load from JSON
    translations = await loadFromJSON();
} catch (error) {
    // Use embedded fallback
    translations = {
        en: { ... },
        zh: { ... }
    };
}
```

## Benefits

### Before (Embedded)
```javascript
// 300+ lines of translations in HTML
const translations = {
    en: {
        ageTitle: "...",
        ageWarning: "...",
        // ... 100 more keys
    },
    zh: {
        ageTitle: "...",
        ageWarning: "...",
        // ... 100 more keys
    }
};
```

**Problems:**
- Large HTML file
- Hard to maintain
- Difficult to version control
- No separation of concerns

### After (Modular)
```javascript
// Load from JSON
translations = await loadTranslations();
```

**Benefits:**
- ✅ Clean HTML
- ✅ Easy to edit
- ✅ Better version control
- ✅ Reusable translations
- ✅ Can be edited by non-developers

## File Sizes

- `en.json`: ~8KB
- `zh.json`: ~8KB
- Total: ~16KB (gzipped: ~4KB)

## Caching

Translations are cached by the browser:

```
Cache-Control: public, max-age=3600
```

Update cache by:
1. Modifying JSON files
2. Restarting Flask server
3. Hard refresh browser (Ctrl+F5)

## Translation Guidelines

### English
- Use natural, conversational language
- Keep it friendly and warm
- Use emojis appropriately

### Chinese (Traditional)
- Use Traditional Chinese characters (繁體中文)
- Maintain natural flow
- Keep cultural context appropriate
- Match tone and formality of English

## Testing

### Test Translation Loading
```javascript
console.log('[Translations] Loaded:', translations);
```

### Test Language Switch
1. Click language selector
2. Verify all text updates
3. Check title changes
4. Verify localStorage saves preference

### Test Fallback
1. Rename JSON files temporarily
2. Reload page
3. Verify embedded translations work
4. Check console for fallback message

## Troubleshooting

### Translations not loading
**Check:**
- JSON files exist in `translations/` folder
- Flask route `/translations/<lang>.json` works
- Browser console for errors
- Network tab shows 200 response

### Text not updating
**Check:**
- Translation key exists in JSON
- `updateLanguage()` is called
- `currentLanguage` variable is correct
- Element selector is correct

### Title not translating
**Check:**
- `title` key exists in JSON
- `updatePageTitle()` is called
- `pageTitle` element ID exists
- `loadTranslations()` completed

## Future Enhancements

- [ ] Add more languages (Japanese, Korean, Spanish, etc.)
- [ ] Translation validation script
- [ ] Missing key detection
- [ ] Translation coverage report
- [ ] Automatic translation suggestions
- [ ] Translation memory/glossary

## Maintenance

### Updating Translations
1. Edit JSON files
2. Commit changes
3. Deploy
4. Users get updates on next page load

### Adding Keys
1. Add to all language files
2. Update code to use new keys
3. Test in both languages

### Removing Keys
1. Remove from code first
2. Then remove from JSON files
3. Verify no references remain
