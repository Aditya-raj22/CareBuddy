"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"

export function Navigation() {
  const pathname = usePathname()

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-white/95 backdrop-blur supports-[backdrop-filter]:bg-white/60">
      <div className="container flex h-16 items-center justify-between">
        <Link href="/" className="flex items-center space-x-2">
          <span className="text-xl font-bold text-blue-600">CareBuddy</span>
        </Link>
        <nav className="flex items-center space-x-6 text-sm font-medium">
          <Link
            href="/"
            className={cn(
              "transition-colors hover:text-blue-600",
              pathname === "/" ? "text-blue-500" : "text-foreground/60"
            )}
          >
            About
          </Link>
          <Link
            href="/doctors-dashboard"
            className={cn(
              "transition-colors hover:text-blue-600",
              pathname.startsWith("/doctors-dashboard") ? "text-blue-500" : "text-foreground/60"
            )}
          >
            Doctor's Dashboard
          </Link>
        </nav>
      </div>
    </header>
  )
}

