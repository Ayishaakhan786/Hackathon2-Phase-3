'use client';

import { ReactNode } from 'react';
import ChatBot from '@/app/components/chatbot';

interface ClientWrapperProps {
  children: ReactNode;
}

const ClientWrapper = ({ children }: ClientWrapperProps) => {
  return (
    <>
      {children}
      <ChatBot />
    </>
  );
};

export default ClientWrapper;