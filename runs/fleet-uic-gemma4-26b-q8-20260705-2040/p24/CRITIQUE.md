# Critique of limiter.py

- **burst-exceeds-capacity**: The implementation always returns `True`, effectively allowing an infinite burst and completely ignoring any capacity constraints.
- **wrong refill math**: There is no refill logic implemented; the limiter performs zero accounting for token replenishment.
- **clock misuse**: The provided `clock` object is entirely ignored, failing to account for elapsed time to drive refills.
