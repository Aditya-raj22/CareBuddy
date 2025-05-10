import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

export function Footer() {
  return (
    <footer className="border-t bg-white">
      <div className="container py-8 md:py-12">
        <div className="grid gap-8 md:grid-cols-2">
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">CareBuddy</h3>
            <p className="text-sm text-muted-foreground">
              Bridging the gap in follow-up care with personalized, doctor-approved guidance.
            </p>
          </div>
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Stay in touch with us</h3>
            <form className="flex gap-2 max-w-md">
              <Input 
                type="email" 
                placeholder="Enter your email" 
                className="flex-1"
              />
              <Button type="submit" className="bg-blue-600 hover:bg-blue-700">
                Subscribe
              </Button>
            </form>
          </div>
        </div>
        <div className="mt-8 border-t pt-8 text-center text-sm text-muted-foreground">
          © {new Date().getFullYear()} CareBuddy. All rights reserved.
        </div>
      </div>
    </footer>
  )
}

