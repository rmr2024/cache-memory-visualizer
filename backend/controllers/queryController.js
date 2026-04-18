import Query from '../models/Query.js';

export const processQuery = async (req, res) => {
  try {
    const { question } = req.body;

    if (!question || typeof question !== 'string' || question.trim().length === 0) {
      return res.status(400).json({ error: 'Question is required and must be a non-empty string' });
    }

    if (question.length > 1000) {
      return res.status(400).json({ error: 'Question must be less than 1000 characters' });
    }

    const trimmedQuestion = question.trim();

    const groqResponse = await fetch('https://api.groq.com/openai/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.GROQ_API_KEY}`
      },
      body: JSON.stringify({
        model: 'llama-3.1-8b-instant',
        messages: [
          {
            role: 'user',
            content: trimmedQuestion
          }
        ],
        temperature: 0.7,
        max_tokens: 1024,
        top_p: 0.9
      })
    });

    if (!groqResponse.ok) {
      const errorData = await groqResponse.json();
      console.error('Groq API Error:', errorData);
      return res.status(502).json({ error: 'Failed to get response from AI service' });
    }

    const groqData = await groqResponse.json();
    const answer = groqData.choices?.[0]?.message?.content;

    if (!answer) {
      return res.status(502).json({ error: 'Invalid response from AI service' });
    }

    const savedQuery = await Query.create({
      question: trimmedQuestion,
      answer: answer
    });

    res.status(200).json({ answer });
  } catch (error) {
    console.error('Controller Error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
};