import net from "node:net";

export function validateUrl(value) {
  let parsed;
  try { parsed = new URL(value); } catch { throw new Error("Enter a complete http:// or https:// website URL."); }
  if (!['http:', 'https:'].includes(parsed.protocol)) throw new Error("Only HTTP and HTTPS URLs can be analyzed.");
  const host = parsed.hostname.toLowerCase();
  if (host === 'localhost' || host.endsWith('.local') || isPrivateAddress(host)) throw new Error("Local or private network addresses cannot be analyzed.");
  return parsed;
}

function isPrivateAddress(host) {
  if (!net.isIP(host)) return false;
  return host === '::1' || host.startsWith('127.') || host.startsWith('10.') || host.startsWith('192.168.') || /^172\.(1[6-9]|2\d|3[01])\./.test(host);
}

export function analyzeUrl(value) {
  const parsed = validateUrl(value);
  const host = parsed.hostname.toLowerCase().replace(/\.$/, '');
  const labels = host.split('.');
  const isIpAddress = Boolean(net.isIP(host));
  const domain = isIpAddress ? host : labels.slice(-2).join('.');
  const specialCharacterCount = (value.match(/[^a-zA-Z0-9./?=&_%:-]/g) || []).length;
  const features = {
    urlLength: value.length, domainLength: domain.length,
    digitCount: (host.match(/\d/g) || []).length, hyphenCount: (host.match(/-/g) || []).length,
    dotCount: (host.match(/\./g) || []).length, subdomainCount: Math.max(0, labels.length - 2),
    specialCharacterCount, hasHttps: parsed.protocol === 'https:', isIpAddress,
    hasPunycode: host.includes('xn--'), hasUnicode: /[^\u0000-\u007f]/.test(host),
    suspiciousStructure: value.length > 100 || labels.length > 4 || (host.match(/-/g) || []).length >= 3 || value.includes('@')
  };
  return { parsed, domain, tld: isIpAddress ? null : labels.at(-1), features };
}
