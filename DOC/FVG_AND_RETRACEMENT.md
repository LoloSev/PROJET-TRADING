# FAIR VALUE GAP (FVG) & RETRACEMENT
**Machine-First | IA Compatible | V3.1 Critical for Trade Validation**

---

## DEFINITION: FAIR VALUE GAP

### What is an FVG?

A Fair Value Gap is a **gap in market price** created during aggressive buying or selling.

```yaml
FVG_creation:
  trigger: Aggressive buying (for bull FVG) or selling (for bear FVG)
  result: Price moves rapidly, creating untouched price levels
  zone: Between the high of candle before gap AND low of candle after gap
  
FVG_bull:
  - high[2] < low[0]  # High 2 bars ago is below current low
  - Creates zone from high[2] to low[0]
  - No price transaction occurred in this zone during the gap
  
FVG_bear:
  - low[2] > high[0]  # Low 2 bars ago is above current high
  - Creates zone from low[2] to high[0]
  - No price transaction occurred in this zone during the gap
```

---

## DEFINITION: RETRACEMENT

### Critical Concept

**Retracement = Price returns into the FVG zone**

```yaml
retracement_bull:
  condition: close > high[2] AND close < low[0]
  meaning: Price has entered the FVG zone (from below)
  depth: Can be shallow (just touching) or deep (50%+)
  
retracement_bear:
  condition: close > high[0] AND close < low[2]
  meaning: Price has entered the FVG zone (from above)
  depth: Can be shallow (just touching) or deep (50%+)
```

### Why Retracement Matters

**Without retracement = No trade validation**

```
Rule: NO RETRACEMENT = NO TRADE
─────────────────────────────────

Reason: You need to lean on the FVG as support/resistance
        
Scenario 1 (VALID):
  • H1 CRT BULL detected
  • M15 SWING LOW detected
  • M1 FVG BULL created
  • Price RETRACES into FVG zone ← Trader enters here
  • This is a trade setup

Scenario 2 (INVALID - NOT A TRADE):
  • H1 CRT BULL detected
  • M15 SWING LOW detected
  • M1 FVG BULL created
  • Price DOES NOT retrace into FVG ← NO ENTRY
  • Just because conditions aligned doesn't mean price validates them
```

---

## RETRACEMENT DEPTH EXPECTATION

```yaml
retracement_depth:
  minimum: ANY penetration into FVG zone
  no_minimum_depth: True
  
  example_shallow:
    - FVG zone: 10000 to 10020
    - Price retraces to 10019
    - Valid: Yes (touched FVG even if barely)
  
  example_deep:
    - FVG zone: 10000 to 10020
    - Price retraces to 10010 (midpoint)
    - Valid: Yes (50%+ penetration)
  
  critical_point: |
    Depth doesn't matter. Any retracement proves
    price respects the FVG as a structural level.
    Without it, the FVG is just a gap in vacuum.
```

---

## PINE SCRIPT IMPLEMENTATION

```pine
// FVG Detection
fvg_bull = high[2] < low       // Gap created
fvg_bear = low[2] > high       // Gap created

// Retracement Check (CRITICAL)
fvg_bull_retrace = fvg_bull and (close > high[2] and close < low)
fvg_bear_retrace = fvg_bear and (close > high and close < low[2])

// Final Signal REQUIRES both FVG + Retracement
buy_signal = m15_bull_ok and fvg_bull_retrace   // ← Must have retracement
sell_signal = m15_bear_ok and fvg_bear_retrace  // ← Must have retracement
```

**Key**: `fvg_bull_retrace` is NOT just `fvg_bull`. It validates that price **actually entered** the zone.

---

## VALIDATION CHECKLIST

```yaml
before_trade_entry:
  ✓ H1 CRT detected (correct direction)
  ✓ M15 SWING detected (correct direction, same hour)
  ✓ M1 FVG created (correct direction)
  ✓ Price HAS RETRACTED into FVG zone ← THIS IS REQUIRED
  
if_any_missing:
  ✗ No trade setup
  → Wait for next cascade alignment
```

---

## COMMON MISTAKES

```yaml
mistake_1_FVG_without_retracement:
  symptom: "FVG box appears but no signal fires"
  cause: Price never entered the FVG zone
  result: Not a valid trade setup (by design)
  
mistake_2_ignoring_retracement:
  symptom: "I want to trade on FVG creation alone"
  cause: Misunderstanding of retracement requirement
  result: Signals fire on every gap (tons of false entries)
  
mistake_3_confusing_retracement_depth:
  symptom: "Is my retracement deep enough?"
  truth: No minimum depth. Any penetration into zone = valid.
```

---

## ALGORITHM: RETRACEMENT FLOW

```
On every M1 candle close:

  IF fvg_bull created:
    ├─ Draw green box from high[2] to low
    └─ Monitor next candles for retracement
    
  IF price closes inside FVG_bull zone (close > high[2] AND close < low):
    └─ fvg_bull_retrace = TRUE
    
  IF fvg_bull_retrace AND h1_bullish_crt AND m15_swing_low:
    └─ FIRE BUY SIGNAL + Alert

(Inverse for bear)
```

---

## VISUAL REFERENCE

**Image 1: FVG Zone Definition**
- Shows FVG creation (gap between candles)
- Zone marked from high[2] to low (for bull FVG)
- Zone shaded in light blue

**Image 2: Retracement Scenarios**
- Buy scenario: Price retraces into FVG (signal fires when all 3 conditions + retracement)
- Sell scenario: Price retraces into FVG (inverse logic)
- Shows numbered sequence: 1) FVG created, 2) Price retraces, 3) Trade fires

---

## RELEVANCE TO V3.1

```yaml
V3.1_status: Signal Validation Build

current_implementation: ✓ Includes retracement filter
reason: Retracement is mandatory for any valid trade setup
not_optional: Removing it = invalid signals

future_phases:
  V4.0: Add entry rules (retracement depth thresholds, SL/TP)
  V5.0: Add risk management (position sizing, BE logic)
```

---

## CRITICAL RULE FOR IMPLEMENTATION

```
❗ NO RETRACEMENT → NO TRADE ❗

This is not a filter. This is the foundation.
Without retracement into FVG, the price has not validated
the market structure. The gap is just noise.

Implementation must REQUIRE both conditions:
  • FVG_creation (high[2] < low for bull)
  • AND retracement_into_fvg (close > high[2] AND close < low)

If either is missing: DO NOT FIRE SIGNAL
```

---

**Last Updated**: 2026-05-25  
**Author**: Laurent (ICT/SMC Methodology)  
**Compatibility**: Pine Script v6, Machine-First, IA-Ready  
**Status**: Required Reading for V3.1 Trade Validation
