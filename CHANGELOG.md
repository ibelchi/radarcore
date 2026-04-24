# Changelog - RadarCore

All notable changes to this project will be documented in this file.

## [1.2.0] - 2026-04-24

### Added
- **HTML Reporting**: New premium HTML report builder based on the Trazo design system. Includes macro context, top 5 opportunities, risk filters, and a "Plan for Tomorrow" section.
- **English Localization**: Complete translation of the entire software suite (UI, logs, diagnostics, and reports) from Catalan to English.
- **Database Backfill**: Added migration utility to automatically fill missing RSI and Volume metrics in historical SQLite records.
- **Macro Sentiment**: Market sentiment dashboard (SPY, QQQ, VIX, TNX, DXY) moved to the top of the "History & Reports" tab for better context when reviewing opportunities.
- **Diagnostic Logging**: Added real-time terminal logging for RSI and Volume calculations during scans.

### Changed
- **Default Configuration**: "Pre-filter universe" toggle now defaults to `ON` for faster, higher-quality scanning.
- **Report Language**: AI-generated research reports now default to English.
- **UI UX**: "Not Recommended" expander in the history tab is now expanded by default to improve risk awareness.
- **Codebase Refactor**: Standardized technical function names (e.g., `calculate_rsi`) and internal documentation to English.

### Fixed
- **Missing Metrics**: Resolved issue where RSI and Volume ratios were missing (N/A) in some scan results.
- **Data Access**: Fixed attribute access in the HTML report generator to correctly pull from database columns.
- **Macro Logic**: Synchronized English data keys across the ingestion, UI, and reporting modules.

---
*RadarCore: Advanced Swing Trading Intelligence*
