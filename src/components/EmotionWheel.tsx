import React, { useState } from 'react';
import { getEmotionsData, getAllLevel2Emotions, getAllLevel3Emotions, EmotionLevel1, EmotionLevel2, EmotionLevel3, getEmotionName as getEmotionNameFromData } from '@/data/emotions';
import { getEmotionName } from '@/translations';
import { Language } from '@/translations';

interface EmotionWheelProps {
  language: string;
}

const EmotionWheel: React.FC<EmotionWheelProps> = ({ language }) => {
  const [selectedEmotion, setSelectedEmotion] = useState<EmotionLevel1 | null>(null);
  const [hoveredEmotion, setHoveredEmotion] = useState<string | null>(null);
  
  // Get emotions data based on current language
  const emotionsData = getEmotionsData(language as Language);
  
  // Larger wheel dimensions
  const svgSize = 1200;
  const centerX = svgSize / 2;
  const centerY = svgSize / 2;
  const innerRadius = svgSize * 0.07; // Center circle
  const level1InnerRadius = innerRadius;
  const level1OuterRadius = svgSize * 0.15;
  const level2InnerRadius = level1OuterRadius;
  const level2OuterRadius = svgSize * 0.23;
  const level3InnerRadius = level2OuterRadius;
  const level3OuterRadius = svgSize * 0.32;

  // Helper function to get appropriate font size based on language
  const getFontSize = (text: string, baseSize: number, level: number = 1) => {
    const isTeluguOrTamil = language === 'te' || language === 'ta';
    let multiplier = 1;
    
    if (isTeluguOrTamil) {
      // Reduce font size for Telugu/Tamil based on level
      if (level === 1) multiplier = 0.7; // Level 1 (primary emotions)
      else if (level === 2) multiplier = 0.6; // Level 2 (secondary emotions)
      else multiplier = 0.5; // Level 3 (tertiary emotions)
    }
    
    return Math.min(baseSize * multiplier, Math.max(baseSize * multiplier * 0.5, (baseSize * multiplier * 400) / text.length));
  };

  // Helper function to get emotion name - use data-based function for better performance
  const getEmotionDisplayName = (emotion: any): string => {
    return getEmotionNameFromData(emotion, language as Language);
  };

  const createLevel1Segment = (emotion: EmotionLevel1, index: number, total: number) => {
    const numPrimary = total;
    const segmentAngle = 360 / numPrimary;
    const startAngle = index * segmentAngle;
    const endAngle = (index + 1) * segmentAngle;
    
    const startAngleRad = (startAngle * Math.PI) / 180;
    const endAngleRad = (endAngle * Math.PI) / 180;
    
    const x1 = centerX + level1InnerRadius * Math.cos(startAngleRad);
    const y1 = centerY + level1InnerRadius * Math.sin(startAngleRad);
    const x2 = centerX + level1OuterRadius * Math.cos(startAngleRad);
    const y2 = centerY + level1OuterRadius * Math.sin(startAngleRad);
    
    const x3 = centerX + level1OuterRadius * Math.cos(endAngleRad);
    const y3 = centerY + level1OuterRadius * Math.sin(endAngleRad);
    const x4 = centerX + level1InnerRadius * Math.cos(endAngleRad);
    const y4 = centerY + level1InnerRadius * Math.sin(endAngleRad);
    
    const largeArcFlag = segmentAngle > 180 ? 1 : 0;
    
    const pathData = [
      `M ${x1} ${y1}`,
      `L ${x2} ${y2}`,
      `A ${level1OuterRadius} ${level1OuterRadius} 0 ${largeArcFlag} 1 ${x3} ${y3}`,
      `L ${x4} ${y4}`,
      `A ${level1InnerRadius} ${level1InnerRadius} 0 ${largeArcFlag} 0 ${x1} ${y1}`,
      'Z'
    ].join(' ');

    const isHovered = hoveredEmotion === emotion.id;
    const isSelected = selectedEmotion?.id === emotion.id;
    
    const textRadius = (level1InnerRadius + level1OuterRadius) / 2;
    const textAngle = startAngle + (segmentAngle / 2);
    const textAngleRad = (textAngle * Math.PI) / 180;
    const textX = centerX + textRadius * Math.cos(textAngleRad);
    const textY = centerY + textRadius * Math.sin(textAngleRad);
    
    let textRotation = textAngle;
    if (textAngle > 90 && textAngle < 270) {
      textRotation = textAngle + 180;
    }
    
    const emotionName = getEmotionDisplayName(emotion);
    const fontSize = getFontSize(emotionName, 22, 1);
    
    return (
      <g key={emotion.id} className="emotion-segment">
        <path
          d={pathData}
          fill={emotion.color}
          fillOpacity={0.9 + (isHovered ? 0.1 : 0)}
          stroke="white"
          strokeWidth="2"
          className={`transition-all duration-300 cursor-pointer ${isSelected ? 'drop-shadow-lg' : ''}`}
          onMouseEnter={() => setHoveredEmotion(emotion.id)}
          onMouseLeave={() => setHoveredEmotion(null)}
          onClick={() => setSelectedEmotion(selectedEmotion?.id === emotion.id ? null : emotion)}
        />
        <text
          x={textX}
          y={textY}
          textAnchor="middle"
          dominantBaseline="middle"
          fill="black"
          fontSize={fontSize}
          fontWeight="700"
          className="pointer-events-none font-inter"
          style={{ 
            textShadow: '1px 1px 2px rgba(255,255,255,0.9), -1px -1px 2px rgba(255,255,255,0.9), 1px -1px 2px rgba(255,255,255,0.9), -1px 1px 2px rgba(255,255,255,0.9)' 
          }}
          transform={`rotate(${textRotation} ${textX} ${textY})`}
        >
          {emotionName}
        </text>
      </g>
    );
  };

  const createLevel2Segments = (primaryEmotion: EmotionLevel1, primaryIndex: number, totalPrimary: number) => {
    const primarySegmentAngle = 360 / totalPrimary;
    const primaryStartAngle = primaryIndex * primarySegmentAngle;
    
    const level2Emotions = primaryEmotion.level2Emotions;
    const numLevel2 = level2Emotions.length;
    const level2SegmentAngle = primarySegmentAngle / numLevel2;
    
    return level2Emotions.map((emotion, index) => {
      const startAngle = primaryStartAngle + (index * level2SegmentAngle);
      const endAngle = primaryStartAngle + ((index + 1) * level2SegmentAngle);
      
      const startAngleRad = (startAngle * Math.PI) / 180;
      const endAngleRad = (endAngle * Math.PI) / 180;
      
      const x1 = centerX + level2InnerRadius * Math.cos(startAngleRad);
      const y1 = centerY + level2InnerRadius * Math.sin(startAngleRad);
      const x2 = centerX + level2OuterRadius * Math.cos(startAngleRad);
      const y2 = centerY + level2OuterRadius * Math.sin(startAngleRad);
      
      const x3 = centerX + level2OuterRadius * Math.cos(endAngleRad);
      const y3 = centerY + level2OuterRadius * Math.sin(endAngleRad);
      const x4 = centerX + level2InnerRadius * Math.cos(endAngleRad);
      const y4 = centerY + level2InnerRadius * Math.sin(endAngleRad);
      
      const largeArcFlag = level2SegmentAngle > 180 ? 1 : 0;
      
      const pathData = [
        `M ${x1} ${y1}`,
        `L ${x2} ${y2}`,
        `A ${level2OuterRadius} ${level2OuterRadius} 0 ${largeArcFlag} 1 ${x3} ${y3}`,
        `L ${x4} ${y4}`,
        `A ${level2InnerRadius} ${level2InnerRadius} 0 ${largeArcFlag} 0 ${x1} ${y1}`,
        'Z'
      ].join(' ');

      const textRadius = (level2InnerRadius + level2OuterRadius) / 2;
      const textAngle = startAngle + (level2SegmentAngle / 2);
      const textAngleRad = (textAngle * Math.PI) / 180;
      const textX = centerX + textRadius * Math.cos(textAngleRad);
      const textY = centerY + textRadius * Math.sin(textAngleRad);
      
      let textRotation = textAngle;
      if (textAngle > 90 && textAngle < 270) {
        textRotation = textAngle + 180;
      }

      const emotionName = getEmotionDisplayName(emotion);
      const fontSize = getFontSize(emotionName, 18, 2);
      
      return (
        <g key={`${primaryEmotion.id}-${emotion.id}`} className="emotion-segment">
          <path
            d={pathData}
            fill={primaryEmotion.color}
            fillOpacity={0.7}
            stroke="white"
            strokeWidth="1.5"
            className="cursor-pointer"
          />
          <text
            x={textX}
            y={textY}
            textAnchor="middle"
            dominantBaseline="middle"
            fill="black"
            fontSize={fontSize}
            fontWeight="600"
            className="pointer-events-none font-inter"
            style={{ 
              textShadow: '1px 1px 2px rgba(255,255,255,0.9), -1px -1px 2px rgba(255,255,255,0.9), 1px -1px 2px rgba(255,255,255,0.9), -1px 1px 2px rgba(255,255,255,0.9)' 
            }}
            transform={`rotate(${textRotation} ${textX} ${textY})`}
          >
            {emotionName}
          </text>
        </g>
      );
    });
  };

  const createLevel3Segments = (primaryEmotion: EmotionLevel1, primaryIndex: number, totalPrimary: number) => {
    const primarySegmentAngle = 360 / totalPrimary;
    const primaryStartAngle = primaryIndex * primarySegmentAngle;
    
    const level2Emotions = primaryEmotion.level2Emotions;
    const numLevel2 = level2Emotions.length;
    const level2SegmentAngle = primarySegmentAngle / numLevel2;
    
    const allLevel3Segments: JSX.Element[] = [];
    
    level2Emotions.forEach((level2Emotion, level2Index) => {
      const level2StartAngle = primaryStartAngle + (level2Index * level2SegmentAngle);
      const level3Emotions = level2Emotion.level3Emotions;
      const numLevel3 = level3Emotions.length;
      const level3SegmentAngle = level2SegmentAngle / numLevel3;
      
      level3Emotions.forEach((emotion, level3Index) => {
        const startAngle = level2StartAngle + (level3Index * level3SegmentAngle);
        const endAngle = level2StartAngle + ((level3Index + 1) * level3SegmentAngle);
        
        const startAngleRad = (startAngle * Math.PI) / 180;
        const endAngleRad = (endAngle * Math.PI) / 180;
        
        const x1 = centerX + level3InnerRadius * Math.cos(startAngleRad);
        const y1 = centerY + level3InnerRadius * Math.sin(startAngleRad);
        const x2 = centerX + level3OuterRadius * Math.cos(startAngleRad);
        const y2 = centerY + level3OuterRadius * Math.sin(startAngleRad);
        
        const x3 = centerX + level3OuterRadius * Math.cos(endAngleRad);
        const y3 = centerY + level3OuterRadius * Math.sin(endAngleRad);
        const x4 = centerX + level3InnerRadius * Math.cos(endAngleRad);
        const y4 = centerY + level3InnerRadius * Math.sin(endAngleRad);
        
        const largeArcFlag = level3SegmentAngle > 180 ? 1 : 0;
        
        const pathData = [
          `M ${x1} ${y1}`,
          `L ${x2} ${y2}`,
          `A ${level3OuterRadius} ${level3OuterRadius} 0 ${largeArcFlag} 1 ${x3} ${y3}`,
          `L ${x4} ${y4}`,
          `A ${level3InnerRadius} ${level3InnerRadius} 0 ${largeArcFlag} 0 ${x1} ${y1}`,
          'Z'
        ].join(' ');

        const textRadius = (level3InnerRadius + level3OuterRadius) / 2;
        const textAngle = startAngle + (level3SegmentAngle / 2);
        const textAngleRad = (textAngle * Math.PI) / 180;
        const textX = centerX + textRadius * Math.cos(textAngleRad);
        const textY = centerY + textRadius * Math.sin(textAngleRad);
        
        let textRotation = textAngle;
        if (textAngle > 90 && textAngle < 270) {
          textRotation = textAngle + 180;
        }

        const emotionName = getEmotionDisplayName(emotion);
        const fontSize = getFontSize(emotionName, 14, 3);
        
        allLevel3Segments.push(
          <g key={`${primaryEmotion.id}-${level2Emotion.id}-${emotion.id}`} className="emotion-segment">
            <path
              d={pathData}
              fill={primaryEmotion.color}
              fillOpacity={0.4}
              stroke="white"
              strokeWidth="1"
              className="cursor-pointer"
            />
            <text
              x={textX}
              y={textY}
              textAnchor="middle"
              dominantBaseline="middle"
              fill="black"
              fontSize={fontSize}
              fontWeight="500"
              className="pointer-events-none font-inter"
              style={{ 
                textShadow: '1px 1px 2px rgba(255,255,255,0.9), -1px -1px 2px rgba(255,255,255,0.9), 1px -1px 2px rgba(255,255,255,0.9), -1px 1px 2px rgba(255,255,255,0.9)' 
              }}
              transform={`rotate(${textRotation} ${textX} ${textY})`}
            >
              {emotionName}
            </text>
          </g>
        );
      });
    });
    
    return allLevel3Segments;
  };

  return (
    <div className="flex flex-col items-center space-y-8">
      <div className="relative">
        <svg width={svgSize} height={svgSize} viewBox={`0 0 ${svgSize} ${svgSize}`} className="w-full max-w-6xl">
          {/* Level 3 segments (outermost) */}
          {emotionsData.map((emotion, index) => createLevel3Segments(emotion, index, emotionsData.length))}
          
          {/* Level 2 segments (middle) */}
          {emotionsData.map((emotion, index) => createLevel2Segments(emotion, index, emotionsData.length))}
          
          {/* Level 1 segments (innermost) */}
          {emotionsData.map((emotion, index) => createLevel1Segment(emotion, index, emotionsData.length))}
          
          {/* Center circle */}
          <circle
            cx={centerX}
            cy={centerY}
            r={innerRadius}
            fill="url(#centerGradient)"
            stroke="white"
            strokeWidth="3"
          />
          
          <defs>
            <radialGradient id="centerGradient" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stopColor="#ffffff" stopOpacity="0.9" />
              <stop offset="100%" stopColor="#f0f0f0" stopOpacity="0.8" />
            </radialGradient>
          </defs>
          
          <text
            x={centerX}
            y={centerY}
            textAnchor="middle"
            dominantBaseline="middle"
            fill="#333"
            fontSize="24"
            fontWeight="700"
            className="font-playfair"
          >
            {getTranslation('main.emotions', language as Language)}
          </text>
        </svg>
      </div>

      {/* Emotion Details */}
      {selectedEmotion && (
        <div className="bg-card border border-border rounded-lg p-6 w-full max-w-md mx-auto animate-fade-in">
          <h3 className="text-xl font-playfair font-semibold mb-4 text-center">
            {getEmotionDisplayName(selectedEmotion)}
          </h3>
          
          <div className="space-y-3">
            <div>
              <h4 className="font-semibold text-sm text-muted-foreground mb-2">
                {language === 'en' ? 'Secondary Emotions:' : language === 'te' ? 'ద్వితీయ భావనలు:' : 
                 language === 'es' ? 'Emociones Secundarias:' : 'இரண்டாம் நிலை உணர்ச்சிகள்:'}
              </h4>
              <div className="grid grid-cols-2 gap-1 text-sm">
                {getAllLevel2Emotions(selectedEmotion).map((emotion) => (
                  <span key={emotion.id} className="text-xs bg-accent/20 rounded px-2 py-1">
                    {getEmotionDisplayName(emotion)}
                  </span>
                ))}
              </div>
            </div>
            
            <div>
              <h4 className="font-semibold text-sm text-muted-foreground mb-2">
                {language === 'en' ? 'Detailed Emotions:' : language === 'te' ? 'వివరణాత్మక భావనలు:' : 
                 language === 'es' ? 'Emociones Detalladas:' : 'விரிவான உணர்ச்சிகள்:'}
              </h4>
              <div className="grid grid-cols-2 gap-1 text-sm">
                {getAllLevel3Emotions(selectedEmotion).map((emotion) => (
                  <span key={emotion.id} className="text-xs bg-primary/10 rounded px-2 py-1">
                    {getEmotionDisplayName(emotion)}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
      
      <p className="text-sm text-muted-foreground text-center max-w-md">
        {getTranslation('main.clickExplore', language as Language)}
      </p>
    </div>
  );
};

export default EmotionWheel;
