import React, { useState, useRef, useEffect } from 'react';
import { emotionsData, type Emotion } from '@/data/emotions';
import { getEmotionName, Language } from '@/translations';

interface EmotionWheelProps {
  language: string;
}

const EmotionWheel: React.FC<EmotionWheelProps> = ({ language }) => {
  const [selectedEmotion, setSelectedEmotion] = useState<Emotion | null>(null);
  const [hoveredEmotion, setHoveredEmotion] = useState<Emotion | null>(null);
  const svgRef = useRef<SVGSVGElement>(null);

  const emotions = emotionsData();
  const primaryEmotions = emotions.filter(e => e.intensity === 'primary');

  const renderEmotionSegment = (emotion: Emotion, index: number, total: number) => {
    const angle = (360 / total) * index;
    const nextAngle = (360 / total) * (index + 1);
    
    const isSelected = selectedEmotion?.id === emotion.id;
    const isHovered = hoveredEmotion?.id === emotion.id;
    
    return (
      <g key={emotion.id}>
        <path
          d={describeArc(200, 200, 60, 120, angle, nextAngle)}
          fill={emotion.color}
          stroke="#fff"
          strokeWidth="2"
          opacity={isSelected || isHovered ? 1 : 0.8}
          style={{ cursor: 'pointer' }}
          onMouseEnter={() => setHoveredEmotion(emotion)}
          onMouseLeave={() => setHoveredEmotion(null)}
          onClick={() => setSelectedEmotion(emotion)}
        />
        <text
          x={200 + Math.cos((angle + (nextAngle - angle) / 2) * Math.PI / 180) * 90}
          y={200 + Math.sin((angle + (nextAngle - angle) / 2) * Math.PI / 180) * 90}
          textAnchor="middle"
          dominantBaseline="middle"
          fill="#000"
          fontSize="12"
          fontWeight="bold"
          style={{ cursor: 'pointer' }}
          onMouseEnter={() => setHoveredEmotion(emotion)}
          onMouseLeave={() => setHoveredEmotion(null)}
          onClick={() => setSelectedEmotion(emotion)}
        >
          {getEmotionName(emotion, language as Language)}
        </text>
      </g>
    );
  };

  const describeArc = (x: number, y: number, innerRadius: number, outerRadius: number, startAngle: number, endAngle: number) => {
    const start = polarToCartesian(x, y, outerRadius, endAngle);
    const end = polarToCartesian(x, y, outerRadius, startAngle);
    const innerStart = polarToCartesian(x, y, innerRadius, endAngle);
    const innerEnd = polarToCartesian(x, y, innerRadius, startAngle);

    const largeArcFlag = endAngle - startAngle <= 180 ? "0" : "1";

    return [
      "M", start.x, start.y, 
      "A", outerRadius, outerRadius, 0, largeArcFlag, 0, end.x, end.y,
      "L", innerEnd.x, innerEnd.y,
      "A", innerRadius, innerRadius, 0, largeArcFlag, 1, innerStart.x, innerStart.y,
      "Z"
    ].join(" ");
  };

  const polarToCartesian = (centerX: number, centerY: number, radius: number, angleInDegrees: number) => {
    const angleInRadians = (angleInDegrees - 90) * Math.PI / 180.0;
    return {
      x: centerX + (radius * Math.cos(angleInRadians)),
      y: centerY + (radius * Math.sin(angleInRadians))
    };
  };

  return (
    <div className="flex flex-col items-center space-y-6">
      <div className="relative">
        <svg ref={svgRef} width="400" height="400" className="drop-shadow-lg">
          {primaryEmotions.map((emotion, index) => 
            renderEmotionSegment(emotion, index, primaryEmotions.length)
          )}
        </svg>
      </div>
      
      {(selectedEmotion || hoveredEmotion) && (
        <div className="bg-white rounded-lg p-4 shadow-lg border max-w-sm">
          <h3 className="font-semibold text-lg mb-2">
            {getEmotionName(selectedEmotion || hoveredEmotion!, language as Language)}
          </h3>
          <div className="flex items-center space-x-2">
            <div 
              className="w-4 h-4 rounded-full" 
              style={{ backgroundColor: (selectedEmotion || hoveredEmotion)?.color }}
            />
            <span className="text-sm text-gray-600 capitalize">
              {(selectedEmotion || hoveredEmotion)?.category} emotion
            </span>
          </div>
          {(selectedEmotion || hoveredEmotion)?.description && (
            <p className="text-sm text-gray-700 mt-2">
              {(selectedEmotion || hoveredEmotion)?.description}
            </p>
          )}
        </div>
      )}
    </div>
  );
};

export default EmotionWheel;
