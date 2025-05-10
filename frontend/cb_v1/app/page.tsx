"use client"

import { useEffect, useRef } from "react"
import Image from "next/image"
import { ContactDialog } from "@/components/contact-dialog"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export default function HomePage() {
  const storyRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("animate-fade-in")
          }
        })
      },
      {
        threshold: 0.1,
      }
    )

    const questions = document.querySelectorAll(".story-section")
    questions.forEach((question) => observer.observe(question))

    return () => observer.disconnect()
  }, [])

  return (
    <div className="flex flex-col">
      {/* Hero Section */}
      <section className="bg-white py-20">
        <div className="container">
          <div className="grid gap-8 md:grid-cols-3">
            <div className="flex items-center justify-center md:col-span-1">
              <div className="relative h-[300px] w-full">
                <Image
                  src="/images/hero/hero-image.png"
                  alt="CareBuddy Hero"
                  fill
                  className="object-contain"
                  priority
                />
              </div>
            </div>
            <div className="space-y-8 md:col-span-2 text-center">
              <h1 className="text-4xl font-bold tracking-tighter sm:text-5xl md:text-6xl">
                Your follow-up care companion!
              </h1>
              <p className="text-lg text-muted-foreground sm:text-xl">
                Have you ever had medical questions after your appointment with a doctor?
              </p>
              <p className="text-lg text-muted-foreground sm:text-xl">
                CareBuddy connects you with personalized, doctor-authorized advice anytime!
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Story Sections */}
      <section className="story-section min-h-screen flex items-center bg-blue-50">
        <div className="container">
          <div className="grid md:grid-cols-2 gap-16 items-center">
            <div className="relative aspect-square">
              <Image
                src="/images/story/story-1.jpg"
                alt="Elderly woman with a fractured foot"
                fill
                className="object-cover rounded-lg"
              />
            </div>
            <div className="text-center">
              <p className="text-2xl text-blue-900">
                After my grandmother fractured her foot, she had so many questions for her doctor...
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="story-section min-h-screen flex items-center bg-white">
        <div className="container">
          <div className="grid md:grid-cols-2 gap-16 items-center">
            <div className="relative aspect-square">
              <Image
                src="/images/story/story-2.jpg"
                alt="Person looking at medication"
                fill
                className="object-cover rounded-lg"
              />
            </div>
            <div className="text-center space-y-8">
              <p className="text-2xl">
                "I forgot to take my medication in the morning. Should I double the dose now or wait until tomorrow?"
              </p>
              <p className="text-2xl">
                "I'm in pain even after visiting the doctor. Is this normal? What can I do with what I have at home?"
              </p>
              <p className="text-2xl">
                "Can I eat this food with my condition and medication?"
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="story-section min-h-screen flex items-center bg-blue-50">
        <div className="container">
          <div className="grid md:grid-cols-2 gap-16 items-center">
            <div className="relative aspect-square">
              <Image
                src="/images/story/story-3.jpg"
                alt="CareBuddy helping patients"
                fill
                className="object-cover rounded-lg"
              />
            </div>
            <div className="text-center">
              <p className="text-2xl font-semibold text-blue-900">
                CareBuddy was built to answer her questions no matter the time of day or night, with answers her doctor would approve of.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="bg-white py-20">
        <div className="container">
          <div className="grid gap-8 md:grid-cols-2">
            <Card className="transition-transform hover:scale-105">
              <CardHeader>
                <CardTitle>Step 1</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="relative aspect-video w-full">
                  <Image
                    src="/images/steps/step-1.jpg"
                    alt="Doctor training CareBuddy"
                    fill
                    className="object-cover rounded-lg"
                  />
                </div>
                <p className="text-lg text-center">
                  Your doctor trains CareBuddy on medically caring for you after your appointment.
                </p>
              </CardContent>
            </Card>
            <Card className="transition-transform hover:scale-105">
              <CardHeader>
                <CardTitle>Step 2</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="relative aspect-video w-full">
                  <Image
                    src="/images/steps/step-2.jpg"
                    alt="WhatsApp connection"
                    fill
                    className="object-cover rounded-lg"
                  />
                </div>
                <p className="text-lg text-center">
                  You'll receive a WhatsApp number to talk to a CareBuddy
                </p>
              </CardContent>
            </Card>
            <Card className="transition-transform hover:scale-105">
              <CardHeader>
                <CardTitle>Step 3</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="relative aspect-video w-full">
                  <Image
                    src="/images/steps/step-3.jpg"
                    alt="CareBuddy answering questions"
                    fill
                    className="object-cover rounded-lg"
                  />
                </div>
                <p className="text-lg text-center">
                  CareBuddy keeps you connected with your doctor and answers your questions quickly using trusted information!
                </p>
              </CardContent>
            </Card>
            <Card className="transition-transform hover:scale-105">
              <CardHeader>
                <CardTitle>Step 4</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="relative aspect-video w-full">
                  <Image
                    src="/images/steps/step-4.jpg"
                    alt="Doctor notification"
                    fill
                    className="object-cover rounded-lg"
                  />
                </div>
                <p className="text-lg text-center">
                  When CareBuddy can't answer your questions, your doctors are immediately notified
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section className="bg-blue-50 py-20">
        <div className="container text-center">
          <ContactDialog />
        </div>
      </section>
    </div>
  )
}

