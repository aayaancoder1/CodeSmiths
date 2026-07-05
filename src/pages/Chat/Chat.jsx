import React, { useState, useEffect, useRef } from 'react';
import Button from '../../components/ui/Buttons/Button';
import Avatar from '../../components/ui/Feedback/Avatar';
import Badge from '../../components/ui/Feedback/Badge';
import Skeleton from '../../components/ui/Feedback/Skeleton';
import EmptyState from '../../components/ui/Feedback/EmptyState';
import { chatService } from '../../services/chatService';
import { useToast } from '../../context/ToastContext';

// --- Structured Answer Card Component ---
const AssistantAnswerCard = ({ message, onToast }) => {
  // Render simple welcome message if no raw payload exists
  if (!message.raw) {
    return (
      <div className="bg-ui-surface border border-ui-border text-ui-text-secondary p-4 rounded-2xl rounded-tl-none text-xs leading-relaxed shadow-lg max-w-xl">
        {message.text}
      </div>
    );
  }

  const { answer, sources, entities, relationships } = message.raw;

  // Simple Markdown formatter for Gemini response (bolds, bullets, lists, headings)
  const formatText = (txt) => {
    if (!txt) return '';
    return txt.split('\n').map((line, i) => {
      const parts = [];
      let lastIdx = 0;
      const regex = /\*\*(.*?)\*\*/g;
      let match;
      while ((match = regex.exec(line)) !== null) {
        if (match.index > lastIdx) {
          parts.push(line.substring(lastIdx, match.index));
        }
        parts.push(<strong key={match.index} className="text-white font-bold">{match[1]}</strong>);
        lastIdx = regex.lastIndex;
      }
      if (lastIdx < line.length) {
        parts.push(line.substring(lastIdx));
      }

      if (line.startsWith('* ') || line.startsWith('- ')) {
        return <li key={i} className="ml-4 list-disc text-ui-text-secondary mb-1">{parts}</li>;
      }
      if (line.startsWith('### ')) {
        return <h4 key={i} className="text-xs font-bold text-slate-100 mt-4 mb-2 uppercase tracking-wide">{parts}</h4>;
      }
      if (line.startsWith('## ')) {
        return <h3 key={i} className="text-sm font-bold text-white mt-5 mb-2.5 border-b border-ui-divider pb-1">{parts}</h3>;
      }
      if (line.startsWith('# ')) {
        return <h2 key={i} className="text-base font-extrabold text-white mt-6 mb-3">{parts}</h2>;
      }
      return line.trim() ? <p key={i} className="mb-2.5 text-ui-text-secondary leading-relaxed">{parts}</p> : <div key={i} className="h-1" />;
    });
  };

  return (
    <div className="bg-ui-surface/65 backdrop-blur-md border border-ui-border p-6 rounded-2xl rounded-tl-none shadow-2xl space-y-6 max-w-3xl animate-fade-in">
      {/* Title Header */}
      <div className="flex items-center justify-between pb-3 border-b border-ui-divider">
        <h3 className="text-xs font-bold text-slate-100 uppercase tracking-wider flex items-center gap-2">
          <span className="w-2.5 h-2.5 rounded-full bg-brand-500 animate-pulse" /> Grounded Synthesis Response
        </h3>
        <Badge variant="success" size="sm">Verified GraphRAG</Badge>
      </div>

      {/* Answer Paragraphs */}
      <div className="text-xs space-y-1">
        {formatText(answer)}
      </div>

      {/* Supporting Relations */}
      {relationships && relationships.length > 0 && (
        <div className="space-y-2 pt-2">
          <h4 className="text-[10px] font-semibold text-ui-text-tertiary uppercase tracking-wider">Supporting Graph Relations</h4>
          <div className="bg-ui-bg/80 border border-ui-border rounded-xl p-3.5 space-y-2 font-mono text-[10px]">
            {relationships.map((rel, idx) => (
              <div key={idx} className="flex items-center gap-1.5 flex-wrap">
                <span className="text-brand-400 font-bold">{rel.source_id}</span>
                <span className="text-ui-text-tertiary">➔</span>
                <span className="px-1.5 py-0.5 bg-brand-500/10 border border-brand-500/20 text-brand-400 rounded text-[9px] font-sans font-bold uppercase tracking-wider">{rel.type}</span>
                <span className="text-ui-text-tertiary">➔</span>
                <span className="text-emerald-400 font-bold">{rel.target_id}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Sources Grid */}
      {sources && sources.length > 0 && (
        <div className="space-y-2">
          <h4 className="text-[10px] font-semibold text-ui-text-tertiary uppercase tracking-wider">Retrieved Source Documents</h4>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            {sources.map((src, idx) => (
              <div key={idx} className="flex items-center gap-2.5 p-2.5 bg-ui-bg/30 border border-ui-border rounded-xl hover:border-brand-500/30 transition-all select-text">
                <span className="text-base select-none">📄</span>
                <div className="min-w-0">
                  <span className="text-[9px] text-ui-text-tertiary block font-mono">Source [{src.index}]</span>
                  <span className="text-xs font-bold text-slate-100 truncate block">{src.document_id}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Entity Pills */}
      {entities && entities.length > 0 && (
        <div className="space-y-2">
          <h4 className="text-[10px] font-semibold text-ui-text-tertiary uppercase tracking-wider">Linked Graph Entities</h4>
          <div className="flex flex-wrap gap-2">
            {entities.map((ent, idx) => {
              const label = ent.label?.toLowerCase() || 'entity';
              let colorClasses = 'bg-slate-500/10 border-slate-500/20 text-slate-400';
              let icon = '⚪';
              if (label === 'service') {
                colorClasses = 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400';
                icon = '🟢';
              } else if (label === 'incident') {
                colorClasses = 'bg-red-500/10 border-red-500/20 text-red-400';
                icon = '🔴';
              } else if (label === 'document') {
                colorClasses = 'bg-blue-500/10 border-blue-500/20 text-blue-400';
                icon = '🔵';
              } else if (label === 'slack thread' || label === 'ticket') {
                colorClasses = 'bg-purple-500/10 border-purple-500/20 text-purple-400';
                icon = '🟣';
              }

              return (
                <div key={idx} className={`inline-flex items-center gap-1.5 px-2.5 py-1 border rounded-lg text-[10px] font-bold ${colorClasses}`}>
                  <span className="select-none">{icon}</span>
                  <span>{ent.node_id}</span>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};

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
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, []);

  const conversationHistory = [
    { id: '1', title: 'Payment Outage Investigation', active: true }
  ];

  const suggestedPrompts = [
    'What caused the payment outage?',
    'Which service failed?',
    'What does the Slack thread reference?',
    'Explain Incident #1001.',
    'Which documents support the outage analysis?'
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
        text: response.raw.answer,
        raw: response.raw,
        time: response.timestamp
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      console.error('Error sending message:', err);
      addToast({
        message: 'Query Failed',
        description: 'Failed to retrieve response from GraphRAG endpoint.',
        variant: 'danger'
      });
      setMessages((prev) => prev.filter((m) => m.id !== userMessage.id));
    } finally {
      setIsTyping(false);
      setTimeout(() => inputRef.current?.focus(), 50);
    }
  };

  const handlePromptClick = (prompt) => {
    setInput(prompt);
    inputRef.current?.focus();
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const ChatSkeleton = () => (
    <div className="space-y-6 p-6">
      {Array.from({ length: 2 }).map((_, i) => (
        <div key={i} className={`flex gap-3 max-w-3xl ${i % 2 === 0 ? 'mr-auto' : 'ml-auto flex-row-reverse'}`}>
          <Skeleton variant="circle" className="w-8 h-8 shrink-0" />
          <div className="space-y-1.5 flex-1">
            <Skeleton variant="rect" className="h-16 rounded-2xl" />
            <Skeleton variant="text" className="w-12 h-2.5" />
          </div>
        </div>
      ))}
    </div>
  );

  return (
    <div className="flex h-[78vh] w-full border border-ui-border rounded-2xl overflow-hidden bg-ui-surface/20 backdrop-blur-md">
      {/* Sidebar history */}
      <aside className="hidden md:flex flex-col w-64 border-r border-ui-border bg-ui-bg/50">
        <div className="p-4 border-b border-ui-divider">
          <Button variant="outline" className="w-full flex items-center justify-center gap-2" size="sm">
            <span>+</span> New Session
          </Button>
        </div>
        <div className="flex-grow p-3 space-y-1 overflow-y-auto">
          <span className="text-[9px] font-bold uppercase text-ui-text-tertiary tracking-widest px-2 block mb-2">History</span>
          {conversationHistory.map((h) => (
            <button
              key={h.id}
              className="w-full text-left px-3 py-2 text-xs font-bold rounded-xl truncate transition-all bg-brand-500/10 text-brand-400 border border-brand-500/20"
            >
              💬 {h.title}
            </button>
          ))}
        </div>
      </aside>

      {/* Main Workspace */}
      <div className="flex-1 flex flex-col min-w-0 bg-ui-bg/10">
        {/* Header */}
        <header className="h-14 border-b border-ui-divider px-6 flex items-center justify-between bg-ui-surface/30 shrink-0">
          <div className="flex items-center gap-3">
            <Avatar name="Corporate Brain AI" size="sm" status="online" />
            <div>
              <h1 className="text-xs font-extrabold text-white">Corporate Brain AI</h1>
              <p className="text-[10px] text-ui-text-tertiary">Indexed Knowledge Base GraphRAG Assistant</p>
            </div>
          </div>
          <Badge variant="brand" size="sm">Gemini 2.5 Flash</Badge>
        </header>

        {/* Message Area */}
        <div className="flex-grow overflow-y-auto space-y-6">
          {loading ? (
            <ChatSkeleton />
          ) : (
            <div className="p-6 space-y-6">
              {messages.map((msg) => {
                const isUser = msg.sender === 'user';
                return (
                  <div key={msg.id} className={`flex gap-3 max-w-3xl ${isUser ? 'ml-auto flex-row-reverse' : 'mr-auto'}`}>
                    <Avatar name={isUser ? 'Admin' : 'AI'} size="sm" className="shrink-0" />
                    <div className="space-y-1">
                      {isUser ? (
                        <div className="p-4 rounded-2xl text-xs leading-relaxed bg-brand-500 text-white rounded-tr-none shadow-lg shadow-brand-500/10">
                          {msg.text}
                        </div>
                      ) : (
                        <AssistantAnswerCard message={msg} onToast={addToast} />
                      )}
                      <span className="text-[9px] text-ui-text-tertiary block px-1">
                        <time>{msg.time || msg.timestamp}</time>
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          )}

          {/* Thinking Indicator */}
          {isTyping && (
            <div className="px-6 pb-2 flex gap-3 max-w-xl animate-pulse">
              <Avatar name="AI" size="sm" className="shrink-0" />
              <div className="bg-ui-surface border border-ui-border p-4 rounded-2xl rounded-tl-none space-y-2">
                <div className="flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-brand-500 animate-ping" />
                  <span className="text-[10px] font-bold text-brand-400 uppercase tracking-widest">Pipeline executing GraphRAG traversal...</span>
                </div>
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

        {/* Input & Suggestions */}
        <div className="p-4 border-t border-ui-divider bg-ui-surface/20 shrink-0">
          {!loading && messages.length <= 1 && !isTyping && (
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-3 mb-4 max-w-5xl mx-auto">
              {suggestedPrompts.map((p, idx) => (
                <button
                  key={idx}
                  onClick={() => handlePromptClick(p)}
                  className="text-left p-3 text-xs border border-ui-border bg-ui-bg hover:bg-ui-surfaceHover hover:border-brand-500/30 rounded-xl text-ui-text-secondary hover:text-white transition-all focus:outline-none"
                >
                  💡 {p}
                </button>
              ))}
            </div>
          )}

          <form onSubmit={handleSend} className="flex gap-3 max-w-4xl mx-auto">
            <input
              ref={inputRef}
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              disabled={isTyping || loading}
              placeholder="Ask anything about the payment outage or Redis..."
              className="flex-1 bg-ui-bg border border-ui-border text-ui-text-primary rounded-xl text-xs px-4 py-3 focus:outline-none focus:border-brand-500 placeholder-ui-text-tertiary disabled:opacity-50 transition-colors"
              autoComplete="off"
            />
            <Button type="submit" variant="primary" disabled={!input.trim() || isTyping || loading}>
              Send Query
            </Button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Chat;
