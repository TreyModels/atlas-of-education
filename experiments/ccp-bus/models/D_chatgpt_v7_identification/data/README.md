# Temporal data separation

Training: filed cases 2013–2019, seven annual observations; land receipts 2013–2019, from the cited MOF execution releases. Forecast information origin: 24 May 2020, after the 2019 land release. Earlier vintages are retained rather than silently substituted with later final accounts. The 2015 budget reclassification and publication lags constrain comparability. Finance and defense inputs are excluded from the primary fit because no comparable verified pre-cutoff panel was acquired.

Holdout: 2020–2025 cases and land receipts. fit.py reads only training files. evaluate.py reads the holdout after candidate selection is frozen. Case counts are disciplinary filings, not a count of known corrupt persons. A fitted scale maps civilian simulated filings into this observation series, with uncertain coverage. This is an exploratory measurement approximation rather than an established population crosswalk.
