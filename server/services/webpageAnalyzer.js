import * as cheerio from "cheerio";
const loginTerms = ['login', 'sign in', 'password', 'verify', 'account', 'secure', 'authentication'];
export async function analyzeWebpage(url) {
  const controller = new AbortController(); const timeout = setTimeout(() => controller.abort(), 7000);
  try {
    const response = await fetch(url, { signal: controller.signal, redirect: 'follow', headers: {'User-Agent':'PhishingDomainDetector/1.0 (passive educational analysis)'} });
    if (!response.ok || !response.headers.get('content-type')?.includes('text/html')) throw new Error('The address did not return an HTML page.');
    const text = await response.text(); const html = text.slice(0, 1_000_000); const $ = cheerio.load(html); const visible = $('body').text().toLowerCase();
    return { available: true, warning: null, features: { formCount:$('form').length,inputCount:$('input').length,passwordFieldCount:$('input[type="password"]').length,buttonCount:$('button').length,linkCount:$('a').length,imageCount:$('img').length,scriptCount:$('script').length,loginTerms:loginTerms.filter(term=>visible.includes(term)) } };
  } catch { return { available:false, warning:'Unable to retrieve the webpage. Domain-level analysis was still completed.', features:{formCount:0,inputCount:0,passwordFieldCount:0,buttonCount:0,linkCount:0,imageCount:0,scriptCount:0,loginTerms:[]} }; } finally { clearTimeout(timeout); }
}
