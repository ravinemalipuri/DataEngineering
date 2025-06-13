
import React, { useRef, useEffect } from 'react';
import { defaultMediaLinks, getYouTubeVideoId } from '@/data/mediaLinks';
import { Youtube } from 'lucide-react';
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel";

const MediaBar: React.FC = () => {
  const iframeRefs = useRef<(HTMLIFrameElement | null)[]>([]);

  const pauseAllVideos = () => {
    iframeRefs.current.forEach((iframe) => {
      if (iframe && iframe.contentWindow) {
        iframe.contentWindow.postMessage('{"event":"command","func":"pauseVideo","args":""}', '*');
      }
    });
  };

  const handleIframeLoad = (index: number) => {
    const iframe = iframeRefs.current[index];
    if (iframe && iframe.contentWindow) {
      // Enable JS API for YouTube iframes
      iframe.addEventListener('load', () => {
        iframe.contentWindow?.postMessage('{"event":"listening"}', '*');
      });
    }
  };

  useEffect(() => {
    const handleMessage = (event: MessageEvent) => {
      if (event.origin !== 'https://www.youtube.com') return;
      
      try {
        const data = JSON.parse(event.data);
        if (data.event === 'video-progress' && data.info === 1) { // Playing state
          // Pause all other videos when one starts playing
          pauseAllVideos();
        }
      } catch (e) {
        // Ignore parsing errors
      }
    };

    window.addEventListener('message', handleMessage);
    return () => window.removeEventListener('message', handleMessage);
  }, []);

  const renderYouTubeEmbed = (url: string, title: string, index: number) => {
    const videoId = getYouTubeVideoId(url);
    if (!videoId) return null;

    return (
      <div className="flex-1 min-w-0">
        <div className="aspect-video bg-black rounded-lg overflow-hidden">
          <iframe
            ref={(el) => (iframeRefs.current[index] = el)}
            src={`https://www.youtube.com/embed/${videoId}?enablejsapi=1&origin=${window.location.origin}`}
            title={title}
            className="w-full h-full"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
            onLoad={() => handleIframeLoad(index)}
            onClick={pauseAllVideos}
          ></iframe>
        </div>
        <p className="text-sm text-muted-foreground mt-2 text-center truncate">{title}</p>
      </div>
    );
  };

  return (
    <div className="bg-card border-t border-border py-8 mt-8">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-center mb-6">
          <Youtube className="w-6 h-6 text-red-500 mr-2" />
          <h3 className="text-xl font-playfair font-semibold">Related Videos</h3>
        </div>
        
        <div className="max-w-6xl mx-auto">
          <Carousel className="w-full">
            <CarouselContent className="-ml-2 md:-ml-4">
              {defaultMediaLinks.map((link, index) => (
                <CarouselItem key={link.id} className="pl-2 md:pl-4 md:basis-1/3">
                  {renderYouTubeEmbed(link.url, link.title, index)}
                </CarouselItem>
              ))}
            </CarouselContent>
            <CarouselPrevious className="hidden md:flex" />
            <CarouselNext className="hidden md:flex" />
          </Carousel>
        </div>
      </div>
    </div>
  );
};

export default MediaBar;
