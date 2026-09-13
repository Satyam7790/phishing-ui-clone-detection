/** Transparent prototype Risk Scoring Engine; replaceable with a trained model later. */
export function calculateRisk(urlFeatures, brandMatch, webFeatures) {
  let score = 4; const reasons = [];
  const add = (amount, explanation) => { score += amount; reasons.push(explanation); };
  if (brandMatch.similarity >= .85) add(48, `The domain closely resembles ${brandMatch.brand}.`);
  else if (brandMatch.similarity >= .68) add(25, `The domain has moderate similarity to ${brandMatch.brand}.`);
  if (urlFeatures.urlLength > 100) add(10, 'The URL is unusually long.');
  if (urlFeatures.hyphenCount >= 2) add(8, 'The domain contains multiple hyphens.');
  if (urlFeatures.subdomainCount >= 2) add(9, 'The URL has multiple subdomains.');
  if (urlFeatures.digitCount >= 2) add(8, 'The domain contains several digits.');
  if (urlFeatures.isIpAddress) add(20, 'An IP address is used instead of a domain name.');
  if (urlFeatures.hasPunycode || urlFeatures.hasUnicode) add(14, 'The domain uses an encoded or Unicode lookalike pattern.');
  if (urlFeatures.suspiciousStructure) add(8, 'The URL has an unusually complex structure.');
  if (webFeatures.passwordFieldCount > 0) add(7, 'A password input field was detected.');
  if (webFeatures.formCount > 0 && webFeatures.loginTerms.length > 0) add(6, 'A form and login-related page content were detected.');
  score = Math.min(99, score); const riskLevel = score < 30 ? 'LOW' : score < 70 ? 'SUSPICIOUS' : 'HIGH';
  return { phishingProbability: Number((score / 100).toFixed(2)), riskLevel, reasons: reasons.length ? reasons : ['No strong impersonation or suspicious URL signal was found.'] };
}
