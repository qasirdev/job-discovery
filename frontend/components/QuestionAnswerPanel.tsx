'use client';

import React, { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { TextField, Button, CircularProgress } from '@mui/material';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export default function QuestionAnswerPanel({ jobId }: { jobId: string }) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');

  const getApiUrl = (endpoint: string) => {
    const apiBase = process.env.NEXT_PUBLIC_API_URL || '/api/v1';
    const isDev = typeof window !== 'undefined' && window.location.hostname === 'localhost';
    const base = isDev ? 'http://localhost:8000/api/v1' : apiBase;
    const cleanBase = base.endsWith('/') ? base.slice(0, -1) : base;
    const cleanEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
    return `${cleanBase}${cleanEndpoint}`;
  };

  const askQuestion = useMutation({
    mutationFn: async (question: string) => {
      const res = await fetch(getApiUrl(`/question-answer/${jobId}`), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question })
      });
      if (!res.ok) throw new Error('Failed to get answer');
      return res.json();
    },
    onSuccess: (data) => {
      setMessages(prev => [...prev, { role: 'assistant', content: data.answer || "Sorry, I couldn't process that." }]);
    },
    onError: (error: any) => {
      setMessages(prev => [...prev, { role: 'assistant', content: `Error: ${error.message}` }]);
    }
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;
    
    setMessages(prev => [...prev, { role: 'user', content: input }]);
    askQuestion.mutate(input);
    setInput('');
  };

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 flex flex-col h-[500px]">
      <h3 className="text-xl font-bold text-gray-900 mb-4 pb-2 border-b border-gray-100">Ask about this Job</h3>
      
      <div className="flex-1 overflow-y-auto space-y-4 mb-4 pr-2">
        {messages.length === 0 ? (
          <div className="text-center text-gray-400 mt-10 italic">
            Ask any question about the company, role, or requirements.
          </div>
        ) : (
          messages.map((msg, i) => (
            <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-[85%] p-3 rounded-xl ${
                msg.role === 'user' 
                  ? 'bg-indigo-600 text-white rounded-br-none' 
                  : 'bg-gray-100 text-gray-800 rounded-bl-none border border-gray-200'
              }`}>
                {msg.content}
              </div>
            </div>
          ))
        )}
      </div>

      <form onSubmit={handleSubmit} className="flex gap-2 items-center">
        <TextField
          fullWidth
          size="small"
          placeholder="Type your question..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={askQuestion.isPending}
          variant="outlined"
          className="bg-gray-50"
        />
        <Button 
          type="submit" 
          variant="contained" 
          disabled={!input.trim() || askQuestion.isPending}
          className="bg-indigo-600 shadow-none hover:bg-indigo-700 min-w-[100px] h-10"
        >
          {askQuestion.isPending ? <CircularProgress size={24} color="inherit" /> : 'Ask'}
        </Button>
      </form>
    </div>
  );
}
