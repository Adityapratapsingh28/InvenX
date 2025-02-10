"use client";

import React, { useRef, useEffect, useState } from "react";
import { gsap } from "gsap";

interface PixelTransitionProps {
  firstContent: React.ReactNode;
  secondContent: React.ReactNode;
  gridSize?: number;
  pixelColor?: string;
  animationStepDuration?: number;
  className?: string;
}

const PixelTransition: React.FC<PixelTransitionProps> = ({
  firstContent,
  secondContent,
  gridSize = 12,
  pixelColor = '#ffffff',
  animationStepDuration = 0.4,
  className = "",
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const pixelGridRef = useRef<HTMLDivElement>(null);
  const activeRef = useRef<HTMLDivElement>(null);
  const [isActive, setIsActive] = useState(false);

  useEffect(() => {
    const pixelGridEl = pixelGridRef.current;
    if (!pixelGridEl) return;

    pixelGridEl.innerHTML = "";

    for (let row = 0; row < gridSize; row++) {
      for (let col = 0; col < gridSize; col++) {
        const pixel = document.createElement("div");
        pixel.classList.add("pixel-transition");
        pixel.style.width = `${100 / gridSize}%`;
        pixel.style.height = `${100 / gridSize}%`;
        pixel.style.position = 'absolute';
        pixel.style.left = `${(col * 100) / gridSize}%`;
        pixel.style.top = `${(row * 100) / gridSize}%`;
        pixel.style.backgroundColor = pixelColor;
        pixel.style.opacity = '0';
        pixel.style.pointerEvents = 'none';
        pixelGridEl.appendChild(pixel);
      }
    }
  }, [gridSize, pixelColor]);

  const animatePixels = (activate: boolean) => {
    setIsActive(activate);
    const pixelGridEl = pixelGridRef.current;
    const activeEl = activeRef.current;
    if (!pixelGridEl || !activeEl) return;

    const pixels = Array.from(pixelGridEl.children) as HTMLElement[];
    
    gsap.killTweensOf([pixels, activeEl]);
    
    const shuffledPixels = [...pixels].sort(() => Math.random() - 0.5);

    if (activate) {
      // Show second content first but invisible
      gsap.set(activeEl, { 
        display: 'block',
        opacity: 0,
      });

      // Animate pixels
      gsap.to(shuffledPixels, {
        opacity: 1,
        duration: animationStepDuration / 2,
        stagger: {
          each: animationStepDuration / pixels.length,
          from: "random",
        },
        onComplete: () => {
          // Fade in the content
          gsap.to(activeEl, {
            opacity: 1,
            duration: 0.3,
          });
          // Fade out pixels
          gsap.to(shuffledPixels, {
            opacity: 0,
            duration: 0.3,
          });
        }
      });
    } else {
      // Fade out content
      gsap.to(activeEl, {
        opacity: 0,
        duration: 0.3,
        onComplete: () => {
          gsap.set(activeEl, { display: 'none' });
        }
      });

      // Animate pixels out
      gsap.to(shuffledPixels, {
        opacity: 0,
        duration: animationStepDuration / 2,
        stagger: {
          each: animationStepDuration / pixels.length,
          from: "random",
        }
      });
    }
  };

  return (
    <div
      ref={containerRef}
      className={`relative overflow-hidden ${className}`}
      onMouseEnter={() => !isActive && animatePixels(true)}
      onMouseLeave={() => isActive && animatePixels(false)}
    >
      <div className="relative w-full h-full">
        {firstContent}
      </div>

      <div
        ref={activeRef}
        className="absolute inset-0 w-full h-full transition-opacity duration-300"
        style={{ display: 'none' }}
      >
        {secondContent}
      </div>

      <div
        ref={pixelGridRef}
        className="absolute inset-0 w-full h-full pointer-events-none z-10"
      />
    </div>
  );
};

export default PixelTransition;