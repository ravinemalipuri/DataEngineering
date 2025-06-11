
export interface MediaLink {
  id: string;
  title: string;
  url: string;
  type: 'youtube' | 'facebook' | 'instagram';
  thumbnail?: string;
}

export const defaultMediaLinks: MediaLink[] = [
  {
    id: '1',
    title: 'Emotional Intelligence Video 1',
    url: 'https://www.youtube.com/watch?v=SYzqO5xxFl8',
    type: 'youtube'
  },
  {
    id: '2', 
    title: 'Understanding Emotions Video 2',
    url: 'https://www.youtube.com/watch?v=AagqaAQebKk',
    type: 'youtube'
  },
  {
    id: '3',
    title: 'Emotion Wheel Guide Video 3', 
    url: 'https://www.youtube.com/watch?v=skZagPiKQfQ',
    type: 'youtube'
  }
];

// Helper function to extract YouTube video ID from URL
export const getYouTubeVideoId = (url: string): string | null => {
  const regex = /(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})/;
  const match = url.match(regex);
  return match ? match[1] : null;
};
