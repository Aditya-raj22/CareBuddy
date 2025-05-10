// frontend/cb_v1/app/doctors-dashboard/buddy/[id]/page.tsx
'use client';

import { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { getBuddyAnalytics, getBuddyDetails } from '@/lib/api';

export default function BuddyDetailPage({
  params,
}: {
  params: { id: string };
}) {
  const [loading, setLoading] = useState(true);
  const [buddy, setBuddy] = useState<any>(null);
  const [whatsappInfo, setWhatsappInfo] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const buddyData = await getBuddyDetails(params.id);
        setBuddy(buddyData);
        setWhatsappInfo(`wa.me/${buddyData.whatsapp_number}`);
      } catch (error) {
        console.error('Error fetching buddy details:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [params.id]);

  if (loading) {
    return (
      <div className="p-8">
        <h1 className="text-2xl font-bold">Loading...</h1>
      </div>
    );
  }

  return (
    <div className="p-8 space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">{buddy?.name}</h1>
        <p className="text-sm text-muted-foreground">ID: {params.id}</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>WhatsApp Connection</CardTitle>
        </CardHeader>
        <CardContent>
          <p>To chat with this CareBuddy:</p>
          <ol className="list-decimal ml-4 mt-2 space-y-2">
            <li>Open WhatsApp on your phone</li>
            <li>Send "CONNECT {params.id}" to <strong>{whatsappInfo}</strong></li>
            <li>Start asking your questions!</li>
          </ol>
        </CardContent>
      </Card>

      {/* Analytics Card */}
      <Card>
        <CardHeader>
          <CardTitle>Performance</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-sm text-muted-foreground">Questions Answered</p>
              <p className="text-2xl font-bold">{buddy?.stats?.total_questions || 0}</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Active Patients</p>
              <p className="text-2xl font-bold">{buddy?.stats?.active_patients || 0}</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Response Rate</p>
              <p className="text-2xl font-bold">{buddy?.stats?.response_rate || 0}%</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Average Rating</p>
              <p className="text-2xl font-bold">{buddy?.stats?.average_rating || 0}/5</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Documents Card */}
      <Card>
        <CardHeader>
          <CardTitle>Training Documents</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            {buddy?.documents?.map((doc: any) => (
              <div key={doc.id} className="flex justify-between items-center p-2 border rounded">
                <span>{doc.name}</span>
                <span className="text-sm text-muted-foreground">
                  {new Date(doc.uploaded_at).toLocaleDateString()}
                </span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}