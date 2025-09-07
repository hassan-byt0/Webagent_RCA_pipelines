export interface PostType {
  id: number;
  author: string;
  content: string;
  avatar: string;
  image?: string;
  companyId?: string;
  width?: number;
  height?: number;
  sponsored?: boolean;
}
