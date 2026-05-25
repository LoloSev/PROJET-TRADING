# FILTRAGE ENTONNOIR H1→M15→M1
**Version 3.0 | Machine-Readable | Pine Script v6**

---

## ARCHITECTURE EXÉCUTABLE

```yaml
NIVEAU_1_H1:
  condition: CRT
  bullish: (close[1] < open[1]) AND (close > open) AND (close IN [low[1], high[1]])
  bearish: (close[1] > open[1]) AND (close < open) AND (close IN [low[1], high[1]])
  
NIVEAU_2_M15:
  swing_low: (close[2] < open[2]) AND (low[2] > low[1] < low[3]) AND (close > open)
  swing_high: (close[2] > open[2]) AND (high[2] < high[1] > high[3]) AND (low[2] < low[1] > low[3]) AND (close < open)
  cascade: SWING_BULL requires CRT_BULL in SAME_HOUR_H1
  cascade: SWING_BEAR requires CRT_BEAR in SAME_HOUR_H1

NIVEAU_3_M1:
  fvg_bull: high[2] < low
  fvg_bear: low[2] > high
  price_in_fvg_bull: (close > high[2]) AND (close < low) AND fvg_bull_created
  price_in_fvg_bear: (close > high) AND (close < low[2]) AND fvg_bear_created

FINAL_SIGNALS:
  buy: CRT_BULL AND SWING_LOW AND FVG_BULL AND PRICE_IN_FVG_BULL
  sell: CRT_BEAR AND SWING_HIGH AND FVG_BEAR AND PRICE_IN_FVG_BEAR
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
