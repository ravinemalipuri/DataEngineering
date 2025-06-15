
import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Heart } from 'lucide-react';

interface EmotionWheelProps {
  language: string;
}

const EmotionWheel: React.FC<EmotionWheelProps> = ({ language }) => {
  const [selectedEmotion, setSelectedEmotion] = useState<string | null>(null);

  const emotions = [
    { name: 'Joy', color: '#FFD700', angle: 0 },
    { name: 'Trust', color: '#90EE90', angle: 45 },
    { name: 'Fear', color: '#8B4513', angle: 90 },
    { name: 'Surprise', color: '#FFA500', angle: 135 },
    { name: 'Sadness', color: '#4169E1', angle: 180 },
    { name: 'Disgust', color: '#9ACD32', angle: 225 },
    { name: 'Anger', color: '#DC143C', angle: 270 },
    { name: 'Anticipation', color: '#FF6347', angle: 315 }
  ];

  return (
    <div className="flex flex-col items-center space-y-6">
      <div className="relative w-80 h-80">
        <svg viewBox="0 0 400 400" className="w-full h-full">
          {emotions.map((emotion, index) => {
            const isSelected = selectedEmotion === emotion.name;
            const radius = isSelected ? 180 : 160;
            const centerX = 200;
            const centerY = 200;
            
            const startAngle = (emotion.angle - 22.5) * (Math.PI / 180);
            const endAngle = (emotion.angle + 22.5) * (Math.PI / 180);
            
            const x1 = centerX + Math.cos(startAngle) * 60;
            const y1 = centerY + Math.sin(startAngle) * 60;
            const x2 = centerX + Math.cos(endAngle) * 60;
            const y2 = centerY + Math.sin(endAngle) * 60;
            const x3 = centerX + Math.cos(endAngle) * radius;
            const y3 = centerY + Math.sin(endAngle) * radius;
            const x4 = centerX + Math.cos(startAngle) * radius;
            const y4 = centerY + Math.sin(startAngle) * radius;
            
            const largeArcFlag = 0;
            
            return (
              <g key={emotion.name}>
                <path
                  d={`M ${x1} ${y1} A 60 60 0 ${largeArcFlag} 1 ${x2} ${y2} L ${x3} ${y3} A ${radius} ${radius} 0 ${largeArcFlag} 0 ${x4} ${y4} Z`}
                  fill={emotion.color}
                  stroke="#fff"
                  strokeWidth="2"
                  className="cursor-pointer hover:opacity-80 transition-opacity"
                  onClick={() => setSelectedEmotion(selectedEmotion === emotion.name ? null : emotion.name)}
                />
                <text
                  x={centerX + Math.cos(emotion.angle * (Math.PI / 180)) * 110}
                  y={centerY + Math.sin(emotion.angle * (Math.PI / 180)) * 110}
                  textAnchor="middle"
                  dominantBaseline="middle"
                  className="text-sm font-medium fill-gray-800 pointer-events-none"
                >
                  {emotion.name}
                </text>
              </g>
            );
          })}
          
          <circle
            cx="200"
            cy="200"
            r="50"
            fill="white"
            stroke="#ccc"
            strokeWidth="2"
          />
          <Heart className="w-6 h-6" x="188" y="188" />
        </svg>
      </div>
      
      {selectedEmotion && (
        <div className="bg-card border border-border rounded-lg p-4 max-w-md">
          <h3 className="font-semibold text-lg mb-2">{selectedEmotion}</h3>
          <p className="text-muted-foreground">
            You've selected {selectedEmotion}. Take a moment to explore this emotion and consider what might be causing you to feel this way.
          </p>
        </div>
      )}
    </div>
  );
};

export default EmotionWheel;
