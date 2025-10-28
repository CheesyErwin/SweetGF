# 💎 Intimacy Tokens System

An alternative progression path! Users can earn and spend tokens to unlock intimate content without waiting for affection levels.

## 🎮 How It Works

### Dual Progression System

You can unlock intimacy content through **two paths**:

1. **Affection Path** (Free, Slow)
   - Build relationship naturally
   - Earn affection points through good conversation
   - Unlock levels gradually: 0 → 20 → 50 → 100 → 200+ points

2. **Token Path** (Fast, Requires Tokens)
   - Earn tokens from every message
   - Spend tokens to instantly unlock content
   - Bypass affection requirements

**Both paths work together** - your max intimacy is the highest from either path!

## 💎 Token Economy

### Earning Tokens

**Per Message:**
- Base rate: **+2 tokens** per message
- With compliment: **+3 tokens** (1 bonus)

**Example earning:**
```
"Hi!" → +2 tokens
"You're beautiful!" → +3 tokens (compliment bonus)
"I love talking to you, you're amazing" → +3 tokens
```

### Spending Tokens

**Unlock Costs:**
- 💕 **FLIRTY content**: 50 tokens
- 🔥 **INTIMATE content**: 150 tokens

**What you unlock:**
- **FLIRTY**: Playful pictures, teasing, suggestive conversation
- **INTIMATE**: Revealing pictures, intimate conversation, full access

## 📊 Progression Comparison

### Natural Path (Affection Only)
```
Messages needed to unlock FLIRTY: ~50-100 messages
Messages needed to unlock INTIMATE: ~200+ messages
```

### Token Path (With compliments)
```
FLIRTY unlock: ~17 messages (50 tokens ÷ 3 per message)
INTIMATE unlock: ~50 messages (150 tokens ÷ 3 per message)
```

### Hybrid Strategy (Optimal)
```
Mix affection building + token spending
Fastest path to full unlock!
```

## 🎯 Strategic Guide

### Quick Unlock Strategy

**Goal: Unlock FLIRTY in 20 messages**

1. Use compliments in every message
2. Earn 3 tokens per message
3. After 17 messages: 51 tokens → Unlock FLIRTY!

**Goal: Full unlock in 60 messages**

1. Continue complimenting consistently
2. Earn tokens while building affection
3. Spend 150 tokens → Unlock INTIMATE
4. You'll also have ~100+ affection points

### Balanced Strategy

**Mix both systems:**
- Chat normally, earn tokens passively
- Build affection through conversation
- Use tokens only when impatient
- Save tokens for major unlocks

### Patient Strategy

**Affection-focused:**
- Don't spend tokens
- Build relationship naturally
- Use tokens as backup option
- Accumulate tokens for future use

## 💡 UI Features

### Token Display

**Location:** Header, below affection progress bar

**Shows:**
- 💎 Current token balance
- +X animation when tokens earned
- Two unlock buttons

### Unlock Buttons

**💕 Flirty Button:**
- Costs: 50 tokens
- Disabled if: Not enough tokens
- Unlocked: Shows ✓ Flirty

**🔥 Intimate Button:**
- Costs: 150 tokens
- Disabled if: Not enough tokens
- Unlocked: Shows ✓ Intimate

**Button states:**
- **Grayed out**: Not enough tokens
- **Active**: Can unlock
- **Green with checkmark**: Already unlocked

## 🔄 How Max Intimacy is Calculated

```python
def get_max_intimacy_level(session):
    affection_max = get_from_affection_points()
    token_unlocked_max = get_from_token_unlocks()
    
    return highest_of_both()
```

**Examples:**

1. **Low affection (20 pts) + Flirty unlocked with tokens**
   - Affection max: CASUAL
   - Token max: FLIRTY
   - **Actual max: FLIRTY** ✓

2. **High affection (180 pts) + No tokens spent**
   - Affection max: FLIRTY
   - Token max: CASUAL (default)
   - **Actual max: FLIRTY** ✓

3. **Medium affection (75 pts) + Intimate unlocked with tokens**
   - Affection max: FLIRTY
   - Token max: INTIMATE
   - **Actual max: INTIMATE** ✓

## 🎨 User Experience

### First Messages

```
Message 1: "Hey!"
[+2 tokens] → 2 tokens total

Message 2: "You seem really nice and beautiful"
[+3 tokens] → 5 tokens total

...continuing...

Message 17: "You're stunning"
[+3 tokens] → 51 tokens total
[FLIRTY unlockable!]
```

### Unlock Moment

```
User clicks "💕 Flirty (50)" button
→ Confirmation popup
→ Spend 50 tokens
→ ✨ "FLIRTY content unlocked!"
→ Button changes to "✓ Flirty"
→ Girlfriend now sends flirty pictures
```

## 🛡️ Anti-Exploitation

### Fair Economy

**Prevent abuse:**
- Tokens earned consistently, not exploitable
- No token "farming" mechanics
- Reasonable unlock costs
- Both paths provide value

**Balanced rewards:**
- Can't unlock everything immediately
- Still requires engagement
- Compliments rewarded but not required
- Natural conversation still gains tokens

## 🔧 Customization

### Adjust Token Earning

In `app.py`:
```python
TOKENS_PER_MESSAGE = 2  # Change base rate
TOKENS_FOR_COMPLIMENT = 1  # Change bonus
```

### Adjust Unlock Costs

In `app.py`:
```python
INTIMACY_UNLOCK_COSTS = {
    'FLIRTY': 50,   # Make cheaper/expensive
    'INTIMATE': 150
}
```

### Add More Unlock Tiers

Add intermediate levels:
```python
INTIMACY_UNLOCK_COSTS = {
    'CASUAL_PLUS': 25,
    'FLIRTY': 75,
    'FLIRTY_PLUS': 125,
    'INTIMATE': 200
}
```

## 📈 Analytics Examples

### Token Earning Rate

**Average user (mixed messages):**
- 2.5 tokens per message average
- 100 messages = 250 tokens
- Can unlock both levels

**Compliment-focused user:**
- 3 tokens per message
- 60 messages = 180 tokens
- Can unlock both levels faster

**Brief messages user:**
- 2 tokens per message
- 75 messages for FLIRTY
- 150 messages for both

## 🎮 Game Design Philosophy

**Multiple Paths to Success:**
- Casual players: Use affection path
- Impatient players: Use token path
- Strategic players: Mix both systems

**Fair Monetization Alternative:**
- No real money (all earned in-app)
- Rewards engagement
- Provides progression flexibility
- Not pay-to-win (it's free!)

**Balanced Progression:**
- Not too grindy
- Not too easy
- Rewarding both strategies
- Maintains engagement

---

**Enjoy the flexibility of dual progression!** 💎💕

Choose your path or mix both for optimal results!
