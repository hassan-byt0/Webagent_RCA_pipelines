// app/linkedin/user/[userId]/layout.tsx
import { ReactNode } from "react";

export default function UserLayout({ children }: { children: ReactNode }) {
  return <div className="p-4 bg-gray-50">{children}</div>;
}
