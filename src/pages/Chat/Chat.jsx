import React from 'react';
import PageContainer from '../../components/Common/PageContainer';
import PageHeader from '../../components/Common/PageHeader';
import Button from '../../components/Buttons/Button';
import Input from '../../components/Inputs/Input';

const Chat = () => {
  return (
    <PageContainer>
      <PageHeader 
        title="Chat UI" 
        subtitle="Interact with the knowledge agent retrieval system"
      />
      
      <div className="flex flex-col h-[550px] bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden">
        {/* Chat History Placeholder Area */}
        <div className="flex-1 p-6 overflow-y-auto space-y-4">
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 rounded-xl bg-brand-500 flex items-center justify-center font-bold text-xs">AI</div>
            <div className="bg-slate-800 p-4 rounded-2xl rounded-tl-none max-w-lg text-sm text-slate-200">
              Welcome! Ask me any question related to ingestion logs or the connected knowledge graph.
            </div>
          </div>
        </div>

        {/* Input Form Box */}
        <div className="p-4 border-t border-slate-800/80 bg-slate-900/60 flex items-center gap-3">
          <Input 
            placeholder="Type your question..." 
            className="flex-1"
          />
          <Button variant="primary">Send</Button>
        </div>
      </div>
    </PageContainer>
  );
};

export default Chat;
