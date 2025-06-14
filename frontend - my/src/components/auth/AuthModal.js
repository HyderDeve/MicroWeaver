import React, { useState } from 'react';
import SignIn from './SignIn';
import SignUp from './SignUp';

function AuthModal({ isOpen, onClose }) {
  const [authMode, setAuthMode] = useState('signin'); // 'signin' or 'signup'

  if (!isOpen) return null;

  const handleToggleAuth = (mode) => {
    setAuthMode(mode);
  };

  return (
    <div className="z-50">
      {authMode === 'signin' ? (
        <SignIn onToggleAuth={handleToggleAuth} />
      ) : (
        <SignUp onToggleAuth={handleToggleAuth} />
      )}
    </div>
  );
}

export default AuthModal;