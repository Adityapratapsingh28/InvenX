'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { Package, Truck, BarChart3, Globe, Cloud, Shield, Zap, Database } from 'lucide-react';

interface FloatingElementProps {
  icon: React.ElementType; // Use the icon component directly
  delay?: number;
  className?: string;
}

export const FloatingElement: React.FC<FloatingElementProps> = ({
  icon: Icon,
  delay = 0,
  className = '',
}) => {
  return (
    <motion.div
      className={`flex items-center justify-center ${className}`}
      initial={{ y: 0 }}
      animate={{
        y: [-10, 10, -10], // Smaller floating range for subtlety
        rotate: [0, 5, -5, 0], // Slight rotation
      }}
      transition={{
        duration: 4, // Slower animation
        repeat: Infinity,
        delay,
        ease: 'easeInOut',
      }}
    >
      <Icon className="w-8 h-8 text-blue-500/80" /> {/* Smaller icons for better alignment */}
    </motion.div>
  );
};