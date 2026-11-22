// p1_priors.js — prior distributions for the Angkor model, each with a derivation.
//
// The point of this file is that no parameter here is a free knob. Each is either
// (a) derived from an identity that a reader can check, or (b) anchored on a stated
// comparative range. Where a value is a guess it says so and says what would replace it.
//
// Usage: require('./p1_priors.js').sample(rng) -> {params..., meta}
'use strict';

// lognormal from a median and a log-sigma
function lognorm(median, sigma, r) {
  // Box-Muller on the normal, then exponentiate
  var u = 1 - r(), v = 1 - r();
  var z = Math.sqrt(-2 * Math.log(Math.max(1e-9, u))) * Math.cos(2 * Math.PI * v);
  return median * Math.exp(sigma * z);
}
function truncNorm(mu, sd, lo, hi, r) {
  for (var i = 0; i < 40; i++) {
    var u = 1 - r(), v = 1 - r();
    var z = Math.sqrt(-2 * Math.log(Math.max(1e-9, u))) * Math.cos(2 * Math.PI * v);
    var x = mu + sd * z;
    if (x >= lo && x <= hi) return x;
  }
  return mu;
}

var PRIORS = {
  // ---- agronomy ----
  y: {
    dist: 'lognormal(median 1.30, sigma 0.20)', ci90: [0.95, 1.78],
    why: 'Flood-recession/deepwater regime implies the LOW end of the pre-Green-Revolution ' +
      'band (litreview.md section 7.4: 0.8-1.8 t/ha for floating rice). Median 1.30 is the ' +
      'midpoint of that sub-band, not of the whole 1.2-2.2 regional band.',
    replaceWith: 'a phytolith or grain-assemblage study identifying the water regime at Angkor'
  },
  riceKg: {
    dist: 'normal(200, 25) truncated [150,250]', ci90: [159, 241],
    why: '200 kg paddy/person/yr is the standard rice-dominant figure; Castillo et al. 2020 ' +
      '("The Khmer did not live by rice alone") is direct evidence that fish, legumes and ' +
      'other crops substituted, which is why the lower tail is real rather than noise.',
    replaceWith: 'faunal and archaeobotanical calorie reconstruction for a residential assemblage'
  },
  Amax: {
    dist: 'lognormal(median 1100 km2, sigma 0.28)', ci90: [690, 1620],
    why: 'DERIVED, not chosen: 750,000 people x 200 kg = 150,000 t; at 1.30 t/ha that is ' +
      '115,400 ha = 1,154 km2 under paddy in a single year, with no fallow, no seed reserve ' +
      'and no other land use. Median sits just under that identity so the identity is a ' +
      'constraint the draws can violate rather than an assumption baked in.',
    replaceWith: 'a mapped planted-area estimate (not occupation density x extent)'
  },
  // ---- the fiscal mechanism ----
  endowRate: {
    dist: 'lognormal(median 0.0011 /yr, sigma 0.45)', ci90: [0.00045, 0.0026],
    why: 'DERIVED from a cumulative claim: if temples held 30-50% of cultivated land by ' +
      'c. 1300, then over 400 years -ln(1-0.4)/400 = 0.00128 and -ln(1-0.3)/400 = 0.00089. ' +
      'Median is the geometric midpoint. This is the model\'s most influential parameter ' +
      '(Morris 7.0) and the derivation is the only defensible handle on it.',
    replaceWith: 'a systematic sum of dated land grants as a share of a settled cultivated-area figure'
  },
  eliteGrow: {
    dist: 'lognormal(median 0.0020 /yr, sigma 0.50)', ci90: [0.0008, 0.0045],
    why: 'Elite households at 1-3% of population, doubling over roughly 350 years: ' +
      'ln(2)/350 = 0.00198. Same order as Turchin\'s elite overproduction rates.',
    replaceWith: 'a count of titled officials or endowment beneficiaries per reign'
  },
  taxRate: {
    dist: 'normal(0.13, 0.03) truncated [0.06, 0.25]', ci90: [0.08, 0.18],
    why: 'Comparative pre-modern agrarian extraction runs 10-20% of produce. The model taxes ' +
      'gross harvest, so the low end is the honest choice for a state without a standing bureaucracy.',
    replaceWith: 'temple and royal revenue figures from the inscription corpus'
  },
  rentRate: {
    dist: 'normal(0.30, 0.05) truncated [0.15, 0.45]', ci90: [0.22, 0.38],
    why: 'Share tenancy norms across monsoon Asia cluster at one third to one half of the crop. ' +
      'Not Angkor-specific; a comparative prior.',
    replaceWith: 'nothing available; this is the weakest of the social parameters'
  },
  crownShare: {
    dist: 'normal(0.45, 0.08) truncated [0.2, 0.7]', ci90: [0.32, 0.58],
    why: 'The share of elite rent the crown actually captures. No evidence either way; the ' +
      'range reflects whether the crown taxed elites directly or only through service.',
    replaceWith: 'any evidence on whether elite estates paid tax at all'
  },
  // ---- climate ----
  droughtSlope: {
    dist: 'lognormal(median 0.15, sigma 0.60)', ci90: [0.05, 0.45],
    why: 'Buckley et al. 2010 establish megadroughts in the 14th-15th c. from tree rings; the ' +
      'magnitude in yield terms is unknown, so the prior spans "barely matters" to "severe".',
    replaceWith: 'a calibrated yield-anomaly series from the tree-ring reconstruction'
  }
};

// draw one full parameter set
function sample(r) {
  var out = { meta: {} };
  out.y = lognorm(1.30, 0.20, r);
  out.riceKg = truncNorm(200, 25, 150, 250, r);
  out.Amax = lognorm(1100, 0.28, r);
  out.endowRate = lognorm(0.0011, 0.45, r);
  out.eliteGrow = lognorm(0.0020, 0.50, r);
  out.taxRate = truncNorm(0.13, 0.03, 0.06, 0.25, r);
  out.rentRate = truncNorm(0.30, 0.05, 0.15, 0.45, r);
  out.crownShare = truncNorm(0.45, 0.08, 0.20, 0.70, r);
  out.droughtSlope = lognorm(0.15, 0.60, r);
  // keep the identity visible in the output
  out.meta.peopleFed = Math.round((out.Amax * 100 * out.y * (1 - 0.16)) / (out.riceKg / 1000));
  return out;
}

module.exports = { PRIORS: PRIORS, sample: sample };
