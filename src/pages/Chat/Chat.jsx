import React, { useState, useEffect, useRef } from 'react';
import Button from '../../components/ui/Buttons/Button';
import Avatar from '../../components/ui/Feedback/Avatar';
import Card from '../../components/ui/Cards/Card';

const Chat = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'assistant',
      text: 'Hello! I am your AI Enterprise Assistant. Ask me any question related to indexed drives, Notion docs, Slack messages, or GitHub logs.',
      time: '10:00 AM'
    }
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  
  const messagesEndRef = useRef(null);

  const conversationHistory = [
    { id: '1', title: 'AWS IAM configuration issues', active: true },
    { id: '2', title: 'Notion SSO credentials info', active: false },
    { id: '3', title: 'Q3 ingestion log status', active: false },
    { id: '4', title: 'Docker container latency debug', active: false }
  ];

  const suggestedPrompts = [
    'How do I sync AWS microservices?',
    'Show me the recent Notion onboarding checklists',
    'Why did the GDrive indexing script warn?'
  ];

  // Auto-scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const handleSend = (e) => {
    if (e) e.preventDefault();
    if (!input.trim()) return;

    const userMessage = {
      id: Date.now(),
      sender: 'user',
      text: input,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsTyping(true);

    // Simulate AI response delay
    setTimeout(() => {
      setIsTyping(false);
      const botMessage = {
        id: Date.now() + 1,
        sender: 'assistant',
        text: `Here is what I found regarding "${userMessage.text}". Based on Notion page "SSO Integration Guide" (page 2) and Google Drive file "security-policy-v4.pdf", you can find detailed setup checklists with 94% relevance. Would you like me to extract the steps for you?`,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages((prev) => [...prev, botMessage]);
    }, 1500);
  };

  const handlePromptClick = (prompt) => {
    setInput(prompt);
  };

  return (
    <div className="flex h-[75vh] w-full border border-ui-border rounded-2xl overflow-hidden bg-ui-bg/30">
      
      {/* Left Sidebar: Conversation History (Hidden on mobile) */}
      <div className="hidden md:flex flex-col w-64 border-r border-ui-border bg-ui-surface/50">
        <div className="p-4 border-b border-ui-divider">
          <Button variant="outline" className="w-full flex items-center justify-center gap-2" size="sm">
            <span>+</span> New Chat Session
          </Button>
        </div>
        <div className="flex-1 overflow-y-auto p-3 space-y-1">
          <span className="text-[10px] font-semibold uppercase text-ui-text-tertiary tracking-wider px-2 block mb-2">History</span>
          {conversationHistory.map((history) => (
            <button
              key={history.id}
              className={`w-full text-left px-3 py-2 text-xs font-medium rounded-xl truncate transition-all ${
                history.active 
                  ? 'bg-brand-500/10 text-brand-400 border border-brand-500/20' 
                  : 'text-ui-text-secondary hover:bg-ui-surface hover:text-ui-text-primary'
              }`}
            >
              💬 {history.title}
            </button>
          ))}
        </div>
      </div>

      {/* Main Chat Workspace */}
      <div className="flex-1 flex flex-col min-w-0 bg-ui-bg/10">
        
        {/* Chat Header */}
        <div className="h-14 border-b border-ui-divider px-6 flex items-center justify-between bg-ui-surface/20 shrink-0">
          <div className="flex items-center gap-3">
            <Avatar name="AI Assistant" size="sm" status="online" />
            <div>
              <h3 className="text-xs font-bold text-ui-text-primary">Corporate Brain AI</h3>
              <p className="text-[10px] text-ui-text-tertiary">Indexed Knowledge Base Graph Assistant</p>
            </div>
          </div>
          <Badge variant="brand" size="sm">GPT-4 Node Model</Badge>
        </div>

        {/* Message Area */}
        <div className="flex-grow overflow-y-auto p-6 space-y-6">
          {messages.map((msg) => {
            const isUser = msg.sender === 'user';
            return (
              <div 
                key={msg.id} 
                className={`flex gap-3 max-w-3xl ${isUser ? 'ml-auto flex-row-reverse' : 'mr-auto'}`}
              >
                <Avatar 
                  name={isUser ? 'Thanmayee' : 'AI'} 
                  size="sm"
                  className="shrink-0"
                />
                <div className="space-y-1">
                  <div 
                    className={`p-4 rounded-2xl text-xs leading-relaxed ${
                      isUser 
                        ? 'bg-brand-500 text-white rounded-tr-none shadow-md shadow-brand-500/10' 
                        : 'bg-ui-surface border border-ui-border text-ui-text-secondary rounded-tl-none'
                    }`}
                  >
                    {msg.text}
                  </div>
                  <span className="text-[10px] text-ui-text-tertiary block px-1">
                    {msg.time}
                  </span>
                </div>
              </div>
            );
          })}

          {isTyping && (
            <div className="flex gap-3 max-w-xl">
              <Avatar name="AI" size="sm" className="shrink-0" />
              <div className="bg-ui-surface border border-ui-border p-4 rounded-2xl rounded-tl-none">
                <div className="flex items-center gap-1.5 py-1">
                  <span className="w-2 h-2 bg-brand-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                  <span className="w-2 h-2 bg-brand-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                  <span className="w-2 h-2 bg-brand-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input & Suggested Prompts Area */}
        <div className="p-4 border-t border-ui-divider bg-ui-surface/20 shrink-0">
          
          {/* Suggested prompts list */}
          {messages.length === 1 && !isTyping && (
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mb-4 max-w-4xl mx-auto">
              {suggestedPrompts.map((p, idx) => (
                <button
                  key={idx}
                  onClick={() => handlePromptClick(p)}
                  className="text-left p-3 text-xs border border-ui-border bg-ui-bg hover:bg-ui-surfaceHover hover:border-ui-borderHover rounded-xl text-ui-text-secondary hover:text-ui-text-primary transition-all focus:outline-none"
                >
                  💡 {p}
                </button>
              ))}
            </div>
          )}

          {/* Form */}
          <form onSubmit={handleSend} className="flex gap-3 max-w-4xl mx-auto">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={isTyping}
              placeholder="Ask anything about the company's knowledge map..."
              className="flex-1 bg-ui-bg border border-ui-border text-ui-text-primary rounded-xl text-xs px-4 py-3 focus:outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/10 placeholder-ui-text-tertiary disabled:opacity-50"
            />
            <Button 
              type="submit" 
              variant="primary" 
              disabled={!input.trim() || isTyping}
            >
              Send
            </Button>
          </form>
        </div>

      </div>
    </div>
  );
};

export default Chat;
