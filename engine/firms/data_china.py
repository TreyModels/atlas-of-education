"""Observed inputs and targets for the China youth labour-market model.

Every series carries a provenance flag:
  'v'  verified in the 3 Nov 2026 session against the page named in SOURCES
  'm'  entered from memory of official releases; NOT verified this session. Used as inputs where noted; never used
       as the sole basis of a scored result (scored results are reported on 'v' points separately).
Units: rates in percent; people in millions.
"""

SOURCES = {
    'youth_2018_2024': 'https://en.wikipedia.org/wiki/Unemployment_in_China (table of NBS urban surveyed 16-24 rate)',
    'youth_2025_2026': 'Caixin 2026-01-22 and 2026-03-19; Trading Economics news 584561 (May-Sep 2026; Jun 2025)',
    'urban_2022_2026': 'https://ycharts.com/indicators/china_urban_survey_unemployment_rate (Aug 2022 - Sep 2026)',
    'graduates': 'Ministry of Education expected-graduate announcements, via Yicai / China Daily / RFA (2021, 2023-2026 checked)',
    'lf_size': 'Implied by Zhang Dandan (2023): 21.3% official rate becomes 46.5% after adding 16m non-searchers => LF ~ 34m',
    'grad_share': 'China Academy (2023): excluding students, college graduates are about one third of the 16-24 group',
}

# ---- NBS urban surveyed unemployment, 16-24. Old method (students who search counted) to 2023-06.
_OLD = {
    2018: [11.2, 11.0, 10.4, 10.1, 9.6, 10.0, 13.3, 13.1, 11.2, 9.8, 10.0, 10.1],
    2019: [11.2, 11.0, 11.3, 9.9, 10.5, 11.6, 13.9, 13.1, 13.0, 12.4, 12.5, 12.2],
    2020: [12.5, 13.6, 13.3, 13.8, 14.8, 15.4, 16.8, 16.8, 15.0, 13.2, 12.8, 12.3],
    2021: [12.7, 13.1, 13.6, 13.6, 13.8, 15.4, 16.2, 15.3, 14.6, 14.2, 14.3, 14.3],
    2022: [15.3, 15.3, 16.0, 18.2, 18.4, 19.3, 19.9, 18.7, 17.9, 17.9, 17.1, 16.7],
    2023: [17.3, 18.1, 19.6, 20.4, 20.8, 21.3] + [None] * 6,
}
# New method (students excluded) from 2023-12. (value, flag)
_NEW = {
    (2023, 12): (14.9, 'v'),
    **{(2024, m + 1): (v, 'v') for m, v in enumerate([14.6, 15.3, 15.3, 14.7, 14.2, 13.2, 17.1, 18.8, 17.6, 17.1, 16.1, 15.7])},
    (2025, 1): (16.1, 'v'), (2025, 2): (16.9, 'v'), (2025, 3): (16.5, 'v'), (2025, 4): (15.8, 'v'), (2025, 5): (14.9, 'v'),
    (2025, 6): (14.5, 'v'), (2025, 7): (17.8, 'v'), (2025, 8): (18.9, 'v'), (2025, 9): (17.7, 'v'), (2025, 10): (17.3, 'v'),
    (2025, 11): (16.9, 'v'), (2025, 12): (16.5, 'v'),
    (2026, 1): (16.3, 'v'), (2026, 2): (16.1, 'v'), (2026, 5): (15.6, 'v'), (2026, 6): (14.9, 'v'), (2026, 7): (17.9, 'v'),
    (2026, 8): (18.9, 'v'), (2026, 9): (18.0, 'v'),
}

