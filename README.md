# SCALPING INDICATOR V3 — Hugo FX Methodology

**Pine Script v6 | TradingView M1 Scalping | Multi-Timeframe Cascade Filter**

---

## Overview

Automated trading indicator for M1 scalping using tri-level timeframe filtering:
- **H1**: CRT (Candle Range Theory) detection → Trigger
- **M15**: Swing pattern validation → Safety filter  
- **M1**: FVG (Fair Value Gap) + Price retracement → Entry signal

**Status**: ✅ Production Ready | Tested & Validated

---

## Quick Start

1. Open TradingView Desktop with debugging enabled:
   ```bash
   "C:\Program Files\WindowsApps\TradingView.Desktop_3.1.0.7818_x64__n534cwy3pjxzj\TradingView.exe" --remote-debugging-port=9222
   ```

2. Copy `SCALPING_INDICATOR_V3.pine` content into Pine Script Editor

3. Click "Save and Compile" (must show: ✅ Compiled clean — 0 errors)

4. Apply to M1, M15, H1 charts and monitor for BUY/SELL signals

👉 **Full setup guide:** See [START.md](START.md)

---

## Files

| File | Purpose |
|------|---------|
| `SCALPING_INDICATOR_V3.pine` | Main indicator (Pine Script v6) |
| `START.md` | Setup + execution instructions |
| `FILTRAGE_H1_M1_CONDITIONS.md` | Logic reference (machine-readable) |
| `README.md` | This file |

---

## Signal Logic

```
BUY Signal:
  H1 Bullish CRT 
  ∩ M15 Swing Low (same hour)
  ∩ M1 FVG Bull created
  ∩ Price retrace into FVG
  → DIAMOND LABEL "BUY" + ALERT

SELL Signal:
  H1 Bearish CRT
  ∩ M15 Swing High (same hour)
  ∩ M1 FVG Bear created
  ∩ Price retrace into FVG
  → DIAMOND LABEL "SELL" + ALERT
```

---

## Key Principle: Cascade Correlation

**M15 Swings must appear within the same H1 hour as CRT detection.**
- CRT H1 detected @ H:00 → Swing M15 waits H:15, H:30, H:45
- No orphaned swings after hour change
- `request.security()` automatically validates same-hour correlation

---

## Display

| Timeframe | Element | Color | Position |
|-----------|---------|-------|----------|
| **H1** | CRT Label | Green (BULL) / Red (BEAR) | 2nd candle |
| **M15** | SWING Label | Green (LOW) / Red (HIGH) | 2nd candle |
| **M1** | FVG Box | Green (BULL) / Red (BEAR) | Gap zone |
| **M1** | Signal | 💎 BUY / SELL | Diamond |

---

## Configuration

- **Version**: Pine Script v6
- **Overlay**: true (display on candlesticks)
- **Max boxes**: 200 (FVG storage)
- **Alerts**: ON (once per bar close)

---

## Requirements

- TradingView Desktop v3.1.0.7818+
- Windows/Mac/Linux
- 4GB RAM minimum

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No CRT labels | Wait for pattern completion (BEAR + BULL inside range) |
| Orphaned swings | Restart indicator or reload script |
| No signals despite FVG | Price must **retrace INTO** FVG zone |
| Alerts not firing | Check system alert settings in TradingView |

👉 **Full troubleshooting:** See [START.md](START.md#troubleshooting)

---

## References

- Strategy document: `Strategie_Scalping_M1_Analyse_HugoFX.pdf`
- Logic reference: `FILTRAGE_H1_M1_CONDITIONS.md`
- Complete guide: `START.md`

---

## License

Private — Educational & Testing Only

---

**Last Updated**: 2026-05-25  
**Author**: Laurent (Hugo FX Methodology Implementation)  
**Support**: Check START.md + FILTRAGE_H1_M1_CONDITIONS.md for machine-readable logic
