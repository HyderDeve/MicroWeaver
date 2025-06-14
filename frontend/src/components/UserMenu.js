import React, { useState } from 'react';

function UserMenu({ onOpenAuth }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  if (isAuthenticated) {
    return (
      <div className="relative">
        <button
          className="flex items-center space-x-2 text-gray-700 hover:text-gray-900"
          onClick={() => setIsAuthenticated(false)}
        >
          <div className="w-8 h-8 rounded-full bg-primary text-white flex items-center justify-center">
            <span className="text-sm font-medium">U</span>
          </div>
          <span className="hidden md:inline">Sign Out</span>
        </button>
      </div>
    );
  }

  return (
    <button
      onClick={() => onOpenAuth()}
      className="flex items-center space-x-2 text-gray-700 hover:text-gray-900"
    >
      <svg
        className="w-6 h-6"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
        />
      </svg>
      <span className="hidden md:inline">Sign In</span>
    </button>
  );
}

export default UserMenu;