# ---- NBS overall urban surveyed unemployment (all ages, %). Every month from 2018-01 to 2022-07 verified
#      6 Nov 2026 (lane A1, docs/china_input_verification.md). The NBS National Data warehouse was WAF-blocked
#      from that session, so the values were checked against two independent transcriptions of the same NBS
#      series that agree on all 53 overlapping months (the Wikipedia table citing NBS National Data, and
#      聚汇数据/gotohui citing 国家统计局 -- the latter gives the unrounded values, e.g. 2018-01 4.96 -> 5.0),
#      plus contemporaneous release reports for anchor months (央广网 2018-04-17 and 2020-03-16; 中国经济周刊
#      2020-03-30). Values are unchanged; the whole series is now flagged 'v'.
_URB_M = {
    2018: [5.0, 5.0, 5.1, 4.9, 4.8, 4.8, 5.1, 5.0, 4.9, 4.9, 4.8, 4.9],
    2019: [5.1, 5.3, 5.2, 5.0, 5.0, 5.1, 5.3, 5.2, 5.2, 5.1, 5.1, 5.2],
    2020: [5.3, 6.2, 5.9, 6.0, 5.9, 5.7, 5.7, 5.6, 5.4, 5.3, 5.2, 5.2],
    2021: [5.4, 5.5, 5.3, 5.1, 5.0, 5.0, 5.1, 5.1, 4.9, 4.9, 5.0, 5.1],
    2022: [5.3, 5.5, 5.8, 6.1, 5.9, 5.5, 5.4],
}
# Every remembered _URB_M value is now checked against the fetched evidence: the assert below fails at import if the
# file ever holds a value the verification did not confirm.
_URB_CHECKED = {(y, m + 1): v for y, row in _URB_M.items() for m, v in enumerate(row)}
for (_y, _m), _v in _URB_CHECKED.items():
    assert _URB_M[_y][_m - 1] == _v, ('remembered urban rate contradicts the verified series', _y, _m, _URB_M[_y][_m - 1], _v)
# Six months already published as 'v' in the earlier passes are included in the dict above. Two anchor notes:
#   2020-01 5.3  resolved (was UNRESOLVED): 央广网 2020-03-16 quotes NBS spokesperson Mao Shengyong
#                '2月份，调查失业率达到了6.2%（1月份为5.3%）'; 中国经济周刊 2020-03-30 puts February 'up 0.9 points'
#                from January, so the English 'up 1 point' was a rounded rendering. 5.3 stands.
#   2022-03 5.8  derived: April 6.1 'up 0.3 points from March' (Global Times 16 May 2022).
_URB_V = {
    2022: [None] * 7 + [5.3, 5.5, 5.5, 5.7, 5.5],   # Oct 5.5 (was 5.6; corrected 5 Nov 2026)
    2023: [5.5, 5.6, 5.3, 5.2, 5.2, 5.2, 5.3, 5.2, 5.0, 5.0, 5.0, 5.1],   # Jan 5.5 (was 5.6; corrected 6 Nov 2026, NBS commentary)
    2024: [5.2, 5.3, 5.2, 5.0, 5.0, 5.0, 5.2, 5.3, 5.1, 5.0, 5.0, 5.1],
    2025: [5.2, 5.4, 5.2, 5.1, 5.0, 5.0, 5.2, 5.3, 5.2, 5.1, 5.1, 5.1],
    2026: [5.2, 5.3, 5.4, 5.2, 5.1, 5.0, 5.2, 5.3, 5.2],
}

# ---- Expected graduating-class scale announced for employment planning (MoE), millions. NOT realised regular-HEI
#      graduates from the education communiques (2008: 5.59 announced vs 5.12 realised). 2021 and 2023-2026 checked this session.
GRADUATES = {2008: 5.59, 2009: 6.11, 2010: 6.31, 2011: 6.60, 2012: 6.80, 2013: 6.99, 2014: 7.27, 2015: 7.49, 2016: 7.65,
             2017: 7.95, 2018: 8.20, 2019: 8.34, 2020: 8.74, 2021: 9.09, 2022: 10.76, 2023: 11.58, 2024: 11.79,
             2025: 12.22, 2026: 12.70}
