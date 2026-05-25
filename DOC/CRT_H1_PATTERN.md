# CANDLE RANGE THEORY (CRT) - H1 PATTERN
**Machine-First | IA Compatible | Complete Pattern Definition**

---

## FOUNDATION: WHAT IS CANDLE RANGE THEORY?

### Core Concept

Each candle on a higher timeframe represents a **range (gamme)** on a lower timeframe.

```yaml
candle_structure:
  CRT_High: The highest point of the range
  CRT_Low: The lowest point of the range
  
principle: |
  Market performs "liquidity raid" on previous candle's range
  before moving to next liquidity level.
  
  Example: If price takes liquidity at CRT_Low,
  it will likely target CRT_High next.
```

---

## BEARISH CRT PATTERN (H1)

### Complete Definition

```yaml
bearish_crt_conditions:
  1_first_candle: Bullish (close[1] > open[1])
  2_second_candle: Bearish (close < open)
  3_second_high_exceeds: high > high[1]  ← CRITICAL: Must break above first candle
  4_close_in_range: (close > low[1]) AND (close < high[1])
  
pine_script_v6: |
  h1_bearish_crt = (close[1] > open[1]) 
                   AND (close < open)
                   AND (high > high[1])
                   AND (close > low[1])
                   AND (close < high[1])
```

### Logic Sequence

```
Bar[1]: BULLISH candle
        └─ Sets CRT range: [low[1] ... high[1]]

Bar[0]: BEARISH candle
        ├─ Opens somewhere in range
        ├─ Takes liquidity HIGH (high > high[1])  ← Liquidity raid
        └─ Closes INSIDE range (low[1] < close < high[1])
        
Result: Bearish structure formed, setup complete
```

### Visual Signal

```
        ▼ ← Red triangle above candles (bearish CRT)
      ┌───┐
      │ B │ ← Bearish bar (takes HIGH then closes inside)
      └───┘
      ┌───┐
      │ B │ ← Previous bullish bar (range established)
      └───┘
```

---

## BULLISH CRT PATTERN (H1)

### Complete Definition

```yaml
bullish_crt_conditions:
  1_first_candle: Bearish (close[1] < open[1])
  2_second_candle: Bullish (close > open)
  3_second_low_below: low < low[1]  ← CRITICAL: Must break below first candle
  4_close_in_range: (close > low[1]) AND (close < high[1])
  
pine_script_v6: |
  h1_bullish_crt = (close[1] < open[1])
                   AND (close > open)
                   AND (low < low[1])
                   AND (close > low[1])
                   AND (close < high[1])
```

### Logic Sequence

```
Bar[1]: BEARISH candle
        └─ Sets CRT range: [low[1] ... high[1]]

Bar[0]: BULLISH candle
        ├─ Opens somewhere in range
        ├─ Takes liquidity LOW (low < low[1])  ← Liquidity raid
        └─ Closes INSIDE range (low[1] < close < high[1])
        
Result: Bullish structure formed, setup complete
```

### Visual Signal

```
      ┌───┐
      │ B │ ← Bullish bar (takes LOW then closes inside)
      └───┘
      ▲ ← Green triangle below candles (bullish CRT)
      ┌───┐
      │ B │ ← Previous bearish bar (range established)
      └───┘
```

---

## CRITICAL DISTINCTION: THE LIQUIDITY RAID

```yaml
common_mistake: |
  "CRT is just a candle closing inside previous range"
  
WRONG: This is incomplete.

correct_understanding: |
  CRT = Previous range + LIQUIDITY RAID + Close inside range
  
liquidity_raid_definition:
  bearish_crt: Takes HIGH liquidity (high > high[1])
  bullish_crt: Takes LOW liquidity (low < low[1])
  
why_it_matters: |
  The raid proves market accepted the reversal.
  Without it, it's just a normal inside-range close.
  The raid validates the structural change.
```

---

## CURRENT CODE vs CORRECT IMPLEMENTATION

### Current Implementation (INCOMPLETE)

```pine
h1_bullish_crt = (close[1] < open[1]) and (close > open) and (close > low[1]) and (close < high[1])
h1_bearish_crt = (close[1] > open[1]) and (close < open) and (close > low[1]) and (close < high[1])
```

