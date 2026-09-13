import brands from "../data/legitimateDomains.json" with { type: "json" };
const substitute = value => value.toLowerCase().replace(/0/g, 'o').replace(/1/g, 'l').replace(/3/g, 'e').replace(/4/g, 'a').replace(/5/g, 's').replace(/7/g, 't').replace(/[^a-z0-9]/g, '');
export function levenshtein(left, right) { const row = Array.from({length:right.length+1},(_,i)=>i); for(let i=1;i<=left.length;i++){let prior=row[0];row[0]=i;for(let j=1;j<=right.length;j++){const old=row[j];row[j]=Math.min(row[j]+1,row[j-1]+1,prior+(left[i-1]!==right[j-1]));prior=old;}} return row[right.length]; }
export function findBrandMatch(domain) {
  const candidate = substitute(domain.split('.')[0]); let best = null;
  for (const item of brands) { const token = substitute(item.domain.split('.')[0]); let similarity = 1 - levenshtein(candidate, token) / Math.max(candidate.length, token.length, 1); if (candidate.includes(token) && candidate !== token) similarity = Math.max(similarity, Math.min(.95, .82 + token.length / candidate.length * .1)); if (!best || similarity > best.similarity) best = {...item, similarity: Number(similarity.toFixed(3))}; }
  return best && best.similarity >= .58 ? best : { brand: null, domain: null, similarity: 0 };
}
