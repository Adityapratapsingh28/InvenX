'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { ArrowRight } from 'lucide-react';
import PixelTransition from './PixelTransition';
import { useRouter } from 'next/navigation';

interface FeatureCardProps {
  title: string;
  description: string;
  icon: React.ReactNode;
  link: string;
  imageUrl: string;
}

const FeatureCard = ({ title, description, icon, link, imageUrl }: FeatureCardProps) => {
  const router = useRouter();

  const handleLearnMore = (e: React.MouseEvent) => {
    e.preventDefault();
    router.push(link);
  };

  const firstContent = (
    <div className="relative h-full w-full">
      <img 
        src={imageUrl} 
        alt={title}
        className="w-full h-full object-cover"
      />
      <div className="absolute inset-0 bg-gradient-to-t from-black/80 to-black/20" />
      <div className="absolute inset-0 p-6">
        <div className="w-12 h-12 bg-white/90 rounded-lg flex items-center justify-center mb-4">
          {icon}
        </div>
        <h3 className="text-2xl font-bold text-white font-ibm-plex mb-2">{title}</h3>
      </div>
    </div>
  );

  const secondContent = (
    <div className="h-full w-full bg-black/90 p-6 flex flex-col justify-between">
      <div>
        <div className="w-12 h-12 bg-white/90 rounded-lg flex items-center justify-center mb-4">
          {icon}
        </div>
        <h3 className="text-2xl font-bold text-white font-ibm-plex mb-4">{title}</h3>
        <p className="text-white/90 font-ibm-plex">{description}</p>
      </div>
      <motion.button
        onClick={handleLearnMore}
        className="inline-flex items-center space-x-2 text-white font-ibm-plex hover:text-blue-400 transition-colors"
        whileHover={{ x: 5 }}
      >
        <span>Learn More</span>
        <ArrowRight className="w-4 h-4" />
      </motion.button>
    </div>
  );

  return (
    <motion.div 
      className="w-[300px] h-[400px]"
      whileHover={{ scale: 1.02 }}
      transition={{ duration: 0.2 }}
    >
      <PixelTransition
        firstContent={firstContent}
        secondContent={secondContent}
        gridSize={12}
        pixelColor="#ffffff"
        animationStepDuration={0.4}
        className="w-full h-full rounded-xl overflow-hidden shadow-lg"
      />
    </motion.div>
  );
};

export default FeatureCard; 