'use client';

import { useState, useEffect } from "react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Search, Plus } from 'lucide-react'
import Link from "next/link"
import { cn } from "@/lib/utils"
import {
  Sidebar,
  SidebarContent,
  SidebarHeader,
  SidebarFooter,
  SidebarProvider,
} from "@/components/ui/sidebar"
import { NewBuddyDialog } from "@/components/new-buddy-dialog"
import { getBuddies } from "@/lib/api"
import { useRouter } from "next/navigation"

type Buddy = {
  id: string;
  name: string;
};

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const router = useRouter();
  const [searchQuery, setSearchQuery] = useState("")
  const [buddies, setBuddies] = useState<Buddy[]>([])
  const [isNewBuddyDialogOpen, setIsNewBuddyDialogOpen] = useState(false)
  const [loading, setLoading] = useState(true)

  const fetchBuddies = async () => {
    try {
      const data = await getBuddies();
      setBuddies(data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching buddies:', error);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBuddies();
  }, []);

  const handleBuddyCreated = async (buddyId: string) => {
    await fetchBuddies();
    router.push(`/doctors-dashboard/buddy/${buddyId}`);
  };

  const filteredBuddies = buddies.filter(buddy =>
    buddy.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <SidebarProvider>
      <div className="grid lg:grid-cols-[240px_1fr]">
        <Sidebar className="pt-16">
          <SidebarHeader className="border-b p-4">
            <div className="relative">
              <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search buddies..."
                className="pl-8"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
          </SidebarHeader>
          <SidebarContent className="p-0">
            <nav className="grid gap-1 p-2">
              {loading ? (
                <div className="text-center py-4">Loading...</div>
              ) : filteredBuddies.length === 0 ? (
                <div className="text-center py-4 text-muted-foreground">
                  {searchQuery ? 'No buddies found' : 'No buddies yet'}
                </div>
              ) : (
                filteredBuddies.map((buddy) => (
                  <Link
                    key={buddy.id}
                    href={`/doctors-dashboard/buddy/${buddy.id}`}
                    className={cn(
                      "flex items-center gap-2 rounded-lg px-3 py-2 text-sm transition-colors hover:bg-gray-100"
                    )}
                  >
                    {buddy.name}
                  </Link>
                ))
              )}
            </nav>
          </SidebarContent>
          <SidebarFooter className="border-t p-4">
            <Button 
              onClick={() => setIsNewBuddyDialogOpen(true)}
              className="w-full"
            >
              <Plus className="mr-2 h-4 w-4" />
              Add New Buddy
            </Button>
          </SidebarFooter>
        </Sidebar>
        <main className="flex-1 overflow-auto pt-16">{children}</main>
      </div>

      <NewBuddyDialog
        isOpen={isNewBuddyDialogOpen}
        onClose={() => setIsNewBuddyDialogOpen(false)}
        onSuccess={handleBuddyCreated}
      />
    </SidebarProvider>
  );
}