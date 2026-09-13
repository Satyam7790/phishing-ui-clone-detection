import express from 'express'; import cors from 'cors'; import analyzeRoutes from './routes/analyzeRoutes.js';
const app = express(); app.use(cors()); app.use(express.json({limit:'20kb'})); app.get('/api/health', (_req,res)=>res.json({status:'ok'})); app.use('/api', analyzeRoutes);
app.use((err,_req,res,_next)=>res.status(500).json({error:'Unexpected server error.'}));
const port = process.env.PORT || 5000; app.listen(port,()=>console.log(`API listening at http://localhost:${port}`)); export default app;
