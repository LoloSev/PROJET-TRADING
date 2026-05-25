# START - SCALPING INDICATOR V3
**Machine-First | IA Compatible | Executable Instructions**

---

## PRÉREQUIS

```yaml
software:
  - TradingView Desktop v3.1.0.7818+ WITH --remote-debugging-port=9222
  - Chrome/Chromium (optional, for manual editing)

files_required:
  - SCALPING_INDICATOR_V3.pine
  - FILTRAGE_H1_M1_CONDITIONS.md (reference)

platform:
  - Windows 10+ OR Mac OR Linux
  - minimum: 4GB RAM, 500MB disk
```

---

## SETUP (One-Time)

```
1. Launch TradingView Desktop with debug port:
   Command: "C:\Program Files\WindowsApps\TradingView.Desktop_3.1.0.7818_x64__n534cwy3pjxzj\TradingView.exe" --remote-debugging-port=9222

2. Open chart on desired pair (e.g., EURUSD)
   Set timeframe to: M1 (required for indicator display)

3. Open Pine Script Editor (Ctrl+Shift+E or menu)

4. Copy SCALPING_INDICATOR_V3.pine content
   Paste into editor
   Click "Save and Compile"
   Verify: ✅ Compiled clean — 0 errors

5. Apply indicator to M1 chart
   Verify display on: H1 (left panel), M15 (right panel), M1 (main)
```

---

## CONFIGURATION

```yaml
indicator_settings:
  version: 6 (Pine Script v6 required)
  overlay: true (display ON candlesticks, not separate pane)
  max_boxes_count: 200 (FVG storage)
  
timeframes_to_monitor:
  - H1 (60min): CRT detection + display
  - M15 (15min): SWING detection + cascade filter
  - M1 (1min): FVG + SIGNAL display + alerts

display_elements:
  H1: CRT labels (green BULL / red BEAR on 2nd candle)
  M15: SWING labels (green LOW / red HIGH on 2nd candle) [CASCADED]
  M1: FVG boxes (green/red) + BUY/SELL diamonds + H1/M15 status

alerts:
  - BUY SIGNAL: ON (frequency: once_per_bar_close)
  - SELL SIGNAL: ON (frequency: once_per_bar_close)
```

---

## EXECUTION LOGIC

```
loop (every candle close on M1):
  
  // NIVEAU 1: H1 DATA
  fetch h1_close, h1_open, h1_prev_close, h1_prev_open, h1_prev_high, h1_prev_low via request.security("60")
  
  // NIVEAU 2: M15 DATA
  fetch m15_low[2], m15_low[1], m15_low[0], m15_high[2], m15_high[1], m15_high[0] via request.security("15")
  
  // NIVEAU 3: M1 DATA (NATIVE)
  use close, open, high, low, high[2], low[2]
  
  // CALCULATE CONDITIONS
  h1_crt_bull = (h1_prev_close < h1_prev_open) AND (h1_close > h1_open) AND (h1_close BETWEEN [h1_prev_low, h1_prev_high])
  h1_crt_bear = (h1_prev_close > h1_prev_open) AND (h1_close < h1_open) AND (h1_close BETWEEN [h1_prev_low, h1_prev_high])
  
  m15_swing_low = (m15_close[2] < m15_open[2]) AND (m15_low[2] > m15_low[1] < m15_low[0]) AND (m15_close[0] > m15_open[0])
  m15_swing_high = (m15_close[2] > m15_open[2]) AND (m15_high[2] < m15_high[1] > m15_high[0]) AND (m15_low[2] < m15_low[1] > m15_low[0]) AND (m15_close[0] < m15_open[0])
  
  fvg_bull = high[2] < low
  fvg_bear = low[2] > high
  
  price_in_fvg_bull = (close > high[2] AND close < low) AND fvg_bull
  price_in_fvg_bear = (close > high AND close < low[2]) AND fvg_bear
  
  // CASCADE FILTER (CRITICAL)
  h1_crt_bull_current = request.security(syminfo.tickerid, "60", h1_crt_bull)  // same hour H1?
  h1_crt_bear_current = request.security(syminfo.tickerid, "60", h1_crt_bear)  // same hour H1?
  
  // FINAL SIGNALS
  buy_signal = h1_crt_bull_current AND m15_swing_low AND fvg_bull AND price_in_fvg_bull
  sell_signal = h1_crt_bear_current AND m15_swing_high AND fvg_bear AND price_in_fvg_bear
  
  // OUTPUT
  IF timeframe == "60" (H1):
    IF h1_crt_bull OR h1_crt_bear:
      display_label("CRT\n[BULL|BEAR]", color=[green|red], position=2nd_candle)
  
  IF timeframe == "15" (M15):
    IF h1_crt_bull_current AND m15_swing_low:
      display_label("SWING\nLOW", color=green, position=2nd_candle)
    IF h1_crt_bear_current AND m15_swing_high:
      display_label("SWING\nHIGH", color=red, position=2nd_candle)
  
  IF timeframe == "1" (M1):
    IF fvg_bull: display_box(green, [high[2], low])
    IF fvg_bear: display_box(red, [high, low[2]])
    IF buy_signal: display_label("BUY", color=green, alert=true)
    IF sell_signal: display_label("SELL", color=red, alert=true)

end loop
```

