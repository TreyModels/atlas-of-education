"""Numbers that come from outside the model. Each one is sourced in FACT_CHECK.md.
Nothing here is tuned."""

# IFS chart "Big marriage aspiration gap in China" (as given to us; the chart page itself
# was not found online, see FACT_CHECK.md). Percent of unmarried 18-34 who want to marry.
CHART = {  # country: (women %, men %, significant at 95%?)
    "Egypt": (83, 95, False), "Israel": (85, 92, False), "United Kingdom": (83, 86, None),
    "Ireland": (88, 78, False), "United States": (83, 77, True), "Korea": (66, 78, False),
    "China": (48, 77, True), "Japan": (51, 53, None),
}
# (None = significance not stated in the chart text we were given)

# Sex ratio at birth, male births per 100 female births, UN World Population Prospects 2024
# as published by Our World in Data (read in source; see FACT_CHECK.md).
SRB = {
    "China": {1992: 112.31056, 1993: 113.01446, 1994: 113.71303, 1995: 114.35266, 1996: 114.91414,
              1997: 115.41609, 1998: 115.86005, 1999: 116.241745, 2000: 116.56384, 2001: 116.82568,
              2002: 117.06723, 2003: 117.24912, 2004: 117.38237, 2005: 117.4584, 2006: 117.48244,
              2007: 117.45185, 2008: 117.35351},
    "Korea": {1992: 114.10815, 1993: 115.78167, 1994: 117.07072, 1995: 116.85002, 1996: 114.18403,
              1997: 111.29565, 1998: 111.18679, 1999: 112.21027, 2000: 113.214516, 2001: 112.030365,
              2002: 110.433426, 2003: 110.65917, 2004: 110.44957, 2005: 110.27314, 2006: 109.00117,
              2007: 108.04552, 2008: 108.32657},
    "Japan": {1992: 105.75229, 1993: 105.69354, 1994: 105.49562, 1995: 105.3299, 1996: 105.346535,
              1997: 105.3439, 1998: 105.29259, 1999: 105.44161, 2000: 105.61223, 2001: 105.596275,
              2002: 105.53462, 2003: 105.515175, 2004: 105.341225, 2005: 105.257484, 2006: 105.28795,
              2007: 105.40894, 2008: 105.39842},
}

# Share of people aged 30-34 who had never married, China, 2022: 18.4% (China Population and
# Employment Statistical Yearbook 2023, as reported by Yicai Global; both sexes; read in a
# news report, not the yearbook). So ever-married about 81.6%.
NEVER_MARRIED_30_34 = 0.184
EVER_MARRIED_TARGET = 1 - NEVER_MARRIED_30_34
# Window treated as "realistic" for pooled ever-married at 30-34 (our choice, +/- about 6 points,
# because we have one noisy figure from a news report):
EVER_MARRIED_WINDOW = (0.75, 0.88)

# Other estimates of marriage intention, reported for context in FACT_CHECK.md only (not used in model)
