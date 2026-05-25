# FILTRAGE ENTONNOIR H1→M15→M1
**Version 3.0 | Machine-Readable | Pine Script v6**

---

## ARCHITECTURE EXÉCUTABLE

```yaml
NIVEAU_1_H1:
  condition: CRT (Candle Range Theory)
  
  bullish: (close[1] < open[1])       // Prev bearish
           AND (close > open)         // Curr bullish
           AND (low < low[1])         // Takes LOW liquidity (critical)
           AND (close > low[1])       // Close above prev low
           AND (close < high[1])      // Close below prev high
  
  bearish: (close[1] > open[1])       // Prev bullish
           AND (close < open)         // Curr bearish
           AND (high > high[1])       // Takes HIGH liquidity (critical)
           AND (close > low[1])       // Close above prev low
           AND (close < high[1])      // Close below prev high
  
NIVEAU_2_M15:
  swing_low: (close[2] < open[2]) AND (low[2] > low[1] < low[3]) AND (close > open)
  swing_high: (close[2] > open[2]) AND (high[2] < high[1] > high[3]) AND (low[2] < low[1] > low[3]) AND (close < open)
  cascade: SWING_BULL requires CRT_BULL in SAME_HOUR_H1
  cascade: SWING_BEAR requires CRT_BEAR in SAME_HOUR_H1

NIVEAU_3_M1:
  fvg_bull: high[2] < low
  fvg_bear: low[2] > high
  
  retracement_bull: fvg_bull AND (close > high[2]) AND (close < low)
  retracement_bear: fvg_bear AND (close > high) AND (close < low[2])

FINAL_SIGNALS:
  buy: CRT_BULL AND SWING_LOW AND RETRACEMENT_BULL
  sell: CRT_BEAR AND SWING_HIGH AND RETRACEMENT_BEAR
  
  CRITICAL_RULE: |
    NO RETRACEMENT = NO TRADE
    
    Retracement proves price respects FVG as structural level.
    Without it, FVG is just noise. Every component required:
    - FVG must exist
    - Price MUST retrace into zone (any depth)
    - H1 CRT must align
    - M15 SWING must align
```

---

## CORRÉLATION HORAIRE (CLEF)

```
CRT_H1 détecté dans heure H → Swing_M15 DOIT apparaître dans même heure H
  Si Swing après fin heure H → REJETÉ (cascade rompu)
  Si Swing avant CRT dans même heure → ATTENDRE CRT
  
Timing: CRT_H1 → Swing_M15 (H+15min, H+30min, H+45min) → FVG_M1 dans même heure
```

---

## REJECTION RULES

```
❌ SWING sans CRT correspondant dans même heure H1
❌ PRIX n'entre pas dans FVG
❌ FVG non créé avant retracement
❌ Swing direction ≠ CRT direction
```

---

**Pine Script Implementation:** SCALPING_INDICATOR_V3.pine  
**Status:** ✅ Testé et Validé
