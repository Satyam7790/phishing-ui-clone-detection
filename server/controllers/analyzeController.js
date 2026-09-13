import { analyze } from '../services/analysisService.js';
export async function analyzeController(req, res) { try { if (!req.body?.url) return res.status(400).json({error:'A URL is required.'}); return res.json(await analyze(req.body.url)); } catch (error) { return res.status(400).json({error:error.message || 'Unable to analyze this URL.'}); } }
