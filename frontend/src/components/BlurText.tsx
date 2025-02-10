'use client';

import React, { useEffect, useRef } from 'react';

interface BlurTextProps {
  text: string;
  delay?: number;
  direction?: 'top' | 'bottom';
}

export const BlurText: React.FC<BlurTextProps> = ({
  text,
  delay = 150,
  direction = 'top',
}) => {
  const words = text.split(' ');
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const spans = containerRef.current?.querySelectorAll('span');
    if (!spans) return;

    spans.forEach((span, index) => {
      span.style.animation = `blurReveal 1.8s ease-out ${index * delay}ms forwards`;
      span.style.opacity = '0';
      span.style.filter = 'blur(10px)';
      span.style.transform = `translateY(${direction === 'top' ? '20px' : '-20px'})`;
    });
  }, [delay, direction]);

  return (
    <div ref={containerRef} className="inline">
      {words.map((word, index) => (
        <span
          key={index}
          className="inline-block transition-all duration-800"
          style={{ willChange: 'transform, opacity, filter' }}
        >
          {word}{' '}
        </span>
      ))}
    </div>
  );
};