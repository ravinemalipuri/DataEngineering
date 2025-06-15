
import React from 'react';
import { defaultMediaLinks, getYouTubeVideoId } from '@/data/mediaLinks';
import { Youtube } from 'lucide-react';

const MediaBar: React.FC = () => {
  const renderYouTubeEmbed = (url: string, title: string) => {
    const videoId = getYouTubeVideoId(url);
    if (!videoId) return null;

    return (
      <div className="flex-1 min-w-0">
        <div className="aspect-video bg-black rounded-lg overflow-hidden">
          <iframe
            src={`https://www.youtube.com/embed/${videoId}`}
            title={title}
            className="w-full h-full"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
          ></iframe>
        </div>
        <p className="text-sm text-muted-foreground mt-2 text-center truncate">{title}</p>
      </div>
    );
  };

  return (
    <div className="bg-card border-t border-border py-8 mt-16">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-center mb-6">
          <Youtube className="w-6 h-6 text-red-500 mr-2" />
          <h3 className="text-xl font-playfair font-semibold">Related Videos</h3>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-6xl mx-auto">
          {defaultMediaLinks.map((link) => (
            <div key={link.id}>
              {renderYouTubeEmbed(link.url, link.title)}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default MediaBar;