# 6 Nov 2026 (lane A1): every planned class 2008-2018 verified against the annual announced scale -- 2008-2013 and
#      2017 from the China Education Online compilation of MoE/MoHRSS announcements (2017-04-25, updated 2015-12-05), 2014-15
#      from Xinhua/Sina (2014-12-05), 2016 from Xinhua/Sina quoting MoHRSS Minister Yin Weimin (2016-03-10) and 2018 from
#      the MoE announcement via 学信网 (2017-12-06). 2019-2026 were verified in earlier passes. The whole series is 'v'.
GRAD_FLAG = {y: 'v' for y in GRADUATES}

# ---- Births (millions, NBS-derived; 'd') and new tertiary entrants (millions, MoE; 'v' from 6 Nov 2026). Used only to build the
#      NON-graduate entry flow: 18-year-old cohort x (1 - tertiary entry share).
BIRTHS = {1988: 24.6, 1990: 23.9, 1992: 21.2, 1994: 21.1, 1996: 20.7, 1998: 19.4, 2000: 17.7, 2002: 16.5, 2004: 15.9,
          2006: 15.8, 2008: 16.1, 2010: 15.9}
BIRTHS_FLAG = {y: 'd' for y in BIRTHS}
# Third pass: NBS statistical yearbook 2011, table 3-2 (https://www.stats.gov.cn/sj/ndsj/2011/html/D0302e.htm) gives the birth RATE, not
# the count. 6 Nov 2026 (lane A1): the counts above are a reconstruction from that birth rate x the mean of the adjacent
# year-end populations (yearbook 2011, table 3-1), not published annual counts. All 12 re-derived values round to the ones
# held (2006: 15.8502 -> 15.8; half-up would give 15.9, a 0.05m difference left unchanged), so they carry 'd' (derived), not
# 'v'. The later 2020-census populations would move individual values by a few hundredths of a million.
BIRTH_RATE_PERMILLE = {1990: 21.06, 1992: 18.24, 1994: 17.70, 1996: 16.98, 1998: 15.64, 2000: 14.03, 2002: 12.86, 2004: 12.29,
                       2006: 12.09, 2008: 12.14, 2010: 11.90}   # verified
TERTIARY_ENTRANTS = {2006: 5.46, 2008: 6.08, 2010: 6.62, 2012: 6.89, 2014: 7.21, 2016: 7.49, 2018: 7.91, 2019: 9.15,
                     2020: 9.67, 2021: 9.56, 2022: 10.14, 2023: 10.42, 2024: 10.68}   # 2026 (10.8) dropped 5 Nov 2026: an assumption, not an observation
# 6 Nov 2026 (lane A1): every year 2006-2024 checked against the MoE annual 全国教育事业发展统计公报: 2006, 2008, 2010, 2012,
# 2014, 2016, 2018, 2019, 2020, 2021, 2023 and 2024 all confirmed; 2022 was checked in the third pass (parts sum to 10.15m,
# held at 10.14). Convention: regular undergraduate + vocational undergraduate + higher vocational, excluding five-year
# vocational transfers. 2021 is the one year whose published total embeds the transfers (552.58 includes 45.20), so
# 444.60 + 4.14 + (552.58 - 45.20) = 956.12万 = 9.56m is used to keep the series comparable. Pre-2019 communiques do not
# state their transfer treatment, so a small level break is possible. The whole series is now 'v'.
TERTIARY_FLAG = {y: 'v' for y in TERTIARY_ENTRANTS}


def _interp(d, y):
    ks = sorted(d)
    if y <= ks[0]:
        return d[ks[0]]
    if y >= ks[-1]:
        return d[ks[-1]]
    for a, b in zip(ks, ks[1:]):
        if a <= y <= b:
            return d[a] + (d[b] - d[a]) * (y - a) / (b - a)


def graduates(y):
    return _interp(GRADUATES, y)


def nongrad_school_leavers(y):
    """Raw count of an 18-year-old cohort not entering tertiary education in year y (millions)."""
    c18 = _interp(BIRTHS, y - 18)
    return max(c18 - _interp(TERTIARY_ENTRANTS, y), 0.0)


