import test from 'node:test'; import assert from 'node:assert/strict'; import { analyzeUrl } from '../services/urlAnalyzer.js';
test('extracts expected suspicious URL signals',()=>{ const result=analyzeUrl('https://login.g00gle-security-example.com/path'); assert.equal(result.features.digitCount,2); assert.equal(result.features.hyphenCount,2); assert.equal(result.features.subdomainCount,1); });
test('rejects invalid URLs',()=>assert.throws(()=>analyzeUrl('hello')));
