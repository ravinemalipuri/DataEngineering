
import React from 'react';
import { defaultMediaLinks, getYouTubeVideoId } from '@/data/mediaLinks';
import { Button } from '@/components/ui/button';
import { ExternalLink } from 'lucide-react';

const MediaBar: React.FC = () => {
  return (
    <div className="mt-12 bg-card rounded-xl p-6 border border-border">
      <h3 className="text-xl font-semibold mb-4 text-center">
        Learn More About Emotions
      </h3>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {defaultMediaLinks.map((link) => (
          <Button
            key={link.id}
            variant="outline"
            className="h-auto p-4 flex flex-col items-center space-y-2"
            onClick={() => window.open(link.url, '_blank')}
          >
            <ExternalLink className="w-5 h-5" />
            <span className="text-sm text-center">{link.title}</span>
          </Button>
        ))}
      </div>
    </div>
  );
};

export default MediaBar;
