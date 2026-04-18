import express from 'express';
import { processQuery } from '../controllers/queryController.js';

const router = express.Router();

router.post('/query', processQuery);

export default router;