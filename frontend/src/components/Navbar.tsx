'use client';

import React from 'react';
import Link from 'next/link';
import { Box } from 'lucide-react';

export const Navbar: React.FC = () => {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="bg-gradient-to-r from-white/90 to-white/80 backdrop-blur-lg rounded-t-lg px-6 py-3 flex justify-between items-center border-b border-gray-200 shadow-sm">
          <div className="flex items-center space-x-2">
            <Box className="w-6 h-6 text-gray-800" />
            <span className="text-lg font-semibold text-gray-800 font-ibm-plex">InvenX</span>
          </div>
          <div className="flex items-center space-x-8">
            <Link 
              href="#pricing" 
              className="text-gray-600 hover:text-gray-800 transition-colors duration-200 text-sm font-medium font-ibm-plex"
            >
              Pricing
            </Link>
            <Link 
              href="#labs" 
              className="text-gray-600 hover:text-gray-800 transition-colors duration-200 text-sm font-medium font-ibm-plex"
            >
              Labs
            </Link>
            <button 
              className="text-gray-800 hover:text-gray-600 transition-colors duration-200 text-sm font-medium font-ibm-plex px-4 py-2 rounded-md hover:bg-gray-100"
            >
              Log In
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};