---

## EXPECTED OUTPUT (Live Charts)

```
H1 Panel:
  ✓ CRT labels appear on 2nd candle of pattern
  ✓ Green BULL below, Red BEAR above
  ✓ ~1-2 per hour (varies by volatility)

M15 Panel:
  ✓ SWING LOW labels ONLY if CRT BULL in same hour
  ✓ SWING HIGH labels ONLY if CRT BEAR in same hour
  ✓ NO orphaned swings without CRT
  ✓ Displayed on 2nd candle of swing pattern

M1 Panel:
  ✓ Green/Red FVG boxes (gaps)
  ✓ Green diamond "BUY" when all 4 conditions met
  ✓ Red diamond "SELL" when all 4 conditions met
  ✓ Alert sound/notification on signal
  ✓ Tiny "H1" + "M15" status labels on M1
```

---

## VALIDATION CHECKLIST

```
□ TradingView running with --remote-debugging-port=9222
□ Pine Script v6 indicator compiled (0 errors)
□ Indicator applied to M1, M15, and H1 charts (or same chart with sub-windows)
□ CRT labels visible on H1 chart
□ SWING labels visible on M15 chart (ONLY with CRT)
□ FVG boxes visible on M1 chart
□ BUY/SELL diamonds appear on M1 (not constantly, only valid signals)
□ Alerts trigger on valid signals
□ No orphaned swings (all swings have CRT above them within same hour)
```

---

## TROUBLESHOOTING

```
problem: No CRT labels on H1
  solution: Wait for pattern completion (Candle 1 BEAR + Candle 2 BULL inside range)
  debug: Check h1_bullish_crt and h1_bearish_crt calculations

problem: SWING labels without CRT on M15
  solution: request.security() may not capture same-hour CRT
  debug: Verify h1_crt_bull_detected/h1_crt_bear_detected via request.security()
  fix: Restart indicator or reload Pine Script

problem: No signals despite visible FVG and swing
  solution: Price must RETRACE INTO FVG (not just touch it)
  debug: Check price_in_fvg_bull and price_in_fvg_bear conditions
  fix: Wait for price to enter FVG zone

problem: Alerts not firing
  solution: alert() frequency set to once_per_bar_close
  debug: Verify buy_signal and sell_signal trigger
  fix: Check TradingView alert settings in system
```

---

## OPERATION MODE

```
real_time_monitoring: M1 (1-minute candles)
entry_signals: BUY/SELL diamonds on M1
timeframe_cascade: H1 (filter) → M15 (validation) → M1 (execution)
risk_management: [User responsibility - SL/TP not included in indicator]
```

---

**Last Update:** 2026-05-25  
**Status:** ✅ Production Ready  
**Reference:** SCALPING_INDICATOR_V3.pine | FILTRAGE_H1_M1_CONDITIONS.md
