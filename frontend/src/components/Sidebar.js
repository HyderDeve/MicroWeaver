import React from 'react';

function Sidebar({ chats, activeChat, onChatSelect, onNewChat }) {
  return (
    <div className="w-64 bg-white border-r border-gray-200 h-screen flex flex-col">
      <div className="p-4 border-b border-gray-200">
        <button
          onClick={onNewChat}
          className="w-full bg-primary hover:bg-secondary text-white font-medium py-2 px-4 rounded-lg transition-colors"
        >
          New Chat
        </button>
      </div>
      
      <div className="flex-1 overflow-y-auto p-2">
        {chats.map((chat) => (
          <div
            key={chat.id}
            onClick={() => onChatSelect(chat.id)}
            className={`p-3 rounded-lg cursor-pointer mb-2 transition-colors ${activeChat === chat.id
              ? 'bg-gray-100 text-primary'
              : 'hover:bg-gray-50'}`}
          >
            <div className="font-medium truncate">{chat.name}</div>
            {chat.messages.length > 0 && (
              <div className="text-sm text-gray-500 truncate">
                {chat.messages[chat.messages.length - 1].content.substring(0, 30)}...
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default Sidebar;