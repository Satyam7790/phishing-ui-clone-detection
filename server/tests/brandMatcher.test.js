import test from 'node:test'; import assert from 'node:assert/strict'; import { findBrandMatch } from '../services/brandMatcher.js';
test('finds a PayPal lookalike',()=>{const result=findBrandMatch('paypa1-login.com');assert.equal(result.brand,'PayPal');assert.ok(result.similarity>.8)});
test('does not force unrelated matches',()=>assert.equal(findBrandMatch('student-project-site.com').brand,null));