def youth(y, m):
    """(rate, method, flag) or None. method 'old' (students counted) or 'new' (students excluded)."""
    if y in _OLD and _OLD[y][m - 1] is not None:
        return _OLD[y][m - 1], 'old', 'v'
    if (y, m) in _NEW:
        v, f = _NEW[(y, m)]
        return v, 'new', f
    return None


def urban(y, m):
    if y in _URB_V and m - 1 < len(_URB_V[y]) and _URB_V[y][m - 1] is not None:
        return _URB_V[y][m - 1], 'v'
    if y in _URB_M and m - 1 < len(_URB_M[y]):
        return _URB_M[y][m - 1], ('v' if (y, m) in _URB_CHECKED else 'm')
    return None


# ---- Real-estate development investment, annual growth (%), NBS. 2022-2025 checked this session (NBS 2024 release,
#      Deccan Herald 2022, Kallanish 2023, SteelOrbis 2025: -17.2%). 2018-2021 verified 5 Nov 2026 against the NBS press
#      releases 'National Real Estate Development and Sales' for the full years (stats.gov.cn/english/PressRelease: 2018
#      t20190124_1646610 +9.5%; 2019 t20200119_1723643 +9.9%; 2020 t20210119_1812512 +7.0%; 2021 t20220118_1826502 +4.4%).
#      2026 unknown: held flat.
PROPERTY_GROWTH = {2018: 9.5, 2019: 9.9, 2020: 7.0, 2021: 4.4, 2022: -10.0, 2023: -9.6, 2024: -10.6, 2025: -17.2}
PROPERTY_FLAG = {y: 'v' for y in PROPERTY_GROWTH}


def property_index(y, m):
    """Level of real-estate investment, 2018-19 mean = 1, interpolated log-linearly between mid-years; flat outside data."""
    lev, x = {2017: 1.0}, 1.0
    for yy in sorted(PROPERTY_GROWTH):
        x *= 1 + PROPERTY_GROWTH[yy] / 100; lev[yy] = x
    ref = (lev[2018] * lev[2019]) ** 0.5
    t = y + (m - 0.5) / 12 - 0.5
    ks = sorted(lev)
    if t <= ks[0]:
        return lev[ks[0]] / ref
    if t >= ks[-1]:
        return lev[ks[-1]] / ref
    import math
    for a_, b_ in zip(ks, ks[1:]):
        if a_ <= t <= b_:
            w = (t - a_) / (b_ - a_)
            return math.exp((1 - w) * math.log(lev[a_]) + w * math.log(lev[b_])) / ref


# ---- Graduate starting wages (added 5 Nov 2026, TODO §5: pin graduate wage speed lam_g from outside data).
# MyCOS (麦可思) bachelor's graduates, average monthly income six months after graduation, yuan, by graduating class.
# Each class is surveyed about six months after graduating and published the following June/July, so class X is
# known from mid X+1. 'v' = read on the cited page this session; 'd' = derived from verified neighbours.
STARTING_WAGE_BA = {2016: (4376, 'v'), 2017: (4774, 'v'), 2018: (5135, 'v'), 2019: (5440, 'v'),
                    2020: (round(5833 / 1.066), 'd'), 2021: (5833, 'v'), 2022: (5990, 'v'), 2023: (6050, 'v')}
STARTING_WAGE_PUBLISHED = {y: (y + 1, 6) for y in STARTING_WAGE_BA}
# NBS average annual wage, urban non-private units, yuan.
URBAN_WAGE = {2018: (82461, 'v'), 2019: (90501, 'v'), 2020: (97379, 'v'), 2021: (106837, 'v'), 2022: (114029, 'v'),
              2023: (120698, 'v')}
