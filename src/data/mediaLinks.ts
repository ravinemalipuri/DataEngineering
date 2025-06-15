
export interface MediaLink {
  id: string;
  title: string;
  url: string;
  type: 'youtube' | 'article' | 'podcast';
}

export const defaultMediaLinks: MediaLink[] = [
  {
    id: '1',
    title: 'Understanding Emotions - Psychology Basics',
    url: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    type: 'youtube'
  },
  {
    id: '2', 
    title: 'Emotional Intelligence in Daily Life',
    url: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    type: 'youtube'
  },
  {
    id: '3',
    title: 'Managing Difficult Emotions',
    url: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ', 
    type: 'youtube'
  }
];

export const getYouTubeVideoId = (url: string): string | null => {
  const regex = /(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)/;
  const match = url.match(regex);
  return match ? match[1] : null;
};
