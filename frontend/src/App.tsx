import React from 'react';
import { motion } from 'framer-motion';
import { BlurText } from './components/BlurText';
import { FloatingElement } from './components/FloatingElement';
import { Navbar } from './components/Navbar';

function App() {
  return (
    <div className="min-h-screen bg-white font-inter">
      <Navbar />
      
      <main className="relative pt-32 pb-16 overflow-hidden">
        {/* Hero Section */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="relative">
            {/* Floating Elements */}
            <FloatingElement type="truck" className="top-0 right-[20%]" delay={0} />
            <FloatingElement type="box" className="top-40 left-[15%]" delay={1} />
            <FloatingElement type="graph" className="bottom-0 right-[30%]" delay={2} />
            
            {/* Main Content */}
            <div className="text-center max-w-4xl mx-auto">
              <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
                <BlurText 
                  text="Optimize with InvenX"
                  delay={150}
                  direction="top"
                />
              </h1>
              
              <p className="text-xl text-gray-600 mb-8">
                Transform your inventory management with cutting-edge AI technology.
                Streamline operations, reduce costs, and boost efficiency.
              </p>
              
              <motion.button
                className="bg-blue-600 text-white text-lg px-8 py-4 rounded-lg shadow-lg hover:bg-blue-700 transition-colors"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                Get Started
              </motion.button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;