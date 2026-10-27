import React from 'react';
import { motion } from 'framer-motion';

interface ConfidenceRingProps {
  percentage: number;
  size?: number;
  strokeWidth?: number;
}

export const ConfidenceRing: React.FC<ConfidenceRingProps> = ({
  percentage,
  size = 120,
  strokeWidth = 10,
}) => {
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const clampedPct = Math.min(Math.max(percentage, 0), 100);
  const strokeDashoffset = circumference - (clampedPct / 100) * circumference;

  // Color mapping: Green >= 70%, Amber 40-70%, Red < 40%
  let strokeColor = '#52B788'; // Leaf Green
  let glowColor = 'rgba(82, 183, 136, 0.4)';
  let labelColor = 'text-[#52B788]';

  if (clampedPct < 40) {
    strokeColor = '#EF4444'; // Red
    glowColor = 'rgba(239, 68, 68, 0.4)';
    labelColor = 'text-red-400';
  } else if (clampedPct < 70) {
    strokeColor = '#F59E0B'; // Amber
    glowColor = 'rgba(245, 158, 11, 0.4)';
    labelColor = 'text-amber-400';
  }

  return (
    <div className="relative inline-flex items-center justify-center" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="transform -rotate-90">
        {/* Track circle */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="rgba(255, 255, 255, 0.08)"
          strokeWidth={strokeWidth}
          fill="transparent"
        />
        {/* Animated Progress circle */}
        <motion.circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke={strokeColor}
          strokeWidth={strokeWidth}
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset }}
          transition={{ duration: 1.2, ease: 'easeOut' }}
          strokeLinecap="round"
          fill="transparent"
          style={{
            filter: `drop-shadow(0 0 8px ${glowColor})`,
          }}
        />
      </svg>
      {/* Center Percentage Display */}
      <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
        <motion.span
          className={`font-heading font-extrabold text-2xl tracking-tight ${labelColor}`}
          initial={{ opacity: 0, scale: 0.5 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: 0.3 }}
        >
          {percentage.toFixed(1)}%
        </motion.span>
        <span className="text-[10px] uppercase font-bold tracking-wider text-slate-400">Confidence</span>
      </div>
    </div>
  );
};
