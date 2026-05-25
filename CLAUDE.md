# CLAUDE.md - Project Configuration

## 🎯 Project Goal
V3.1 Signal Validation: Test Pine Script signal logic (H1 CRT + M15 SWING + M1 FVG) in TradingView.

---

## 🤖 Auto-Deploy Workflow

### Why?
You'll iterate the Pine Script many times. Manual copy/paste/compile is tedious.

### Setup (One-time)

#### 1. Install Dependencies
```powershell
pip install watchdog pyautogui keyboard pywin32
```

#### 2. Start Auto-Deploy
From the project folder:
```powershell
python auto_deploy_pine.py
```

**What it does:**
- Launches TradingView (if not running) with debug port
- Opens Pine Script Editor
- Watches `SCALPING_INDICATOR_V3_1_SIGNAL_VALIDATION.pine` for changes
- On save: auto-copies code → compiles → applies to M1
- Continuous monitoring until you Ctrl+C

### Usage (Iterative)

**Workflow:**
```
1. Edit SCALPING_INDICATOR_V3_1_SIGNAL_VALIDATION.pine in your editor
   (VS Code, vim, whatever)

2. Save file

3. auto_deploy_pine.py detects change → auto-deploys

4. Check TradingView M1 chart for:
   - ✓ No compile errors (Status bar)
   - ✓ FVG boxes appear (green/red)
   - ✓ Debug labels show (if enabled)
   - ✓ BUY/SELL diamonds appear on valid cascade

5. Iterate step 1-4 until signals are correct
```

---

## 📋 Validation Checklist (V3.1)

Before deploying each iteration:
- [ ] Pine compiles with 0 errors
- [ ] FVG boxes visible on M1
- [ ] H1 CRT labels appear when condition met
- [ ] M15 SWING labels align with H1 CRT
- [ ] BUY/SELL signals appear ONLY when all 3 conditions met
- [ ] No false positives (signals without all 3 conditions)
- [ ] Alerts trigger on bar close

---

## 🖥️ TradingView Workflow

### Setup (One-time)

**Install Python dependencies:**
```powershell
pip install pyautogui pyperclip
```

---

### Deploy Steps (For each indicator)

#### 1️⃣ **In TradingView Desktop**

Open the chart where you want the indicator:
- M1 for: FVG M1, CRT H1, STRAT_HUGO_V1
- M15 for: SWING M15
- H1 for: CRT H1 (if viewing alone)

Click **"Indicateurs"** → **"Pine Script Editor"** → **"+"** button

Give it a name matching the script you're deploying:
```
LOLO_SWING_M15
LOLO_FVG_M1
LOLO_CRT_H1
LOLO_STRAT_HUGO_V1
```

The editor opens **blank**. Leave it open.

#### 2️⃣ **From Command Line**

```powershell
cd "C:\Users\Laurent\Desktop\PROJET TRADING"
python deploy_safe.py LOLO_SWING_M15.pine
```

Or for any script:
```powershell
python deploy_safe.py SCRIPT_NAME.pine
```

**What happens:**
- Code reads from disk → copies to clipboard
- Clicks inside Pine Editor
- Pastes code → Selects all → Saves
- Compiles automatically

#### 3️⃣ **Verify in TradingView**

- ✅ Code appears in Pine Editor
- ✅ Status: "Compiled clean — 0 errors"
- ✅ Click **"Ajouter au Graphique"** (Add to Chart)
- ✅ Labels/boxes appear on chart

---

### Quick Reference

| Indicator | Deploy Command | Target Chart |
|-----------|---|---|
| SWING M15 | `python deploy_safe.py LOLO_SWING_M15.pine` | M15 |
| FVG M1 | `python deploy_safe.py LOLO_FVG_M1.pine` | M1 |
| CRT H1 | `python deploy_safe.py LOLO_CRT_H1.pine` | H1 |
| STRAT V1 | `python deploy_safe.py LOLO_STRAT_HUGO_V1.pine` | M1 |

---

## 🔧 Configuration

### Chart Setup
- **Left**: H1 (for debug labels)
- **Right**: M1 (main signal display)
- **Instrument**: BTCUSD (or your choice)

### Pine Settings
```
show_debug: true  (see H1/M15 cascade)
show_fvg: true    (see M1 gaps)
one_signal_per_bar: true  (signal only on bar close)
```

