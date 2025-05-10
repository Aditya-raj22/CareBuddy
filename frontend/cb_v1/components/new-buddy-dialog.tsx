import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { createBuddy } from '@/lib/api';

interface NewBuddyDialogProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: (buddyId: string) => void;
}

export function NewBuddyDialog({ isOpen, onClose, onSuccess }: NewBuddyDialogProps) {
  const [name, setName] = useState('');
  const [files, setFiles] = useState<FileList | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    try {
      setLoading(true);
      setError(null);

      if (!name.trim()) {
        throw new Error('Please provide a name for your CareBuddy');
      }

      if (!files?.length) {
        throw new Error('Please upload at least one training document');
      }

      const buddyId = await createBuddy(name, files);
      setName('');
      setFiles(null);
      onSuccess(buddyId);
      onClose();
    } catch (err: any) {
      console.error('Error creating buddy:', err);
      setError(err.message || 'Failed to create buddy');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Create New CareBuddy</DialogTitle>
        </DialogHeader>

        <div className="grid gap-4 py-4">
          <div className="grid gap-2">
            <Label htmlFor="name">Name your CareBuddy</Label>
            <Input
              id="name"
              placeholder="e.g., Diabetes Care Assistant"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
          </div>

          <div className="grid gap-2">
            <Label>Upload Training Documents</Label>
            <Input
              type="file"
              multiple
              accept=".pdf,.doc,.docx,.txt"
              onChange={(e) => setFiles(e.target.files)}
            />
            <p className="text-sm text-muted-foreground">
              Upload PDF documents containing the medical information you want your CareBuddy to know
            </p>
          </div>

          {error && (
            <p className="text-sm text-red-600">
              {error}
            </p>
          )}

          <Button 
            onClick={handleSubmit} 
            disabled={loading}
            className="w-full"
          >
            {loading ? 'Creating...' : 'Create CareBuddy'}
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}