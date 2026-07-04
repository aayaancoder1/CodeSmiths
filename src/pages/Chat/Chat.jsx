import React, { useState, useEffect, useRef } from 'react';
import Button from '../../components/ui/Buttons/Button';
import Avatar from '../../components/ui/Feedback/Avatar';
import Badge from '../../components/ui/Feedback/Badge';
import Skeleton from '../../components/ui/Feedback/Skeleton';
import EmptyState from '../../components/ui/Feedback/EmptyState';
import { chatService } from '../../services/chatService';
import { useToast } from '../../context/ToastContext';

const Chat = () => {
  const { addToast } = useToast();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    const fetchHistory = async () => {
      setLoading(true);
      setError(null);
      try {
        const history = await chatService.getHistory('session-1');
        setMessages(history);
      } catch (err) {
        console.error('Error fetching chat history:', err);
        setError('Failed to load conversation history.');
        addToast({
          message: 'Chat Error',
          description: 'Could not load conversation history.',
          variant: 'danger'
        });
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, [addToast]);

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

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const handleSend = async (e) => {
    if (e) e.preventDefault();
    if (!input.trim() || isTyping) return;

    const userMessage = {
      id: Date.now(),
      sender: 'user',
      text: input,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages((prev) => [...prev, userMessage]);
    const querySent = input;
    setInput('');
    setIsTyping(true);

    try {
      const response = await chatService.sendMessage('session-1', querySent);
      const botMessage = {
        id: Date.now() + 1,
        sender: 'assistant',
        text: response.text,
        time: response.timestamp
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      console.error('Error sending message:', err);
      addToast({
        message: 'Message Failed',
        description: 'Could not send message. Please try again.',
        variant: 'danger'
      });
      // Remove last user message on failure
      setMessages((prev) => prev.filter((m) => m.id !== userMessage.id));
    } finally {
      setIsTyping(false);
      // Refocus input after response
      setTimeout(() => inputRef.current?.focus(), 50);
    }
  };

  const handlePromptClick = (prompt) => {
    setInput(prompt);
    inputRef.current?.focus();
  };

  // Keyboard handler for chat: Ctrl+Enter sends
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  // Loading skeleton for chat history
  const ChatSkeleton = () => (
    <div className="space-y-6 p-6">
      {Array.from({ length: 3 }).map((_, i) => (
        <div key={i} className={`flex gap-3 max-w-3xl ${i % 2 === 0 ? 'mr-auto' : 'ml-auto flex-row-reverse'}`}>
          <Skeleton variant="circle" className="w-8 h-8 shrink-0" aria-hidden="true" />
          <div className="space-y-1.5 flex-1">
            <Skeleton variant="rect" className={`h-16 rounded-2xl ${i % 2 === 0 ? 'rounded-tl-none' : 'rounded-tr-none'}`} aria-hidden="true" />
            <Skeleton variant="text" className="w-12 h-2.5" aria-hidden="true" />
          </div>
        </div>
      ))}
    </div>
  );

  return (
    <div
      className="flex h-[75vh] w-full border border-ui-border rounded-2xl overflow-hidden bg-ui-bg/30"
      role="main"
      aria-label="Chat workspace"
    >

      {/* Left Sidebar: Conversation History (Hidden on mobile) */}
      <aside className="hidden md:flex flex-col w-64 border-r border-ui-border bg-ui-surface/50" aria-label="Conversation history">
        <div className="p-4 border-b border-ui-divider">
          <Button variant="outline" className="w-full flex items-center justify-center gap-2" size="sm" aria-label="Start new chat session">
            <span aria-hidden="true">+</span> New Chat Session
          </Button>
        </div>
        <div className="flex-1 overflow-y-auto p-3 space-y-1">
          <span className="text-[10px] font-semibold uppercase text-ui-text-tertiary tracking-wider px-2 block mb-2">
            History
          </span>
          {conversationHistory.map((history) => (
            <button
              key={history.id}
              className={`w-full text-left px-3 py-2 text-xs font-medium rounded-xl truncate transition-all focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-500/50 ${
                history.active
                  ? 'bg-brand-500/10 text-brand-400 border border-brand-500/20'
                  : 'text-ui-text-secondary hover:bg-ui-surface hover:text-ui-text-primary'
              }`}
              aria-current={history.active ? 'true' : undefined}
            >
              <span aria-hidden="true">💬 </span>{history.title}
            </button>
          ))}
        </div>
      </aside>

      {/* Main Chat Workspace */}
      <div className="flex-1 flex flex-col min-w-0 bg-ui-bg/10">

        {/* Chat Header */}
        <header className="h-14 border-b border-ui-divider px-6 flex items-center justify-between bg-ui-surface/20 shrink-0">
          <div className="flex items-center gap-3">
            <Avatar name="AI Assistant" size="sm" status="online" />
            <div>
              <h1 className="text-xs font-bold text-ui-text-primary">Corporate Brain AI</h1>
              <p className="text-[10px] text-ui-text-tertiary">Indexed Knowledge Base Graph Assistant</p>
            </div>
          </div>
          <Badge variant="brand" size="sm">GPT-4 Node Model</Badge>
        </header>

        {/* Message Area */}
        <div
          className="flex-grow overflow-y-auto space-y-6"
          role="log"
          aria-label="Chat messages"
          aria-live="polite"
        >
          {loading ? (
            <ChatSkeleton />
          ) : error ? (
            <div className="p-6">
              <EmptyState
                title="Could not load conversation"
                description={error}
                action={
                  <Button
                    variant="primary"
                    size="sm"
                    onClick={() => window.location.reload()}
                  >
                    Retry
                  </Button>
                }
              />
            </div>
          ) : (
            <div className="p-6 space-y-6">
              {messages.map((msg) => {
                const isUser = msg.sender === 'user';
                return (
                  <div
                    key={msg.id}
                    className={`flex gap-3 max-w-3xl ${isUser ? 'ml-auto flex-row-reverse' : 'mr-auto'}`}
                    role="article"
                    aria-label={`${isUser ? 'Your message' : 'Assistant message'}: ${msg.text}`}
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
                        <time>{msg.time}</time>
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          )}

          {isTyping && (
            <div className="px-6 pb-2 flex gap-3 max-w-xl" aria-label="Assistant is typing" aria-live="assertive">
              <Avatar name="AI" size="sm" className="shrink-0" />
              <div className="bg-ui-surface border border-ui-border p-4 rounded-2xl rounded-tl-none">
                <div className="flex items-center gap-1.5 py-1" aria-hidden="true">
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
          {!loading && !error && messages.length <= 1 && !isTyping && (
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mb-4 max-w-4xl mx-auto">
              {suggestedPrompts.map((p, idx) => (
                <button
                  key={idx}
                  onClick={() => handlePromptClick(p)}
                  className="text-left p-3 text-xs border border-ui-border bg-ui-bg hover:bg-ui-surfaceHover hover:border-ui-borderHover rounded-xl text-ui-text-secondary hover:text-ui-text-primary transition-all focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-500/50"
                  aria-label={`Use suggested prompt: ${p}`}
                >
                  <span aria-hidden="true">💡 </span>{p}
                </button>
              ))}
            </div>
          )}

          {/* Form */}
          <form onSubmit={handleSend} className="flex gap-3 max-w-4xl mx-auto" role="search" aria-label="Send a message">
            <label htmlFor="chat-input" className="sr-only">Type your message</label>
            <input
              id="chat-input"
              ref={inputRef}
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              disabled={isTyping || loading}
              placeholder="Ask anything about the company's knowledge map..."
              className="flex-1 bg-ui-bg border border-ui-border text-ui-text-primary rounded-xl text-xs px-4 py-3 focus:outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/10 placeholder-ui-text-tertiary disabled:opacity-50 transition-colors"
              autoComplete="off"
            />
            <Button
              type="submit"
              variant="primary"
              disabled={!input.trim() || isTyping || loading}
              aria-label="Send message"
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
