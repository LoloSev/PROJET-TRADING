# START - SCALPING INDICATOR V3.1
**Machine-First | IA Compatible | Signal Validation First**

---

## 📌 QUICK NOTE

**This doc is for V3.1** (complete cascade with BUY/SELL signals).

If you want **individual component testing**, see **CLAUDE.md** for:
- **LOLO_SWING_M15.pine** → M15 swing detection
- **LOLO_FVG_M1.pine** → M1 FVG detection  
- **LOLO_CRT_H1.pine** → H1 CRT detection
- **LOLO_STRAT_HUGO_V1.pine** → Combined (H1 CRT + M15 SWING + M1 FVG on M1)

---

## OBJECTIF PRIORITAIRE V3.1

```yaml
primary_goal:
  - Obtenir un signal BUY/SELL quand les conditions structurelles COMPLÈTES sont réunies.
  - Valider la cascade H1 -> M15 -> M1 AVEC retracement.
  - Valider l'affichage visuel et les alertes TradingView.

validation_signal_REQUIRED:
  BUY: H1 CRT BULL + M15 SWING LOW + M1 FVG BULL + PRICE RETRACES INTO FVG
  SELL: H1 CRT BEAR + M15 SWING HIGH + M1 FVG BEAR + PRICE RETRACES INTO FVG

critical_rule:
  NO_RETRACEMENT: "Pas de retracement = Pas de trade, peu importe les autres conditions"
  reason: "Price must validate FVG as structural level"
  reference: "See FVG_AND_RETRACEMENT.md"

explicitly_excluded_for_now:
  - Entrée sur OB / Breaker / PD Array.
  - Premium / Discount.
  - SL / TP.
  - Breakeven.
  - Add-in / pyramidage.
```

> Cette version ne valide pas encore une prise de trade complète. Elle sert d'abord à vérifier que le moteur produit un signal lorsque les conditions de base sont alignées.

---

## PRÉREQUIS

```yaml
software:
  - TradingView Desktop v3.1.0.7818+ WITH --remote-debugging-port=9222
  - Chrome/Chromium (optional, for manual editing)

files_required:
  - SCALPING_INDICATOR_V3_1_SIGNAL_VALIDATION.pine
  - FILTRAGE_H1_M1_CONDITIONS.md (reference)

platform:
  - Windows 10+ OR Mac OR Linux
  - minimum: 4GB RAM, 500MB disk
```

---

## SETUP

```text
1. Launch TradingView Desktop with debug port:
   "C:\\Program Files\\WindowsApps\\TradingView.Desktop_3.1.0.7818_x64__n534cwy3pjxzj\\TradingView.exe" --remote-debugging-port=9222

2. Open chart on desired instrument.
   Required timeframe for signal validation: M1.

3. Open Pine Script Editor.

4. Copy SCALPING_INDICATOR_V3_1_SIGNAL_VALIDATION.pine content.
   Paste into editor.
   Save and compile.
   Expected result: 0 errors.

5. Apply indicator to M1 chart.
   Optional: also view H1 and M15 charts to verify debug labels.
```

---

## CONFIGURATION

```yaml
indicator_settings:
  pine_version: 6
  overlay: true
  max_boxes_count: 200
  max_labels_count: 500

inputs:
  show_debug: true
  show_fvg: true
  one_signal_per_bar: true

timeframes_to_monitor:
  H1: CRT context
  M15: swing structure filter
  M1: FVG detection + BUY/SELL signal

display_elements:
  H1: H1 CRT BULL / H1 CRT BEAR labels
  M15: H1+M15 BULL / H1+M15 BEAR labels
  M1: FVG boxes + BUY/SELL diamonds + H1/M15 debug labels

alerts:
  BUY SIGNAL: once_per_bar_close
  SELL SIGNAL: once_per_bar_close
```

---

## EXECUTION LOGIC V3.1

