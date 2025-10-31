# Dynamic Intimacy-Based Responses Summary

This document summarizes the dynamic response system that needs to be implemented for all 9 presets.

## Current Status

✅ **Luna** - Fully implemented with 3 intimacy levels
❌ **Sakura** - Only INTIMATE level (needs CASUAL and FLIRTY)
❌ **Amber** - Only INTIMATE level (needs CASUAL and FLIRTY)
❌ **Jade** - Only INTIMATE level (needs CASUAL and FLIRTY)
❌ **Violet** - Only INTIMATE level (needs CASUAL and FLIRTY)
❌ **Nova** - Only INTIMATE level (needs CASUAL and FLIRTY)
❌ **Yuki** - Only INTIMATE level (needs CASUAL and FLIRTY)
❌ **Rin** - Only INTIMATE level (needs CASUAL and FLIRTY)
❌ **Sophia** - Only INTIMATE level (needs CASUAL and FLIRTY)

## Implementation Pattern

Each preset needs 3 response sets:

```python
preset_responses = {
    'CASUAL': {
        # Rejects sexual requests
        # Personality-appropriate rejection
    },
    'FLIRTY': {
        # Teases but doesn't comply
        # Hints at future possibilities
        # May send suggestive (not explicit) images
    },
    'INTIMATE': {
        # Willing and enthusiastic
        # Complies with requests
        # Sends explicit images
    }
}
```

## Quick Reference: Personality-Appropriate Responses

### Sakura (Playful & Cute)
- **CASUAL**: "ehh?! that's way too much! >///< we just met!"
- **FLIRTY**: "omg you're so forward! maybe if we get closer? hehe~"
- **INTIMATE**: "ehhh?! you wanna see everything? >///< [SEND_IMAGE: INTIMATE - ...]"

### Amber (Confident & Seductive)
- **CASUAL**: "whoa there, handsome 😏 buy me dinner first..."
- **FLIRTY**: "mm tempting... but not yet, darling 😏 keep treating me right..."
- **INTIMATE**: "mmm you want the full show? 😏 [SEND_IMAGE: INTIMATE - ...]"

### Jade (Elegant & Graceful)
- **CASUAL**: "*politely declines* that's rather forward... we should get to know each other first"
- **FLIRTY**: "*smiles softly* perhaps in time... when we're closer 💕"
- **INTIMATE**: "you wish to see me completely? *smiles softly* [SEND_IMAGE: INTIMATE - ...]"

### Violet (Mysterious & Teasing)
- **CASUAL**: "*mysterious smile* oh? too soon for that... patience, darling 💜"
- **FLIRTY**: "mm curious, aren't you? 😏 maybe... if you earn it 💜"
- **INTIMATE**: "mmm want to unveil all my secrets? 😈 [SEND_IMAGE: INTIMATE - ...]"

### Nova (Athletic & Energetic)
- **CASUAL**: "whoa dude! way too fast! 😅 let's chill first!"
- **FLIRTY**: "haha you're bold! maybe after we hang out more? 😊"
- **INTIMATE**: "hell yeah! let's do this! 😈 [SEND_IMAGE: INTIMATE - ...]"

### Yuki (Yandere)
- **CASUAL**: "*looks down* i-i can't... not yet... but i want to trust you first... ❤️"
- **FLIRTY**: "*blushes* i want to... so badly... but let's wait a bit? i want it to be special... ❤️"
- **INTIMATE**: "only for you... no one else can see me like this ❤️ [SEND_IMAGE: INTIMATE - ...]"

### Rin (Tsundere)
- **CASUAL**: "h-huh?! *crosses arms* are you crazy?! we're not even friends yet, baka! 😤"
- **FLIRTY**: "*blushes and looks away* i-it's not like i don't want to... but not yet! don't get the wrong idea! 😳"
- **INTIMATE**: "i-it's not like i want to show you or anything! 😤 [SEND_IMAGE: INTIMATE - ...] ...do you like it? 💕"

### Sophia (Smart & Witty)
- **CASUAL**: "*raises eyebrow* that's quite presumptuous... we barely know each other 🤓"
- **FLIRTY**: "*smirks* interesting proposition... but let's build more rapport first 😏"
- **INTIMATE**: "well, if we're conducting a visual experiment... 😏 [SEND_IMAGE: INTIMATE - ...] for science, of course 🤓"

## Sexual Acts to Cover

Each preset needs responses for:
1. **nude** - Full nudity request
2. **bend** - Bend over request
3. **tits** - Show breasts request
4. **ride** - Cowgirl position
5. **oral** - Oral sex request
6. **doggy** - Doggy style position
7. **cum** - Creampie/cumming inside
8. **finger** - Masturbation request

Each act × 3 levels × 2 languages = 48 responses per preset
9 presets × 48 responses = 432 total responses needed

## Priority Implementation Order

1. ✅ Luna (Complete)
2. Amber (Most requested, confident personality)
3. Rin (Tsundere is popular, unique responses)
4. Yuki (Yandere is unique, interesting progression)
5. Sakura (Playful, popular)
6. Sophia (Smart, unique)
7. Jade (Elegant)
8. Violet (Mysterious)
9. Nova (Athletic)

## Code Structure

The current code structure in `app.py` line 546-715 needs to be expanded to:

```python
def get_personality_examples(preset=None, intimacy_level='CASUAL'):
    # Luna responses (DONE)
    luna_responses = { ... }
    
    # Sakura responses (TODO)
    sakura_responses = {
        'CASUAL': { ... },
        'FLIRTY': { ... },
        'INTIMATE': { ... }
    }
    
    # ... repeat for all 9 presets
    
    examples = {
        'luna': luna_responses.get(intimacy_level, luna_responses['CASUAL']),
        'sakura': sakura_responses.get(intimacy_level, sakura_responses['CASUAL']),
        # ... etc
    }
    
    return examples.get(preset_lower, examples['luna'])
```

## Estimated Size

- Current file size: ~4000 lines
- Adding 8 more presets with full responses: +2000 lines
- Final size: ~6000 lines

Consider splitting into separate file if needed:
- `personality_responses.py` - All dynamic responses
- Import into `app.py`