❌ **Missing**:
- Bearish: `high > high[1]` (liquidity raid on HIGH)
- Bullish: `low < low[1]` (liquidity raid on LOW)

### Correct Implementation (COMPLETE)

```pine
h1_bullish_crt = (close[1] < open[1]) 
                 AND (close > open) 
                 AND (low < low[1])      ← ADD THIS
                 AND (close > low[1]) 
                 AND (close < high[1])

h1_bearish_crt = (close[1] > open[1]) 
                 AND (close < open) 
                 AND (high > high[1])    ← ADD THIS
                 AND (close > low[1]) 
                 AND (close < high[1])
```

---

## VERIFICATION CHECKLIST

```yaml
verify_bearish_crt:
  □ Is bar[1] bullish? (close[1] > open[1])
  □ Is bar[0] bearish? (close < open)
  □ Does bar[0] HIGH exceed bar[1] HIGH? (high > high[1])
  □ Does bar[0] close INSIDE bar[1] range? (low[1] < close < high[1])
  
verify_bullish_crt:
  □ Is bar[1] bearish? (close[1] < open[1])
  □ Is bar[0] bullish? (close > open)
  □ Does bar[0] LOW go BELOW bar[1] LOW? (low < low[1])
  □ Does bar[0] close INSIDE bar[1] range? (low[1] < close < high[1])
```

---

## EXPECTED BEHAVIOR ON CHARTS

```yaml
H1_chart_display:
  bearish_crt:
    symbol: ▼ (Red triangle)
    position: Above candles
    trigger: After 2-candle pattern completes
    
  bullish_crt:
    symbol: ▲ (Green triangle)
    position: Below candles
    trigger: After 2-candle pattern completes
    
frequency: Multiple per day on H1
reliability: High when followed by M15 swing + M1 FVG
```

---

## ALGORITHM: CRT DETECTION FLOW

```
On every H1 candle close:

  // Check for BEARISH CRT
  IF (close[1] > open[1])              // Prev bullish
     AND (close < open)                // Current bearish
     AND (high > high[1])              // HIGH liquidity raid ← KEY
     AND (close > low[1])              // Close above prev low
     AND (close < high[1]):            // Close below prev high
    
    → h1_bearish_crt = TRUE
    → Display red triangle above
    → Signal available for M15 cascade
  
  // Check for BULLISH CRT (inverse)
  IF (close[1] < open[1])              // Prev bearish
     AND (close > open)                // Current bullish
     AND (low < low[1])                // LOW liquidity raid ← KEY
     AND (close > low[1])              // Close above prev low
     AND (close < high[1]):            // Close below prev high
    
    → h1_bullish_crt = TRUE
    → Display green triangle below
    → Signal available for M15 cascade
```

---

## IMPORTANCE IN V3.1 CASCADE

```yaml
cascade_requirement:
  H1_CRT:
    - Must be detected first
    - Sets direction (bullish/bearish)
    - Gates M15 swing filter
    
  M15_SWING:
    - Must align with H1 CRT direction
    - Must occur in same hour
    - Gates M1 FVG
    
  M1_FVG_RETRACE:
    - Must align with both H1+M15
    - Completes signal validation
    
broken_cascade_causes: |
  If H1 CRT detection is incomplete (missing liquidity raid check),
  false signals propagate through entire cascade.
  This is why signals were firing incorrectly.
```

---

## REFERENCES

| Reference | Status |
|-----------|--------|
| CRT Indicator 1.5 (TradingView) | ✅ Working example (no source access) |
| ICT/SMC Documentation | ✅ Source material |
| Pine Script v6 | ✅ Implementation language |
| FVG_AND_RETRACEMENT.md | ✅ Related concept |
| FILTRAGE_H1_M1_CONDITIONS.md | ⚠️ Needs update |

---

**Last Updated**: 2026-05-25  
**Status**: CRITICAL - Implementation fix required  
**Priority**: HIGH - This affects entire signal cascade  
**Author**: Laurent (Corrected from ICT/SMC sources)  
**Compatibility**: Pine Script v6, Machine-First, IA-Ready