```text
loop on M1 candle close:

  // H1 CONTEXT (CRT with liquidity raid validation)
  h1_bullish_crt = previous H1 candle bearish
                   AND current H1 candle bullish
                   AND current H1 LOW breaks BELOW previous low (liquidity raid)
                   AND current H1 close inside previous H1 range

  h1_bearish_crt = previous H1 candle bullish
                   AND current H1 candle bearish
                   AND current H1 HIGH breaks ABOVE previous high (liquidity raid)
                   AND current H1 close inside previous H1 range

  // M15 STRUCTURE
  m15_swing_low = M15 three-candle swing low pattern
                  AND last candle bullish

  m15_swing_high = M15 three-candle swing high pattern
                   AND last candle bearish

  // M1 FVG + RETRACEMENT
  fvg_bull = high[2] < low
  fvg_bear = low[2] > high
  
  retracement_bull = fvg_bull AND (close > high[2] AND close < low)
  retracement_bear = fvg_bear AND (close > high AND close < low[2])

  // VALIDATION SIGNALS ONLY (ALL 4 CONDITIONS REQUIRED)
  buy_signal = h1_bullish_crt AND m15_swing_low AND retracement_bull
  sell_signal = h1_bearish_crt AND m15_swing_high AND retracement_bear

  // OUTPUT
  IF buy_signal:
    display BUY diamond
    trigger BUY alert

  IF sell_signal:
    display SELL diamond
    trigger SELL alert

end loop
```

---

## IMPORTANT - IMPLÉMENTATION EN V3.1

```yaml
implemented:
  fvg_retracement:
    status: REQUIRED
    reason: Price must validate FVG as structural level
    reference: FVG_AND_RETRACEMENT.md
    rule: "No retracement = No trade"

not_in_scope:
  order_block_entry:
    status: excluded
    reason: trade-entry logic later

  premium_discount_filter:
    status: excluded
    reason: trade-entry logic later

  risk_management:
    status: excluded
    reason: indicator currently validates signals only
```

---

## EXPECTED OUTPUT

```text
H1 chart:
  ✓ H1 CRT BULL / H1 CRT BEAR labels when CRT condition appears

M15 chart:
  ✓ H1+M15 BULL when H1 bullish CRT + M15 swing low align
  ✓ H1+M15 BEAR when H1 bearish CRT + M15 swing high align

M1 chart:
  ✓ Green/red FVG boxes
  ✓ BUY diamond when H1 CRT BULL + M15 SWING LOW + M1 FVG BULL
  ✓ SELL diamond when H1 CRT BEAR + M15 SWING HIGH + M1 FVG BEAR
  ✓ Alert on BUY/SELL signal
```

---

## VALIDATION CHECKLIST

```text
□ Pine Script compiles with 0 errors.
□ Indicator is applied on M1.
□ FVG boxes appear on M1.
□ H1 debug labels appear when CRT conditions exist.
□ M15 debug labels appear when H1 + M15 conditions align.
□ BUY/SELL diamonds appear when structural conditions align.
□ Alerts trigger on BUY/SELL signal.
□ No expectation yet of FVG retracement, OB entry, SL/TP or BE.
```

---

## TROUBLESHOOTING

```text
problem: No BUY/SELL signal
  check: Are the three validation blocks aligned?
    - H1 CRT in the expected direction
    - M15 swing in the same direction
    - M1 FVG in the same direction
  note: V3.1 does NOT wait for retracement into FVG.

problem: FVG boxes appear but no BUY/SELL signal
  cause: H1 and/or M15 filter not aligned.
  debug: Enable show_debug.

problem: H1/M15 labels appear but no final signal
  cause: No M1 FVG at the same validation moment.
  debug: Check M1 chart with show_fvg enabled.

problem: Too many debug labels
  solution: Disable show_debug in indicator settings.

problem: Alerts not firing
  check: TradingView alert configured on indicator.
  check: alertcondition BUY SIGNAL / SELL SIGNAL available.
```

---

## OPERATION MODE

```yaml
mode: signal_validation
real_time_monitoring: M1
cascade: H1 CRT -> M15 SWING -> M1 FVG -> BUY/SELL signal
trade_execution: manual / not covered
risk_management: not included
next_phase: retracement FVG / OB / PD Array entry logic
```

---

**Last Update:** 2026-05-25  
**Status:** V3.1 Signal Validation  
**Reference:** SCALPING_INDICATOR_V3_1_SIGNAL_VALIDATION.pine | FILTRAGE_H1_M1_CONDITIONS.md
