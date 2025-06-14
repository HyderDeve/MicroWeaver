import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import UserMenu from './components/UserMenu';
import AuthModal from './components/auth/AuthModal';

function App() {
  const [prompt, setPrompt] = useState('');
  const [output, setOutput] = useState(null);
  const [loading, setLoading] = useState(false);
  const [chats, setChats] = useState([]);
  const [activeChat, setActiveChat] = useState(null);
  const [isAuthOpen, setIsAuthOpen] = useState(false);

  useEffect(() => {
    const savedChats = sessionStorage.getItem('chats');
    if (savedChats) {
      setChats(JSON.parse(savedChats));
    }
  }, []);

  useEffect(() => {
    sessionStorage.setItem('chats', JSON.stringify(chats));
  }, [chats]);

  const createNewChat = () => {
    const newChat = {
      id: Date.now().toString(),
      name: `New Chat ${chats.length + 1}`,
      messages: []
    };
    setChats([...chats, newChat]);
    setActiveChat(newChat.id);
    setOutput(null);
    setPrompt('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!prompt.trim() || !activeChat) return;

    setLoading(true);
    
    const updatedChats = chats.map(chat => {
      if (chat.id === activeChat) {
        return {
          ...chat,
          messages: [...chat.messages, { role: 'user', content: prompt }]
        };
      }
      return chat;
    });
    setChats(updatedChats);
    
    try {
      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt })
      });
      
      const data = await response.json();
      setOutput(data);

      const chatsWithResponse = updatedChats.map(chat => {
        if (chat.id === activeChat) {
          return {
            ...chat,
            messages: [...chat.messages, { 
              role: 'assistant', 
              content: JSON.stringify(data, null, 2)
            }]
          };
        }
        return chat;
      });
      setChats(chatsWithResponse);
    } catch (error) {
      console.error('Error generating project:', error);
    } finally {
      setLoading(false);
      setPrompt('');
    }
  };

  return (
    <div className="flex min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      <Sidebar
        chats={chats}
        activeChat={activeChat}
        onChatSelect={setActiveChat}
        onNewChat={createNewChat}
      />
      
      <div className="flex-1 flex flex-col">
        <div className="p-4 border-b border-gray-200 bg-white flex justify-end">
          <UserMenu onOpenAuth={() => setIsAuthOpen(true)} />
        </div>

        <div className="flex-1 py-8 px-4 sm:px-6 lg:px-8 overflow-y-auto">
          <div className="max-w-3xl mx-auto">
            <h1 className="text-4xl font-bold text-center text-gray-900 mb-8">
              AI Project Generator
            </h1>
            
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="rounded-lg bg-white shadow-sm border border-gray-200 p-4">
                <textarea
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  placeholder="Describe your project idea (e.g., 'Create a product catalog service with REST APIs')..."
                  className="w-full h-32 p-3 border-0 focus:ring-0 resize-none text-gray-900 placeholder-gray-400"
                />
              </div>
              
              <div className="flex justify-center">
                <button
                  type="submit"
                  disabled={loading || !prompt.trim() || !activeChat}
                  className={`px-6 py-3 rounded-lg text-white font-medium transition
                    ${loading || !prompt.trim() || !activeChat
                      ? 'bg-gray-400 cursor-not-allowed'
                      : 'bg-primary hover:bg-secondary'}`}
                >
                  {loading ? 'Generating...' : 'Generate Project'}
                </button>
              </div>
            </form>

            {activeChat && chats.find(chat => chat.id === activeChat)?.messages.map((message, index) => (
              <div key={index} className="mt-8">
                <div className={`rounded-lg p-4 ${message.role === 'user' ? 'bg-primary text-white' : 'bg-white border border-gray-200'}`}>
                  {message.role === 'assistant' ? (
                    <div className="space-y-6">
                      {(() => {
                        const data = JSON.parse(message.content);
                        return (
                          <>
                            {data.files && (
                              <div>
                                <h2 className="text-xl font-semibold text-gray-900 mb-4">Project Structure</h2>
                                <pre className="bg-gray-50 rounded p-4 overflow-x-auto">
                                  {data.files.join('\n')}
                                </pre>
                              </div>
                            )}
                            
                            {data.preview && (
                              <div>
                                <h2 className="text-xl font-semibold text-gray-900 mb-4">Main File Preview</h2>
                                <pre className="bg-gray-50 rounded p-4 overflow-x-auto">
                                  {data.preview}
                                </pre>
                              </div>
                            )}
                            
                            {data.dockerfile && (
                              <div>
                                <h2 className="text-xl font-semibold text-gray-900 mb-4">Dockerfile</h2>
                                <pre className="bg-gray-50 rounded p-4 overflow-x-auto">
                                  {data.dockerfile}
                                </pre>
                              </div>
                            )}
                          </>
                        );
                      })()}
                    </div>
                  ) : (
                    <div>{message.content}</div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <AuthModal
        isOpen={isAuthOpen}
        onClose={() => setIsAuthOpen(false)}
      />
    </div>
  );
}

export default App;