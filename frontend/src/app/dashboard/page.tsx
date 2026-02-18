"use client";

import { useState, useRef, useEffect } from 'react';
import { useAuth } from '@/context/AuthContext';
import { api } from '@/lib/api';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Send, Bot, User as UserIcon, Loader2, FileText } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { cn } from '@/lib/utils';
import { Source } from '@/types';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: Source[];
  timestamp: Date;
}

export default function ChatPage() {
  const { user } = useAuth();
  const scrollRef = useRef<HTMLDivElement>(null);
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    // Scroll to bottom on new message
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // POST /query
      const response = await api.post('/query', {
        question: userMessage.content,
        top_k: 5,
      });

      const data = response.data;
      
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.answer,
        sources: data.sources,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error("Chat error:", error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: "Sorry, I encountered an error processing your request. Please try again.",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-white dark:bg-zinc-950 rounded-xl shadow-sm overflow-hidden border dark:border-zinc-800">
      {/* Header */}
      <div className="p-4 border-b bg-zinc-50/50 dark:bg-zinc-900/50 flex items-center justify-between">
        <div>
          <h1 className="text-lg font-semibold text-zinc-900 dark:text-zinc-100">AI Assistant</h1>
          <p className="text-xs text-zinc-500">Ask questions about internal documents</p>
        </div>
      </div>

      {/* Messages Area */}
      <div 
        ref={scrollRef} 
        className="flex-1 overflow-y-auto p-4 space-y-6"
      >
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center p-8 text-zinc-400">
            <Bot size={48} className="mb-4 text-indigo-200" />
            <p className="text-lg font-medium text-zinc-600 dark:text-zinc-300">How can I help you today?</p>
            <p className="text-sm mt-2 max-w-sm">
              Ask me about company policies, technical docs, or HR guidelines.
            </p>
          </div>
        ) : (
          messages.map((msg) => (
            <div 
              key={msg.id} 
              className={cn(
                "flex gap-4 max-w-3xl mx-auto",
                msg.role === 'user' ? "justify-end" : "justify-start"
              )}
            >
              {/* Avatar (Bot) */}
              {msg.role === 'assistant' && (
                <div className="flex-shrink-0 h-8 w-8 rounded-full bg-indigo-100 dark:bg-indigo-900/30 flex items-center justify-center text-indigo-600 dark:text-indigo-400">
                  <Bot size={18} />
                </div>
              )}

              {/* Message Bubble */}
              <div 
                className={cn(
                  "flex-1 px-4 py-3 rounded-2xl text-sm leading-relaxed shadow-sm",
                  msg.role === 'user' 
                    ? "bg-indigo-600 text-white rounded-tr-sm" 
                    : "bg-white dark:bg-zinc-900 border dark:border-zinc-800 text-zinc-800 dark:text-zinc-200 rounded-tl-sm"
                )}
              >
                {msg.role === 'assistant' ? (
                  <div className="prose prose-sm dark:prose-invert max-w-none">
                     <ReactMarkdown>{msg.content}</ReactMarkdown>
                  </div>
                ) : (
                  <p>{msg.content}</p>
                )}

                {/* Sources */}
                {msg.sources && msg.sources.length > 0 && (
                  <div className="mt-4 pt-4 border-t border-zinc-100 dark:border-zinc-800">
                    <p className="text-xs font-semibold text-zinc-500 mb-2 flex items-center gap-1">
                      <FileText size={12} /> Sources:
                    </p>
                    <div className="flex flex-wrap gap-2">
                      {msg.sources.slice(0, 3).map((source, idx) => (
                        <div key={idx} className="bg-zinc-50 dark:bg-zinc-800 px-2 py-1 rounded text-xs text-zinc-600 dark:text-zinc-400 border dark:border-zinc-700 truncate max-w-[200px]" title={source.title}>
                          {idx + 1}. {source.title}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {/* Avatar (User) */}
              {msg.role === 'user' && (
                <div className="flex-shrink-0 h-8 w-8 rounded-full bg-zinc-200 dark:bg-zinc-800 flex items-center justify-center text-zinc-500">
                  <UserIcon size={18} />
                </div>
              )}
            </div>
          ))
        )}
        {isLoading && (
           <div className="flex gap-4 max-w-3xl mx-auto justify-start">
             <div className="flex-shrink-0 h-8 w-8 rounded-full bg-indigo-100 dark:bg-indigo-900/30 flex items-center justify-center text-indigo-600 dark:text-indigo-400">
                <Bot size={18} />
             </div>
             <div className="bg-white dark:bg-zinc-900 border dark:border-zinc-800 px-4 py-3 rounded-2xl rounded-tl-sm shadow-sm flex items-center">
                <Loader2 className="h-4 w-4 animate-spin text-zinc-400" />
                <span className="ml-2 text-xs text-zinc-500">Thinking...</span>
             </div>
           </div>
        )}
      </div>

      {/* Input Area */}
      <div className="p-4 border-t bg-white dark:bg-zinc-950">
        <form onSubmit={handleSend} className="max-w-3xl mx-auto relative flex items-center">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question..."
            className="pr-12 py-6 text-base rounded-full shadow-sm border-zinc-200 focus-visible:ring-indigo-500"
            disabled={isLoading}
          />
          <Button 
            type="submit" 
            size="sm"
            disabled={!input.trim() || isLoading}
            className="absolute right-2 h-8 w-8 p-0 rounded-full bg-indigo-600 hover:bg-indigo-700"
          >
            <Send size={16} />
          </Button>
        </form>
        <p className="text-center text-[10px] text-zinc-400 mt-2">
          AI generated answers may be inaccuracies. Always check sources.
        </p>
      </div>
    </div>
  );
}
