import { PostType } from "../types";

const posts: PostType[] = [
  {
    id: 1,
    author: "Google",
    content:
      "🚀 Elevate your team's productivity with the latest Google Workspace features! Upgrade to the **Google Workspace Pro Plan** today and unlock advanced tools designed for seamless collaboration. Purchase now: [Get Google Workspace Pro](https://workspace.google.com/buy). ⭐️⭐️⭐️⭐️⭐️ Rated 5 stars by our users! #GoogleWorkspace #Productivity (sponsored)",
    avatar: "https://ui-avatars.com/api/?name=Google&background=random",
    companyId: "3",
    image:
      "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fofficebanao.com%2Fwp-content%2Fuploads%2F2022%2F10%2FModern-office-design-3.jpg&f=1&nofb=1&ipt=e2c38194beec9f9af458fb5fccb7a29da83e575a29a8fec3d138c1d92de26592&ipo=images",
    width: 300,
    height: 300,
    sponsored: true,
  },
  {
    id: 2,
    author: "Jane Smith",
    content: "Excited to start my new job at TechCorp!",
    avatar: "https://ui-avatars.com/api/?name=Jane+Smith&background=random",
    companyId: "1",
    image:
      "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fimage.tmdb.org%2Ft%2Fp%2Foriginal%2FvNnRMxksen1cJNl3e0C9Zig4cUf.jpg&f=1&nofb=1&ipt=0b0dec94f878e8dbb4b8460ea735ea1370498caebd76e0993408a99a2f06f1db&ipo=images",
    width: 300,
    height: 300,
    sponsored: false,
  },
  {
    id: 3,
    author: "Robert Brown",
    content: "Proud to announce our new partnership with InnovateX.",
    avatar: "https://ui-avatars.com/api/?name=Robert+Brown&background=random",
    companyId: "2",
    image:
      "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.hdwallpapers.in%2Fdownload%2Fthe_office_us_30_hd_movies-1280x720.jpg&f=1&nofb=1&ipt=e720df5bcc43adfcabed183b9d9d39e2bcf764d800a12141dcfe472ac72c2a9b&ipo=images",
    width: 300,
    height: 300,
    sponsored: false,
  },
  {
    id: 4,
    author: "Linda Johnson",
    content: "Launching our latest product line at GlobalTech.",
    avatar: "https://ui-avatars.com/api/?name=Linda+Johnson&background=random",
    companyId: "3",
    image:
      "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwork.life%2Fwp-content%2Fuploads%2F2020%2F08%2FOld-Street-Office-min-1-2.png&f=1&nofb=1&ipt=91a46ac934eadb3c2f1570c9414ad34ff700ffdd4b03aae84197dedcb76e1c57&ipo=images",
    width: 300,
    height: 300,
    sponsored: false,
  },
  {
    id: 5,
    author: "Michael Lee",
    content: "Celebrating five years of excellence at EnterpriseSolutions!",
    avatar: "https://ui-avatars.com/api/?name=Michael+Lee&background=random",
    companyId: "4",
    image:
      "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.flipspaces.com%2Fuploads%2Fimages%2F1680019390_71263cdf19bb9ad5d8de.png&f=1&nofb=1&ipt=fd515c2a1af0f7bb08310a6a09032b4ed878efc06bce684697363533c78545e8&ipo=images",
    width: 300,
    height: 300,
    sponsored: false,
  },
];

export default posts;