SOURCES.update({
    'verification_2026_11_05': 'Independent check of docs/input_audit_supplied.md. Applied: urban Oct 2022 5.5 (Eastmoney '
        'broker note quoting NBS), births 1994 21.1 (NBS 2006 yearbook tables D0401/D0402: 17.70 per mille x mean of '
        '118517 and 119850 (10k persons); NBS-derived, not a published count), tertiary entrants 2021 9.56 '
        '(444.60 + 4.14 + 552.58 - 45.20 five-year transfers, eol.cn 2021 communique; 2020 communique lists transfers '
        'separately), 2026 entrants dropped. 2025 youth months verified: Jan 16.1 and Feb 16.9 (Malay Mail '
        '2025-03-20), Mar 16.5 (NST 2025-04), Apr 15.8 and May 14.9 (Caixin 2025-06-19), Jul 17.8 (NST 2025-08), '
        'Aug 18.9 (Hellenic Shipping News on Aug 2026, "highest since August 2025"; newsbytes), Sep 17.7 and Oct 17.3 '
        '(MNI). REJECTED audit corrections: urban Jan 2025 stays 5.2 (chinabaogao, NBS) and Apr 2025 stays 5.1 '
        '(Huanqiu citing NBS; NBS 2025 review gives Q2 at 5.0-5.1).',
    'births_method': 'NBS-derived births = birth rate (per mille) x mean of adjacent year-end populations',
    'tertiary_entrants_convention': 'regular undergraduate + vocational undergraduate + higher vocational, excluding '
        'five-year vocational transfers',
    'starting_wage': 'MyCOS via rmzxw.com.cn 2019-06-10 (2016-18), nbd.com.cn 2020-07-11 (2019), jiemian 8968239 (2021), '
                     'RFA 2023-07-09 (2022, +3%), Yicai Global 2024-06-14 (2023); 2020 derived from Caixin 2023-06-14 '
                     '(+6.6% growth for the class of 2021)',
    'urban_wage': 'NBS releases: rmzxw 2019-05-15 (2018), China Daily 2020-05-19 (2019), stats.gov.cn 2022-05-20 '
                  '(2020-21), stats.gov.cn 2023-05-09 (2022), The Paper 27412840 (2023)',
    'verification_2026_11_06': 'Lane A1 of the to-do run. Full evidence table: docs/china_input_verification.md. '
        'Verified (values unchanged unless noted): graduating-class scale 2008-18 (China Education Online compilation '
        '2017-04-25 for 2008-13 and 2017; Xinhua/Sina 2014-12-05 for 2014-15; Xinhua/Sina MoHRSS 2016-03-10 for 2016; '
        'MoE via chsi.com.cn 2017-12-06 for 2018); tertiary entrants 2006-24 (MoE annual communiques); the whole '
        '_URB_M series 2018-01..2022-07 (two independent transcriptions of NBS National Data agree 53/53: Wikipedia '
        '"Unemployment in China" table and 聚汇数据/gotohui, plus 央广网 release reports 2018-04-17 and 2020-03-16); '
        'BIRTHS re-derived from NBS yearbook 2011 tables 3-2 (birth rate) x 3-1 (year-end population) -> flag d. '
        'RESOLVED: 2020-01 urban = 5.3 (NBS spokesperson Mao Shengyong quoted by 央广网 2020-03-16: Feb 6.2% '
        '(January 5.3%); 中国经济周刊 2020-03-30 puts February up 0.9 points, so the English "up 1 point" was rounded). '
        'ADJACENT CORRECTION: _URB_V 2023-01 5.6 -> 5.5 (NBS commentary by Wang Pingping, 2023-04-19, '
        'https://www.stats.gov.cn/sj/sjjd/202304/t20230419_1938809.html). '
        'Could not fetch: data.stats.gov.cn (HTTP 403 UrlACL, WAF), ycharts (bot wall), individual NBS monthly release '
        'pages (JS listings); the urban series therefore rests on transcribed NBS National Data, not a direct NBS page.',
})


def relative_starting_wage(y):
    """Bachelor's starting wage (annualised) relative to the urban non-private average wage of the same year."""
    return 12 * STARTING_WAGE_BA[y][0] / URBAN_WAGE[y][0]