### Test Signal Conditions
```
BUY Signal needs:
  1. H1: CRT bullish (prev bearish + curr bullish in prev range)
  2. M15: Swing low pattern (HL > LL > HH with bull close)
  3. M1: FVG bull (high[2] < low)

SELL Signal needs (inverse):
  1. H1: CRT bearish
  2. M15: Swing high pattern
  3. M1: FVG bear
```

---

## 🐛 Troubleshooting

### Script won't launch TradingView
- Manually open TradingView with: `TradingView.exe --remote-debugging-port=9222`
- Script will still auto-deploy to open window


### Signals not appearing despite correct conditions
1. Check if indicator is applied to **M1 only** (not H1)
2. Check `show_debug=true` to see H1/M15 labels
3. Verify `one_signal_per_bar=true` (edge detection)
4. Look for FVG boxes first - if none, M1 condition isn't met

### Auto-deploy stops responding
- Press Ctrl+C to stop
- Restart: `python auto_deploy_pine.py`

---

## 📚 Indicators & Files

### Core Indicators

| File | Purpose | TF | Display |
|------|---------|-----|---------|
| `LOLO_SWING_M15.pine` | Swing High/Low detection | M15 | Lines + Labels |
| `LOLO_FVG_M1.pine` | Fair Value Gap detection | M1 | Boxes + Midlines |
| `LOLO_CRT_H1.pine` | Candle Range Theory detection | H1 | Labels (up/down) |
| `LOLO_STRAT_HUGO_V1.pine` | **COMBINED** (CRT H1 + SWING M15 + FVG M1 on M1 chart) | M1 + H1 + M15 via request.security() | All 3 on M1 |

### Reference & Documentation

| File | Purpose |
|------|---------|
| `CRT_H1_PATTERN.md` | Complete CRT definition + liquidity raid logic |
| `FILTRAGE_H1_M1_CONDITIONS.md` | Cascade correlation rules |
| `START.md` | V3.1 signal validation workflow |
| `FVG_AND_RETRACEMENT.md` | FVG retracement rules |

### Deploy Script

| File | Purpose |
|------|---------|
| `deploy_safe.py` | **ONLY** deploy script — safe paste to Pine Editor |

---

---

## 🔄 CURRENT PROJECT STATUS

### ✅ COMPLETED

1. **LOLO_SWING_M15.pine** 
   - Detects Swing High/Low on M15
   - Displays lines + labels
   - Working standalone ✓

2. **LOLO_FVG_M1.pine**
   - Detects Bullish/Bearish FVG on M1
   - Displays boxes + midlines
   - Working standalone ✓

3. **LOLO_CRT_H1.pine**
   - Detects Bullish/Bearish CRT on H1 (with liquidity raid validation)
   - Displays labels (up/down)
   - Working standalone ✓

### 🚧 IN PROGRESS

**LOLO_STRAT_HUGO_V1.pine** (Combining all 3)
- Goal: Display CRT H1 + SWING M15 + FVG M1 on single M1 chart
- Challenge: Use request.security() to pull H1/M15 data without chaos
- Status: Code deployed but labels appearing "anarchically" during bar formation
- Next: Fix label detection to only trigger ONCE per bar H1/M15 change, not every M1 bar

### 🎯 STRATEGY

**Goal**: Create single M1 chart showing:
- H1 CRT labels (when detected on H1)
- M15 SWING labels (when detected on M15)  
- M1 FVG boxes (when detected on M1)

Then validate CASCADE: All 3 conditions + retracement = BUY/SELL signal

---

## 🎓 Workflow Examples

### Example 1: Fix H1 CRT Logic
```
1. Edit .pine file (change H1 CRT condition)
2. Save
3. Script auto-deploys
4. Watch H1 chart for "H1 CRT BULL/BEAR" labels
5. If not appearing, adjust logic, save, repeat
```

### Example 2: Debug Why BUY Not Firing
```
1. Enable show_debug=true in Pine inputs
2. Check H1 chart: is "H1 CRT BULL" label there?
3. Check M15 chart: is "H1+M15 BULL" label there?
4. Check M1 chart: are FVG boxes there?
5. If any missing, edit .pine to fix that condition
6. Save → auto-deploys → re-check
```

---

## 📝 Notes

- **TradingView stays open** between iterations (don't close it)
- **Chart settings persist** across deployments
- **Indicators on old code persist** until you re-apply new code
- **You can test multiple versions** by switching branches in git

---

**Last Updated**: 2026-05-26  
**Version**: 3.1 (Signal Validation + LOLO variants)  
**Deploy Methods**: Auto-deploy (V3.1) + Quick-deploy (standalone)
