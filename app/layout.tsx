import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "BancABC IntelliBank | Customer Intelligence",
  description: "Customer analytics and decision support for BancABC."
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
