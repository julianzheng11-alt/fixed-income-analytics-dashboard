## Development Notes

This project was built iteratively as a first fixed-income Python application. I have been teaching myself Python for 1-2 months through coursework, market-focused projects and practical experimentation. The goal is to keep expanding the dashboard while developing a stronger understanding of fixed-income analytics and software design.

So far, challenges of this project included:
- translating bond-pricing and duration formulas into reusable functions
- validating the quote units returned by Yahoo Finance
- handling percentage-point data correctly in Python formatting
- separating market-data retrieval, bond analytics and the Streamlit interface
- removing debug output when modules were imported into the dashboard

## Planned Improvements
- Add 2s10s and 5s30s curve spreads
- Add convexity
- Add parallel yield-shift scenario analysis
- Improve dashboard layout
- Add unit tests for pricing functions
- Add German government bond data
