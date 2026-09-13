import { analyzeUrl } from './urlAnalyzer.js';
import { findBrandMatch } from './brandMatcher.js';
import { analyzeWebpage } from './webpageAnalyzer.js';
import { calculateRisk } from './riskAnalyzer.js';
export async function analyze(value) {
  const url = analyzeUrl(value); const match = findBrandMatch(url.domain); const webpage = await analyzeWebpage(url.parsed.href);
  const risk = calculateRisk(url.features, match, webpage.features);
  return { url:url.parsed.href, domain:url.domain, riskLevel:risk.riskLevel, phishingProbability:risk.phishingProbability, targetBrand:match.brand, targetDomain:match.domain, brandSimilarity:match.similarity, features:{...url.features, tld:url.tld, ...webpage.features}, reasons:risk.reasons, warning:webpage.warning };
}
